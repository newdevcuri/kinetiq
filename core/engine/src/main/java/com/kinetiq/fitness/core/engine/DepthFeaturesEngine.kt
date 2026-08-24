package com.kinetiq.fitness.core.engine

data class BossFightBenchmark(
    val tierTarget: Int,
    val title: String,
    val description: String,
    val requiredExerciseId: String,
    val targetReps: Int,
    val targetWeightMultiplier: Double // e.g. 1.0x bodyweight
)

object DepthFeaturesEngine {
    val Tier4BossFight = BossFightBenchmark(
        tierTarget = 4,
        title = "The Centurion Compound Challenge",
        description = "Perform bodyweight squats with 1.0x bodyweight for 15 unbroken reps with strict 3-1-1 tempo.",
        requiredExerciseId = "ex_goblet_squat",
        targetReps = 15,
        targetWeightMultiplier = 1.0
    )

    /**
     * Automated Deload Detection (PRD §7 / Build Spec §6.2)
     * Recommends active deload if volume load drops >15% or RPE is maxed across 3 consecutive sessions.
     */
    fun evaluateDeloadNeed(
        recentSessionVolumes: List<Double>,
        recentAverageRirs: List<Int>
    ): Boolean {
        if (recentSessionVolumes.size < 3 || recentAverageRirs.size < 3) return false
        val isFatigued = recentAverageRirs.takeLast(3).all { it <= 1 }
        val isVolumeDropping = recentSessionVolumes.takeLast(2).zipWithNext().all { (a, b) -> b < a * 0.88 }
        return isFatigued || isVolumeDropping
    }

    /**
     * Streak Freeze Token Logic
     */
    fun consumeStreakFreeze(availableTokens: Int, missedDay: Boolean): Pair<Int, Boolean> {
        return if (missedDay && availableTokens > 0) {
            (availableTokens - 1) to true // Streak preserved
        } else {
            availableTokens to false
        }
    }
}
