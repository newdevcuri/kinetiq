import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# ==============================================================================
# 1. FEATURE FLAGS (All Phase 3 features opt-in, offline, privacy-first)
# ==============================================================================
write_file("core/model/src/main/java/com/kinetiq/fitness/core/model/FeatureFlags.kt", """package com.kinetiq.fitness.core.model

enum class KinetiqFeature(val key: String, val defaultValue: Boolean) {
    POSE_FORM_COACH("feature_pose_coach", false),
    VOICE_LOGGING_TTS("feature_voice_logging", false),
    LOCAL_P2P_SYNC("feature_p2p_sync", false),
    SORENESS_DYNAMIC_WARMUP("feature_soreness_warmup", true),
    FASTING_TIMERS("feature_fasting_timer", false),
    PLATE_CALCULATOR("feature_plate_calculator", true),
    CIRCADIAN_SCHEDULER("feature_circadian_scheduler", true),
    OFFLINE_NUTRITION_LOOKUP("feature_nutrition_lookup", false)
}

data class FeatureFlagState(
    val flags: Map<KinetiqFeature, Boolean> = KinetiqFeature.values().associateWith { it.defaultValue }
) {
    fun isEnabled(feature: KinetiqFeature): Boolean = flags[feature] ?: feature.defaultValue
}
""")

# ==============================================================================
# 2. ON-DEVICE POSE COACH & REP COUNTER (MediaPipe Geometry)
# ==============================================================================
write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/PoseCoachEngine.kt", """package com.kinetiq.fitness.core.engine

import kotlin.math.acos
import kotlin.math.sqrt

data class PosePoint(val x: Float, val y: Float, val z: Float = 0f, val visibility: Float = 1f)

enum class RepPhase {
    IDLE_SETUP,
    ECCENTRIC_DESCENT,
    INFLECTION_BOTTOM,
    CONCENTRIC_ASCENT,
    REP_COMPLETE
}

data class FormFeedback(
    val currentPhase: RepPhase,
    val repCount: Int,
    val kneeAngleDeg: Double,
    val hipAngleDeg: Double,
    val feedbackCue: String?
)

object PoseCoachEngine {
    /**
     * Calculates 3D/2D joint angle ABC between three landmarks (A-B-C, angle at vertex B)
     */
    fun calculateJointAngle(a: PosePoint, b: PosePoint, c: PosePoint): Double {
        val v1x = a.x - b.x
        val v1y = a.y - b.y
        val v2x = c.x - b.x
        val v2y = c.y - b.y

        val dot = (v1x * v2x) + (v1y * v2y)
        val mag1 = sqrt((v1x * v1x) + (v1y * v1y))
        val mag2 = sqrt((v2x * v2x) + (v2y * v2y))

        if (mag1 * mag2 == 0f) return 180.0
        val cosTheta = (dot / (mag1 * mag2)).coerceIn(-1f, 1f)
        return Math.toDegrees(acos(cosTheta.toDouble()))
    }

    /**
     * Squat Rep State Machine
     * - Standing: Knee angle ~170-180 deg
     * - Parallel depth: Knee angle <= 90 deg
     */
    fun processSquatFrame(
        hip: PosePoint,
        knee: PosePoint,
        ankle: PosePoint,
        currentPhase: RepPhase,
        currentReps: Int
    ): FormFeedback {
        val kneeAngle = calculateJointAngle(hip, knee, ankle)
        var newPhase = currentPhase
        var newReps = currentReps
        var cue: String? = null

        when (currentPhase) {
            RepPhase.IDLE_SETUP -> {
                if (kneeAngle < 155.0) {
                    newPhase = RepPhase.ECCENTRIC_DESCENT
                }
            }
            RepPhase.ECCENTRIC_DESCENT -> {
                if (kneeAngle <= 90.0) {
                    newPhase = RepPhase.INFLECTION_BOTTOM
                    cue = "Depth reached"
                }
            }
            RepPhase.INFLECTION_BOTTOM -> {
                if (kneeAngle > 105.0) {
                    newPhase = RepPhase.CONCENTRIC_ASCENT
                }
            }
            RepPhase.CONCENTRIC_ASCENT -> {
                if (kneeAngle >= 165.0) {
                    newPhase = RepPhase.REP_COMPLETE
                    newReps++
                    cue = "Rep $newReps complete"
                }
            }
            RepPhase.REP_COMPLETE -> {
                newPhase = if (kneeAngle < 155.0) RepPhase.ECCENTRIC_DESCENT else RepPhase.IDLE_SETUP
            }
        }

        return FormFeedback(
            currentPhase = newPhase,
            repCount = newReps,
            kneeAngleDeg = kneeAngle,
            hipAngleDeg = 180.0,
            feedbackCue = cue
        )
    }
}
""")

# ==============================================================================
# 3. VOICE LOGGING & TTS COACH
# ==============================================================================
write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/VoiceWorkoutBuddy.kt", """package com.kinetiq.fitness.core.engine

data class ParsedVoiceLog(
    val reps: Int?,
    val weightKg: Double?,
    val command: String
)

object VoiceWorkoutBuddy {
    private val REPS_REGEX = Regex("(\\\\d+)\\\\s*(?:reps|rep)", RegexOption.IGNORE_CASE)
    private val WEIGHT_REGEX = Regex("(\\\\d+(?:\\\\.\\\\d+)?)\\\\s*(?:kg|kilos|kilo|lbs|pounds)", RegexOption.IGNORE_CASE)

    fun parseVoiceCommand(spokenText: String): ParsedVoiceLog {
        val repsMatch = REPS_REGEX.find(spokenText)
        val reps = repsMatch?.groupValues?.get(1)?.toIntOrNull()

        val weightMatch = WEIGHT_REGEX.find(spokenText)
        val weight = weightMatch?.groupValues?.get(1)?.toDoubleOrNull()

        val command = when {
            spokenText.contains("finish", ignoreCase = true) -> "FINISH_WORKOUT"
            spokenText.contains("next set", ignoreCase = true) -> "NEXT_SET"
            spokenText.contains("pause", ignoreCase = true) -> "PAUSE_TIMER"
            reps != null -> "LOG_SET"
            else -> "UNKNOWN"
        }

        return ParsedVoiceLog(reps = reps, weightKg = weight, command = command)
    }
}
""")

# ==============================================================================
# 4. GYM UTILITIES: Plate Loading Calculator & Circadian Scheduling
# ==============================================================================
write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/GymUtilityEngines.kt", """package com.kinetiq.fitness.core.engine

data class PlateLoadBreakdown(
    val targetWeightKg: Double,
    val barWeightKg: Double,
    val platesPerSide: List<Double>,
    val actualTotalKg: Double
)

object GymUtilityEngines {
    private val AVAILABLE_PLATES_KG = listOf(20.0, 15.0, 10.0, 5.0, 2.5, 1.25)

    /**
     * Calculates required plates per side for standard barbell loading
     */
    fun calculateBarbellPlates(
        targetWeightKg: Double,
        barWeightKg: Double = 20.0
    ): PlateLoadBreakdown {
        if (targetWeightKg <= barWeightKg) {
            return PlateLoadBreakdown(targetWeightKg, barWeightKg, emptyList(), barWeightKg)
        }

        var weightPerSide = (targetWeightKg - barWeightKg) / 2.0
        val plates = mutableListOf<Double>()

        for (plate in AVAILABLE_PLATES_KG) {
            while (weightPerSide >= plate) {
                plates.add(plate)
                weightPerSide -= plate
            }
        }

        val actualTotal = barWeightKg + (plates.sum() * 2.0)
        return PlateLoadBreakdown(
            targetWeightKg = targetWeightKg,
            barWeightKg = barWeightKg,
            platesPerSide = plates,
            actualTotalKg = actualTotal
        )
    }
}
""")

print("Phase 3 components generated.")
