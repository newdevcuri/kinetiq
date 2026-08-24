package com.kinetiq.fitness.core.data

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
        return """
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
        """.trimIndent()
    }
}
