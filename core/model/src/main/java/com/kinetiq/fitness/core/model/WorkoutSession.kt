package com.kinetiq.fitness.core.model

enum class SessionTrackType {
    STRENGTH,
    CARDIO
}

enum class ReadinessBand {
    LOW,
    NORMAL,
    HIGH
}

enum class CalorieSource {
    MET_ONLY,
    KEYTEL_HR_BLENDED
}

enum class SessionPhase {
    WARMUP_SRS,
    PRIMARY_COMPOUND,
    ACCESSORY,
    COOLDOWN
}

data class WorkoutSession(
    val id: String,
    val dateEpochMs: Long,
    val plannedDurationMinutes: Int,
    val actualDurationMinutes: Int = 0,
    val trackType: SessionTrackType,
    val readinessBand: ReadinessBand,
    val estimatedCaloriesBurned: Double = 0.0,
    val calorieSource: CalorieSource = CalorieSource.MET_ONLY,
    val completed: Boolean = false,
    val notes: String = ""
)

data class SetLog(
    val id: String,
    val sessionId: String,
    val exerciseId: String,
    val setNumber: Int,
    val phase: SessionPhase,
    val targetReps: Int,
    val actualReps: Int,
    val weightKg: Double,
    val rir: Int,
    val tempo: String,
    val completed: Boolean,
    val timestampEpochMs: Long = System.currentTimeMillis()
)
