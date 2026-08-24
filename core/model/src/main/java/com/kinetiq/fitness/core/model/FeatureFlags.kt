package com.kinetiq.fitness.core.model

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
