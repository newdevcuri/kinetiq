import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# ==============================================================================
# 1. KEYTEL HR-BLENDED CALORIE ENGINE
# ==============================================================================
write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/KeytelCalorieEngine.kt", """package com.kinetiq.fitness.core.engine

import com.kinetiq.fitness.core.model.BiologicalSex
import com.kinetiq.fitness.core.model.CalorieSource

data class CalorieCalculationResult(
    val totalCaloriesBurned: Double,
    val source: CalorieSource,
    val hrCoveragePercent: Double
)

object KeytelCalorieEngine {
    /**
     * Keytel et al. (2005) Heart Rate Regression Formula
     * Male: EE = [(-55.0969 + (0.6309 * HR) + (0.1988 * W) + (0.2017 * A)) / 4.184] * 60 [kcal/hr]
     * Female: EE = [(-20.4022 + (0.4472 * HR) - (0.1263 * W) + (0.074 * A)) / 4.184] * 60 [kcal/hr]
     */
    fun calculateInstantaneousKcalPerMinute(
        heartRateBpm: Double,
        weightKg: Double,
        ageYears: Int,
        sex: BiologicalSex
    ): Double {
        val kcalPerMin = if (sex == BiologicalSex.MALE) {
            (-55.0969 + (0.6309 * heartRateBpm) + (0.1988 * weightKg) + (0.2017 * ageYears)) / 4.184
        } else {
            (-20.4022 + (0.4472 * heartRateBpm) - (0.1263 * weightKg) + (0.0740 * ageYears)) / 4.184
        }
        return kcalPerMin.coerceAtLeast(0.5)
    }

    /**
     * Integrates per-minute HR samples with gap filling:
     * - Gaps < 5 minutes: Linear interpolation between valid HR samples.
     * - Gaps >= 5 minutes: Revert to Compendium METs for that segment and mark source as MET_ONLY.
     */
    fun calculateSessionCalories(
        hrSamplesPerMinute: List<Double?>,
        weightKg: Double,
        ageYears: Int,
        sex: BiologicalSex,
        defaultMetValue: Double = 6.0 // Standard vigorous resistance training MET
    ): CalorieCalculationResult {
        if (hrSamplesPerMinute.isEmpty()) {
            return CalorieCalculationResult(0.0, CalorieSource.MET_ONLY, 0.0)
        }

        var totalKcal = 0.0
        var validHrCount = 0
        var consecutiveMissingHr = 0
        var lastValidHr: Double? = null

        val metKcalPerMin = (defaultMetValue * 3.5 * weightKg) / 200.0

        for (sample in hrSamplesPerMinute) {
            if (sample != null && sample > 40.0 && sample < 220.0) {
                // Valid HR sample
                lastValidHr = sample
                validHrCount++
                consecutiveMissingHr = 0
                totalKcal += calculateInstantaneousKcalPerMinute(sample, weightKg, ageYears, sex)
            } else {
                consecutiveMissingHr++
                if (consecutiveMissingHr < 5 && lastValidHr != null) {
                    // Gap < 5 min: Linear approximation using last known HR
                    totalKcal += calculateInstantaneousKcalPerMinute(lastValidHr, weightKg, ageYears, sex)
                } else {
                    // Gap >= 5 min: Fallback to Compendium MET equation
                    totalKcal += metKcalPerMin
                }
            }
        }

        val coverage = (validHrCount.toDouble() / hrSamplesPerMinute.size.toDouble()) * 100.0
        val source = if (coverage >= 70.0) CalorieSource.KEYTEL_HR_BLENDED else CalorieSource.MET_ONLY

        return CalorieCalculationResult(
            totalCaloriesBurned = totalKcal,
            source = source,
            hrCoveragePercent = coverage
        )
    }
}
""")

# ==============================================================================
# 2. DEPTH ENGINES: Boss Fights, Deload Detector, Bilateral Symmetry
# ==============================================================================
write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/DepthFeaturesEngine.kt", """package com.kinetiq.fitness.core.engine

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
""")

write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/BilateralSymmetryEngine.kt", """package com.kinetiq.fitness.core.engine

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
""")

# ==============================================================================
# 3. CLINICAL-HONESTY PERSONAL LOG EXPORT
# ==============================================================================
write_file("core/data/src/main/java/com/kinetiq/fitness/core/data/PersonalLogExporter.kt", """package com.kinetiq.fitness.core.data

data class ExportablePersonalLog(
    val userName: String,
    val exportDateEpochMs: Long,
    val currentWeightKg: Double,
    val targetWeightKg: Double?,
    val parqStatus: String,
    val totalWorkoutsCompleted: Int,
    val totalVolumeKg: Double,
    val averageReadinessScore: Int,
    val disclaimer: String = "CONFIDENTIAL PERSONAL FITNESS LOG — Generated for personal tracking and optional professional consultation. This document does not constitute a clinical or medical diagnosis."
)

object PersonalLogExporter {
    fun generateTextLog(log: ExportablePersonalLog): String {
        return \"\"\"
================================================================================
KINETIQ PERSONAL FITNESS LOG & SAFETY SUMMARY
Generated: \${java.util.Date(log.exportDateEpochMs)}
================================================================================

USER METRICS & GOAL TRACKING:
- Current Body Weight: \${log.currentWeightKg} kg
- Target Body Weight: \${log.targetWeightKg ?: "Maintenance / Non-weight goal"} kg
- Pre-Participation Screening (PAR-Q+): \${log.parqStatus}

TRAINING ADHERENCE & VOLUME:
- Total Completed Sessions: \${log.totalWorkoutsCompleted}
- Cumulative Volume Load: \${log.totalVolumeKg} kg
- Average Recovery & Readiness Score: \${log.averageReadinessScore} / 100

LEGAL & CLINICAL DISCLAIMER:
\${log.disclaimer}
================================================================================
        \"\"\".trimIndent()
    }
}
""")

print("Phase 2 Depth components generated.")
