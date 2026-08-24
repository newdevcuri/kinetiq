package com.kinetiq.fitness.core.engine

data class SymmetryEvaluation(
    val leftVolumeKg: Double,
    val rightVolumeKg: Double,
    val asymmetryPercentage: Double,
    val isImbalanced: Boolean,
    val explainablePrescription: String
)

object BilateralSymmetryEngine {
    /**
     * Evaluates bilateral limb strength balance.
     * Flags asymmetry > 10% with explainable auto-prescription.
     */
    fun evaluateSymmetry(leftVolumeKg: Double, rightVolumeKg: Double): SymmetryEvaluation {
        val maxVol = maxOf(leftVolumeKg, rightVolumeKg).coerceAtLeast(1.0)
        val diff = Math.abs(leftVolumeKg - rightVolumeKg)
        val asymmetryPct = (diff / maxVol) * 100.0

        val isImbalanced = asymmetryPct > 10.0
        val weakerSide = if (leftVolumeKg < rightVolumeKg) "Left" else "Right"

        val prescription = if (isImbalanced) {
            "Slight asymmetry detected (${asymmetryPct.toInt()}% difference). Auto-Prescription: Start unilateral sets with your $weakerSide side and match identical reps on the opposite side."
        } else {
            "Optimal symmetry (${asymmetryPct.toInt()}% difference). Left and right strength balance is well within safe thresholds."
        }

        return SymmetryEvaluation(
            leftVolumeKg = leftVolumeKg,
            rightVolumeKg = rightVolumeKg,
            asymmetryPercentage = asymmetryPct,
            isImbalanced = isImbalanced,
            explainablePrescription = prescription
        )
    }
}
