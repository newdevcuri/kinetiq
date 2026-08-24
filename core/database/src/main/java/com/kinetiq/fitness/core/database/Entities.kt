package com.kinetiq.fitness.core.database

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val heightCm: Double,
    val currentWeightKg: Double,
    val targetWeightKg: Double?,
    val sex: String,
    val ageYears: Int,
    val activityLevel: String,
    val goalType: String,
    val goalMode: String?,
    val pacePreset: String?,
    val targetDateEpochMs: Long?,
    val target1RmKg: Double?,
    val targetDurationSeconds: Int?,
    val targetDistanceMeters: Double?,
    val workoutLocation: String,
    val parqPassed: Boolean,
    val parqDateEpochMs: Long,
    val injuryTagsJson: String,
    val equipmentInventoryJson: String,
    val experienceLevel: String,
    val preferredSplit: String,
    val createdAtEpochMs: Long
)

@Entity(tableName = "exercises")
data class ExerciseEntity(
    @PrimaryKey val id: String,
    val name: String,
    val category: String,
    val movementPattern: String,
    val primaryMuscle: String,
    val secondaryMusclesJson: String,
    val equipment: String,
    val tier: Int,
    val fatigueCost: Double,
    val contraindicationsJson: String,
    val instructions: String,
    val safetyNotes: String,
    val tempoEccentric: Int,
    val tempoIsometric: Int,
    val tempoConcentric: Int,
    val animationAssetPath: String,
    val thumbnailAssetPath: String
)

@Entity(tableName = "workout_sessions")
data class WorkoutSessionEntity(
    @PrimaryKey val id: String,
    val dateEpochMs: Long,
    val plannedDurationMinutes: Int,
    val actualDurationMinutes: Int,
    val trackType: String,
    val readinessBand: String,
    val estimatedCaloriesBurned: Double,
    val calorieSource: String,
    val completed: Boolean,
    val notes: String
)

@Entity(
    tableName = "set_logs",
    foreignKeys = [
        ForeignKey(
            entity = WorkoutSessionEntity::class,
            parentColumns = ["id"],
            childColumns = ["sessionId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = ExerciseEntity::class,
            parentColumns = ["id"],
            childColumns = ["exerciseId"],
            onDelete = ForeignKey.RESTRICT
        )
    ],
    indices = [Index("sessionId"), Index("exerciseId")]
)
data class SetLogEntity(
    @PrimaryKey val id: String,
    val sessionId: String,
    val exerciseId: String,
    val setNumber: Int,
    val phase: String,
    val targetReps: Int,
    val actualReps: Int,
    val weightKg: Double,
    val rir: Int,
    val tempo: String,
    val completed: Boolean,
    val timestampEpochMs: Long
)

@Entity(tableName = "daily_readiness_logs")
data class DailyReadinessLogEntity(
    @PrimaryKey val dateEpochDay: Long,
    val sleepMinutes: Int?,
    val hrBaselineDeltaBpm: Double?,
    val selfReportedSorenessScore: Int?,
    val computedBand: String,
    val adjustmentApplied: String
)

@Entity(tableName = "body_weight_logs")
data class BodyWeightLogEntity(
    @PrimaryKey val id: String,
    val dateEpochMs: Long,
    val weightKg: Double,
    val notes: String
)

@Entity(
    tableName = "srs_reviews",
    foreignKeys = [
        ForeignKey(
            entity = ExerciseEntity::class,
            parentColumns = ["id"],
            childColumns = ["exerciseId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("exerciseId")]
)
data class SrsReviewEntity(
    @PrimaryKey val id: String,
    val exerciseId: String,
    val formCueId: String,
    val intervalDays: Double,
    val repetitionNumber: Int,
    val easeFactor: Double,
    val nextReviewEpochMs: Long,
    val lastReviewEpochMs: Long
)
