package com.kinetiq.fitness.core.engine

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
