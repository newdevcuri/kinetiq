package com.kinetiq.fitness.core.engine

import com.kinetiq.fitness.core.model.*

data class GeneratedWorkoutPlan(
    val sessionId: String,
    val trackType: SessionTrackType,
    val totalEstimatedDurationMinutes: Int,
    val warmupExercises: List<Exercise>,
    val primaryCompounds: List<Exercise>,
    val accessories: List<Exercise>,
    val cooldownExercises: List<Exercise>,
    val targetSetsPerExercise: Map<String, Int>,
    val targetRir: Int,
    val readinessAdjustmentNote: String?
)

object WorkoutGeneratorEngine {
    // Guaranteed safe floor exercises for extreme contraindication conflicts
    private val SAFE_FLOOR_EXERCISE_IDS = listOf("ex_plank", "ex_glute_bridge", "ex_deadbug")

    fun generateSession(
        allExercises: List<Exercise>,
        userProfile: UserProfile,
        targetDurationMinutes: Int = 45, // 15, 30, 45, 60
        trackType: SessionTrackType = SessionTrackType.STRENGTH,
        readiness: ReadinessAssessment = ReadinessAssessment(ReadinessBand.NORMAL, 80, 1.0, 0, "Normal")
    ): GeneratedWorkoutPlan {
        val userEquipment = userProfile.equipmentInventory.map { it.uppercase() }.toSet()
        val userInjuries = userProfile.injuryTags.map { it.uppercase() }.toSet()

        // 1. Filter exercises strictly matching available equipment and excluding contraindications
        val eligibleExercises = allExercises.filter { ex ->
            val equipMatches = ex.equipment.name == "BODYWEIGHT" || userEquipment.contains(ex.equipment.name)
            val noContraindication = ex.contraindications.none { userInjuries.contains(it.uppercase()) }
            equipMatches && noContraindication
        }

        // 2. Handle Clinical-Logic Tag Conflict: If filtering yields empty result set, fall back to safe floor exercises
        val usablePool = if (eligibleExercises.isEmpty()) {
            allExercises.filter { it.id in SAFE_FLOOR_EXERCISE_IDS }
        } else {
            eligibleExercises
        }

        // 3. Time-Constrained Phase Allocation with Protected Floors (§7d)
        // Warmup: min 4 min, Cooldown: min 4 min
        val warmupMinutes = (targetDurationMinutes * 0.15).toInt().coerceAtLeast(4)
        val cooldownMinutes = (targetDurationMinutes * 0.15).toInt().coerceAtLeast(4)
        val mainMinutes = (targetDurationMinutes - warmupMinutes - cooldownMinutes).coerceAtLeast(7)

        val warmups = usablePool.filter { it.category == ExerciseCategory.MOBILITY || it.tier == 1 }.take(2)
        val primaries = usablePool.filter { it.category == ExerciseCategory.STRENGTH && it.tier >= 2 }.take(2)
            .ifEmpty { usablePool.take(1) }
        
        val primaryIds = primaries.map { it.id }.toSet()
        val accessories = if (targetDurationMinutes <= 15) {
            emptyList() // Drop accessory first for 15-min micro sessions
        } else {
            usablePool.filter { it.id !in primaryIds && it.tier <= 2 }.take(3)
        }

        val cooldowns = usablePool.filter { it.movementPattern == MovementPattern.CORE || it.category == ExerciseCategory.MOBILITY }.take(2)

        val setsMap = mutableMapOf<String, Int>()
        val baseSets = if (targetDurationMinutes <= 30) 2 else 3
        val adjustedSets = (baseSets * readiness.volumeMultiplier).toInt().coerceAtLeast(2)

        primaries.forEach { setsMap[it.id] = adjustedSets }
        accessories.forEach { setsMap[it.id] = (adjustedSets - 1).coerceAtLeast(2) }

        return GeneratedWorkoutPlan(
            sessionId = "session_" + System.currentTimeMillis(),
            trackType = trackType,
            totalEstimatedDurationMinutes = targetDurationMinutes,
            warmupExercises = warmups,
            primaryCompounds = primaries,
            accessories = accessories,
            cooldownExercises = cooldowns,
            targetSetsPerExercise = setsMap,
            targetRir = (2 + readiness.rirAdjustment).coerceIn(1, 4),
            readinessAdjustmentNote = if (readiness.band != ReadinessBand.NORMAL) readiness.explanation else null
        )
    }
}
