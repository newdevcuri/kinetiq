package com.kinetiq.fitness.core.model

enum class ExerciseCategory {
    STRENGTH,
    CARDIO,
    MOBILITY
}

enum class MovementPattern {
    SQUAT,
    HINGE,
    HORIZONTAL_PUSH,
    HORIZONTAL_PULL,
    VERTICAL_PUSH,
    VERTICAL_PULL,
    LUNGE,
    CARRY,
    CORE,
    ISOLATION,
    CARDIO_INTERVAL,
    CARDIO_STEADY
}

enum class EquipmentType {
    BODYWEIGHT,
    DUMBBELL,
    BARBELL,
    RESISTANCE_BAND,
    KETTLEBELL,
    PULL_UP_BAR,
    BENCH,
    CARDIO_MACHINE
}

data class Exercise(
    val id: String,
    val name: String,
    val category: ExerciseCategory,
    val movementPattern: MovementPattern,
    val primaryMuscle: String,
    val secondaryMuscles: List<String>,
    val equipment: EquipmentType,
    val tier: Int,
    val fatigueCost: Double,
    val contraindications: List<String>,
    val instructions: String,
    val safetyNotes: String,
    val tempoEccentric: Int,
    val tempoIsometric: Int,
    val tempoConcentric: Int,
    val animationAssetPath: String,
    val thumbnailAssetPath: String
)
