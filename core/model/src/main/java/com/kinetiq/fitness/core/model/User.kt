package com.kinetiq.fitness.core.model

enum class WorkoutLocation {
    HOME,
    COMMERCIAL_GYM
}

enum class GoalType {
    WEIGHT_LOSS,
    MUSCLE_GAIN,
    STRENGTH,
    ENDURANCE
}

enum class GoalMode {
    DATE,
    PACE
}

enum class BiologicalSex {
    MALE,
    FEMALE
}

enum class ActivityLevel(val multiplier: Double) {
    SEDENTARY(1.2),
    LIGHTLY_ACTIVE(1.375),
    MODERATELY_ACTIVE(1.55),
    VERY_ACTIVE(1.725),
    EXTRA_ACTIVE(1.9)
}

enum class TrainingExperience {
    BEGINNER,
    INTERMEDIATE,
    EXPERIENCED
}

enum class PreferredSplit {
    FULL_BODY,
    UPPER_LOWER,
    PUSH_PULL_LEGS,
    NO_PREFERENCE
}

data class UserProfile(
    val id: String = "primary_user",
    val heightCm: Double,
    val currentWeightKg: Double,
    val targetWeightKg: Double? = null,
    val sex: BiologicalSex,
    val ageYears: Int,
    val activityLevel: ActivityLevel,
    val goalType: GoalType,
    val goalMode: GoalMode? = null,
    val pacePreset: String? = null,
    val targetDateEpochMs: Long? = null,
    val target1RmKg: Double? = null,
    val targetDurationSeconds: Int? = null,
    val targetDistanceMeters: Double? = null,
    val workoutLocation: WorkoutLocation = WorkoutLocation.HOME,
    val equipmentInventory: List<String> = emptyList(),
    val parqPassed: Boolean,
    val parqDateEpochMs: Long,
    val injuryTags: List<String> = emptyList(),
    val experienceLevel: TrainingExperience,
    val preferredSplit: PreferredSplit,
    val createdAtEpochMs: Long = System.currentTimeMillis()
)
