package com.kinetiq.fitness.core.engine

import com.kinetiq.fitness.core.model.BiologicalSex
import com.kinetiq.fitness.core.model.CalorieSource

data class CalorieCalculationResult(
    val totalCaloriesBurned: Double,
    val source: CalorieSource,
    val hrCoveragePercent: Double
)

object KeytelCalorieEngine {
    /**
     * Keytel et al. (2005) Heart Rate Regression Formula
     * Male: EE = [(-55.0969 + (0.6309 * HR) + (0.1988 * W) + (0.2017 * A)) / 4.184] * 60 [kcal/hr]
     * Female: EE = [(-20.4022 + (0.4472 * HR) - (0.1263 * W) + (0.074 * A)) / 4.184] * 60 [kcal/hr]
     */
    fun calculateInstantaneousKcalPerMinute(
        heartRateBpm: Double,
        weightKg: Double,
        ageYears: Int,
        sex: BiologicalSex
    ): Double {
        val kcalPerMin = if (sex == BiologicalSex.MALE) {
            (-55.0969 + (0.6309 * heartRateBpm) + (0.1988 * weightKg) + (0.2017 * ageYears)) / 4.184
        } else {
            (-20.4022 + (0.4472 * heartRateBpm) - (0.1263 * weightKg) + (0.0740 * ageYears)) / 4.184
        }
        return kcalPerMin.coerceAtLeast(0.5)
    }

    /**
     * Integrates per-minute HR samples with gap filling:
     * - Gaps < 5 minutes: Linear interpolation between valid HR samples.
     * - Gaps >= 5 minutes: Revert to Compendium METs for that segment and mark source as MET_ONLY.
     */
    fun calculateSessionCalories(
        hrSamplesPerMinute: List<Double?>,
        weightKg: Double,
        ageYears: Int,
        sex: BiologicalSex,
        defaultMetValue: Double = 6.0 // Standard vigorous resistance training MET
    ): CalorieCalculationResult {
        if (hrSamplesPerMinute.isEmpty()) {
            return CalorieCalculationResult(0.0, CalorieSource.MET_ONLY, 0.0)
        }

        var totalKcal = 0.0
        var validHrCount = 0
        var consecutiveMissingHr = 0
        var lastValidHr: Double? = null

        val metKcalPerMin = (defaultMetValue * 3.5 * weightKg) / 200.0

        for (sample in hrSamplesPerMinute) {
            if (sample != null && sample > 40.0 && sample < 220.0) {
                // Valid HR sample
                lastValidHr = sample
                validHrCount++
                consecutiveMissingHr = 0
                totalKcal += calculateInstantaneousKcalPerMinute(sample, weightKg, ageYears, sex)
            } else {
                consecutiveMissingHr++
                if (consecutiveMissingHr < 5 && lastValidHr != null) {
                    // Gap < 5 min: Linear approximation using last known HR
                    totalKcal += calculateInstantaneousKcalPerMinute(lastValidHr, weightKg, ageYears, sex)
                } else {
                    // Gap >= 5 min: Fallback to Compendium MET equation
                    totalKcal += metKcalPerMin
                }
            }
        }

        val coverage = (validHrCount.toDouble() / hrSamplesPerMinute.size.toDouble()) * 100.0
        val source = if (coverage >= 70.0) CalorieSource.KEYTEL_HR_BLENDED else CalorieSource.MET_ONLY

        return CalorieCalculationResult(
            totalCaloriesBurned = totalKcal,
            source = source,
            hrCoveragePercent = coverage
        )
    }
}
