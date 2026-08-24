package com.kinetiq.fitness.core.engine

data class ParsedVoiceLog(
    val reps: Int?,
    val weightKg: Double?,
    val command: String
)

object VoiceWorkoutBuddy {
    private val REPS_REGEX = Regex("(\\d+)\\s*(?:reps|rep)", RegexOption.IGNORE_CASE)
    private val WEIGHT_REGEX = Regex("(\\d+(?:\\.\\d+)?)\\s*(?:kg|kilos|kilo|lbs|pounds)", RegexOption.IGNORE_CASE)

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
