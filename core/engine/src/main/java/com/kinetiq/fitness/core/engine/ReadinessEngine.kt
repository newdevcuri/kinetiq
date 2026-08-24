package com.kinetiq.fitness.core.engine

import com.kinetiq.fitness.core.model.ReadinessBand

data class ReadinessAssessment(
    val band: ReadinessBand,
    val score: Int, // 0 to 100
    val volumeMultiplier: Double,
    val rirAdjustment: Int,
    val explanation: String
)

object ReadinessEngine {
    fun computeReadiness(
        yesterdayIntensityVolume: Double?, // Fallback signal (always available locally)
        lastNightSleepMinutes: Int? = null,
        hrBaselineDeltaBpm: Double? = null, // e.g. +5 bpm above 14-day rolling average
        selfReportedSorenessScore: Int? = null // 1 (fresh) to 5 (extremely sore)
    ): ReadinessAssessment {
        var score = 80 // baseline normal

        // Factor 1: Yesterday logged volume
        if (yesterdayIntensityVolume != null && yesterdayIntensityVolume > 10000.0) {
            score -= 25
        }

        // Factor 2: Sleep duration
        if (lastNightSleepMinutes != null) {
            if (lastNightSleepMinutes < 360) score -= 20 // <6 hrs
            else if (lastNightSleepMinutes >= 480) score += 10 // 8+ hrs
        }

        // Factor 3: Elevated resting heart rate
        if (hrBaselineDeltaBpm != null) {
            if (hrBaselineDeltaBpm >= 5.0) score -= 15
            else if (hrBaselineDeltaBpm <= -2.0) score += 5
        }

        // Factor 4: Soreness
        if (selfReportedSorenessScore != null) {
            if (selfReportedSorenessScore >= 4) score -= 20
        }

        return when {
            score < 60 -> ReadinessAssessment(
                band = ReadinessBand.LOW,
                score = score.coerceIn(0, 100),
                volumeMultiplier = 0.85, // 15% reduction
                rirAdjustment = +1,      // Leave 1 extra rep in reserve
                explanation = "Lower volume today — recent load & recovery signals suggest focusing on technique and quality."
            )
            score > 85 -> ReadinessAssessment(
                band = ReadinessBand.HIGH,
                score = score.coerceIn(0, 100),
                volumeMultiplier = 1.10,
                rirAdjustment = 0,
                explanation = "Optimal readiness today — primed for progressive overload within safe parameters."
            )
            else -> ReadinessAssessment(
                band = ReadinessBand.NORMAL,
                score = score.coerceIn(0, 100),
                volumeMultiplier = 1.0,
                rirAdjustment = 0,
                explanation = "Balanced recovery — ready for your standard planned session."
            )
        }
    }
}
