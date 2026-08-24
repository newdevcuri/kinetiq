package com.kinetiq.fitness.core.engine

import com.kinetiq.fitness.core.model.ActivityLevel
import com.kinetiq.fitness.core.model.BiologicalSex
import com.kinetiq.fitness.core.model.GoalType

sealed class GoalPlanResult {
    data class Feasible(
        val targetDateEpochMs: Long,
        val estimatedWeeks: Int,
        val weeklyPacePercent: Double,
        val trajectory: List<Pair<Int, Double>>
    ) : GoalPlanResult()

    data class CorrectedToSafeDate(
        val requestedDateEpochMs: Long,
        val safeDateEpochMs: Long,
        val safeWeeks: Int,
        val reason: String,
        val safeTrajectory: List<Pair<Int, Double>>
    ) : GoalPlanResult()
}

object GoalFeasibilityEngine {
    private const val MS_PER_WEEK = 7L * 24L * 60L * 60L * 1000L

    fun evaluateGoalFeasibility(
        goalType: GoalType,
        currentWeightKg: Double,
        targetWeightKg: Double?,
        heightCm: Double,
        ageYears: Int,
        sex: BiologicalSex,
        activityLevel: ActivityLevel,
        requestedTargetDateEpochMs: Long? = null,
        pacePreset: String? = "MODERATE"
    ): GoalPlanResult {
        if (goalType != GoalType.WEIGHT_LOSS || targetWeightKg == null || targetWeightKg >= currentWeightKg) {
            val defaultWeeks = 12
            val targetMs = System.currentTimeMillis() + (defaultWeeks * MS_PER_WEEK)
            return GoalPlanResult.Feasible(
                targetDateEpochMs = targetMs,
                estimatedWeeks = defaultWeeks,
                weeklyPacePercent = 0.5,
                trajectory = listOf(0 to currentWeightKg, defaultWeeks to (targetWeightKg ?: currentWeightKg))
            )
        }

        val weightToLose = currentWeightKg - targetWeightKg

        // Moderate: 0.5% bodyweight/week, Aggressive: 1.0% bodyweight/week (hard cap)
        val weeklyPacePercent = if (pacePreset == "AGGRESSIVE") 0.010 else 0.006
        val weeklyLossTargetKg = currentWeightKg * weeklyPacePercent
        val weeklyDeficitKcal = weeklyLossTargetKg * 7700.0

        val trajectory = MetabolicEngine.simulateWeightLossTrajectory(
            startWeightKg = currentWeightKg,
            targetWeightKg = targetWeightKg,
            heightCm = heightCm,
            ageYears = ageYears,
            sex = sex,
            activityLevel = activityLevel,
            weeklyDeficitKcal = weeklyDeficitKcal
        )

        val safeWeeks = trajectory.last().first
        val safeTargetDateEpochMs = System.currentTimeMillis() + (safeWeeks * MS_PER_WEEK)

        if (requestedTargetDateEpochMs != null) {
            val requestedWeeks = ((requestedTargetDateEpochMs - System.currentTimeMillis()) / MS_PER_WEEK).toInt().coerceAtLeast(1)
            if (requestedWeeks < safeWeeks) {
                return GoalPlanResult.CorrectedToSafeDate(
                    requestedDateEpochMs = requestedTargetDateEpochMs,
                    safeDateEpochMs = safeTargetDateEpochMs,
                    safeWeeks = safeWeeks,
                    reason = "Your requested date requires exceeding the 1% weekly body weight loss safety threshold. Adjusted to the earliest clinically sound timeline.",
                    safeTrajectory = trajectory
                )
            }
        }

        return GoalPlanResult.Feasible(
            targetDateEpochMs = safeTargetDateEpochMs,
            estimatedWeeks = safeWeeks,
            weeklyPacePercent = weeklyPacePercent * 100.0,
            trajectory = trajectory
        )
    }
}
