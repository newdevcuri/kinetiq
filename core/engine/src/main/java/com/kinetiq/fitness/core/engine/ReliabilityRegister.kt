package com.kinetiq.fitness.core.engine

object ReliabilityRegister {
    private const val PARQ_VALIDITY_DAYS = 90L
    private const val MS_PER_DAY = 24L * 60L * 60L * 1000L

    /**
     * Checks if PAR-Q+ pre-participation screening requires a 90-day refresh.
     */
    fun isParqScreeningDue(lastScreeningEpochMs: Long, currentEpochMs: Long): Boolean {
        val daysElapsed = (currentEpochMs - lastScreeningEpochMs) / MS_PER_DAY
        return daysElapsed >= PARQ_VALIDITY_DAYS
    }

    /**
     * Re-filters existing workout programs when a new injury tag is added mid-program.
     */
    fun reFilterProgramForNewInjury(
        currentProgramExerciseIds: List<String>,
        newInjuryTags: List<String>,
        exerciseContraindicationMap: Map<String, List<String>>
    ): List<String> {
        val upperInjuries = newInjuryTags.map { it.uppercase() }.toSet()
        return currentProgramExerciseIds.filter { exId ->
            val contra = exerciseContraindicationMap[exId] ?: emptyList()
            contra.none { upperInjuries.contains(it.uppercase()) }
        }
    }

    /**
     * Verifies Doze-safe elapsed real-time timer progression.
     */
    fun computeRemainingRestSeconds(
        timerStartElapsedRealtimeMs: Long,
        totalRestSeconds: Int,
        currentElapsedRealtimeMs: Long
    ): Int {
        val elapsedSeconds = ((currentElapsedRealtimeMs - timerStartElapsedRealtimeMs) / 1000L).toInt()
        return (totalRestSeconds - elapsedSeconds).coerceAtLeast(0)
    }
}
