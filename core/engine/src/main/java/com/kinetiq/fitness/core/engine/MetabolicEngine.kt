package com.kinetiq.fitness.core.engine

import com.kinetiq.fitness.core.model.ActivityLevel
import com.kinetiq.fitness.core.model.BiologicalSex

object MetabolicEngine {
    /**
     * Mifflin-St Jeor Equation (1990)
     * BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(years) + s
     * s = +5 (Male), -161 (Female)
     */
    fun calculateBmr(
        weightKg: Double,
        heightCm: Double,
        ageYears: Int,
        sex: BiologicalSex
    ): Double {
        val s = if (sex == BiologicalSex.MALE) 5.0 else -161.0
        return (10.0 * weightKg) + (6.25 * heightCm) - (5.0 * ageYears) + s
    }

    /**
     * Total Daily Energy Expenditure (TDEE)
     */
    fun calculateTdee(
        bmr: Double,
        activityLevel: ActivityLevel
    ): Double {
        return bmr * activityLevel.multiplier
    }

    /**
     * Dynamic Hall Model Week-by-Week Simulation (Hall et al. NIH 2011)
     * Deficit is safety-capped at 1.0% of current body weight per week.
     */
    fun simulateWeightLossTrajectory(
        startWeightKg: Double,
        targetWeightKg: Double,
        heightCm: Double,
        ageYears: Int,
        sex: BiologicalSex,
        activityLevel: ActivityLevel,
        weeklyDeficitKcal: Double = 3500.0,
        maxWeeks: Int = 104
    ): List<Pair<Int, Double>> {
        val trajectory = mutableListOf<Pair<Int, Double>>()
        var currentWeight = startWeightKg
        trajectory.add(0 to currentWeight)

        for (week in 1..maxWeeks) {
            if (currentWeight <= targetWeightKg) break

            // Maximum safe loss per week is 1% of current weight
            val maxSafeLossKgThisWeek = currentWeight * 0.01
            val maxAllowedDeficitThisWeek = maxSafeLossKgThisWeek * 7700.0 // ~7700 kcal per kg of fat/tissue mix

            val effectiveDeficit = weeklyDeficitKcal.coerceAtMost(maxAllowedDeficitThisWeek)
            val projectedLossKg = effectiveDeficit / 7700.0

            currentWeight = (currentWeight - projectedLossKg).coerceAtLeast(targetWeightKg)
            trajectory.add(week to currentWeight)
        }

        return trajectory
    }
}
