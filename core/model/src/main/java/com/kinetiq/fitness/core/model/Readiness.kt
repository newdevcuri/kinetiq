package com.kinetiq.fitness.core.model

data class DailyReadinessLog(
    val dateEpochDay: Long,
    val sleepMinutes: Int? = null,
    val hrBaselineDeltaBpm: Double? = null,
    val selfReportedSorenessScore: Int? = null,
    val computedBand: ReadinessBand,
    val adjustmentApplied: String
)
