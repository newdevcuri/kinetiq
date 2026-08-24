package com.kinetiq.fitness.core.data

import java.util.Date

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
        val targetWeightStr = if (log.targetWeightKg != null) "${log.targetWeightKg} kg" else "Maintenance / Non-weight goal"
        return """
================================================================================
KINETIQ PERSONAL FITNESS LOG & SAFETY SUMMARY
Generated: ${Date(log.exportDateEpochMs)}
================================================================================

USER METRICS & GOAL TRACKING:
- Current Body Weight: ${log.currentWeightKg} kg
- Target Body Weight: $targetWeightStr
- Pre-Participation Screening (PAR-Q+): ${log.parqStatus}

TRAINING ADHERENCE & VOLUME:
- Total Completed Sessions: ${log.totalWorkoutsCompleted}
- Cumulative Volume Load: ${log.totalVolumeKg} kg
- Average Recovery & Readiness Score: ${log.averageReadinessScore} / 100

LEGAL & CLINICAL DISCLAIMER:
${log.disclaimer}
================================================================================
        """.trimIndent()
    }
}
