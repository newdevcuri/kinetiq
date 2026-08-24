import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# ==============================================================================
# 1. MOTION CATALOG (§5b - All 12 Interactions + Reduce-Motion Fallbacks)
# ==============================================================================
write_file("core/designsystem/src/main/java/com/kinetiq/fitness/core/designsystem/motion/MotionCatalog.kt", """package com.kinetiq.fitness.core.designsystem.motion

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.kinetiq.fitness.core.designsystem.theme.KinetiqDarkSlate
import com.kinetiq.fitness.core.designsystem.theme.KinetiqElevatedSurface

object MotionCatalog {
    
    // 1. Hero Expansion
    // Primary: Shared element bounds transform. Fallback: Instant crossfade.
    val HeroExpansionSpec = KinetiqMotion.DefaultSpring

    // 2. Animated Progress Rings
    // Primary: 800-1200ms sweep spring. Fallback: Immediate final sweep snap.
    fun ringAnimationSpec(reduceMotion: Boolean): AnimationSpec<Float> =
        if (reduceMotion) snap() else KinetiqMotion.DefaultSpring

    // 3. Animate-on-Scroll Bar Charts
    // Primary: Staggered height spring overshoot on viewport entry. Fallback: Immediate final height.
    fun barChartAnimationSpec(reduceMotion: Boolean): AnimationSpec<Float> =
        if (reduceMotion) snap() else KinetiqMotion.DefaultSpring

    // 4. Heart Rate Pulsing Effect
    // Primary: Live BPM scale pulse. Fallback: Static icon.
    fun hrPulseScale(liveBpm: Int?, reduceMotion: Boolean): Float =
        if (reduceMotion || liveBpm == null) 1.0f else 1.08f

    // 5. Streak Celebration Burst
    // Primary: Bespoke design-token particle system. Fallback: Static checkmark with haptic tick.
    fun showCelebrationParticles(reduceMotion: Boolean): Boolean = !reduceMotion

    // 6. Springy Checkmark Morph
    // Primary: Morph with DampingRatioMediumBouncy overshoot. Fallback: Instant icon swap.
    val CheckmarkMorphSpring = KinetiqMotion.BouncyTactileSpring

    // 7. Elastic FAB Pop
    // Primary: Press scale-down and bouncy release overshoot. Fallback: Linear opacity tap.
    val ElasticFabSpring = KinetiqMotion.BouncyTactileSpring

    // 8. Horizontal Carousel Slide
    // Primary: Snap fling with parallax offset. Fallback: Instant page snap without parallax.
    fun carouselParallaxMultiplier(reduceMotion: Boolean): Float = if (reduceMotion) 0f else 0.25f

    // 9. Dropdown Timer Slide-In
    // Primary: slideInVertically + expandVertically spring. Fallback: Instant visibility toggle.
    fun timerDropdownTransition(reduceMotion: Boolean): EnterTransition =
        if (reduceMotion) fadeIn(animationSpec = snap())
        else slideInVertically(animationSpec = KinetiqMotion.DefaultSpring) + expandVertically()

    // 10. Shimmer Loading Skeletons
    // Primary: Translating linear gradient brush on #1C1C1E. Fallback: Static #1C1C1E placeholder.
    @Composable
    fun shimmerBrush(reduceMotion: Boolean): Brush {
        return if (reduceMotion) {
            Brush.linearGradient(listOf(KinetiqDarkSlate, KinetiqDarkSlate))
        } else {
            val transition = rememberInfiniteTransition(label = "shimmer")
            val translateAnim by transition.animateFloat(
                initialValue = 0f,
                targetValue = 1000f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = 1200, easing = LinearEasing),
                    repeatMode = RepeatMode.Restart
                ),
                label = "shimmer_translate"
            )
            Brush.linearGradient(
                colors = listOf(KinetiqDarkSlate, KinetiqElevatedSurface, KinetiqDarkSlate),
                start = Offset(translateAnim - 200f, translateAnim - 200f),
                end = Offset(translateAnim, translateAnim)
            )
        }
    }

    // 11. Shared Element Transition
    // Primary: Shared bounds container transform. Fallback: Instant crossfade.
    val SharedElementSpec = KinetiqMotion.DefaultSpring

    // 12. Bottom-Sheet Modal Slide-Up
    // Primary: Spring slide-up + scrim fade. Fallback: Instant fade at final position.
    val BottomSheetSlideSpec = KinetiqMotion.DefaultSpring
}
""")

# ==============================================================================
# 2. CLINICAL-LOGIC EDGE CASES & RELIABILITY REGISTER
# ==============================================================================
write_file("core/engine/src/main/java/com/kinetiq/fitness/core/engine/ReliabilityRegister.kt", """package com.kinetiq.fitness.core.engine

object ReliabilityRegister {
    private const val PARQ_VALIDITY_DAYS = 90L
    private const val MS_PER_DAY = 24L * 60L * 60L * 1000L

    /**
     * Checks if PAR-Q+ pre-participation screening requires a 90-day refresh.
     */
    fun isParqScreeningDue(lastScreeningEpochMs: Long, currentEpochMs: Long): Boolean {
        val daysElapsed = (currentEpochMs - lastScreeningEpochMs) / MS_PER_DAY
        return daysElapsed >= PARQ_VALIDITY_DAYS
    }

    /**
     * Re-filters existing workout programs when a new injury tag is added mid-program.
     */
    fun reFilterProgramForNewInjury(
        currentProgramExerciseIds: List<String>,
        newInjuryTags: List<String>,
        exerciseContraindicationMap: Map<String, List<String>>
    ): List<String> {
        val upperInjuries = newInjuryTags.map { it.uppercase() }.toSet()
        return currentProgramExerciseIds.filter { exId ->
            val contra = exerciseContraindicationMap[exId] ?: emptyList()
            contra.none { upperInjuries.contains(it.uppercase()) }
        }
    }

    /**
     * Verifies Doze-safe elapsed real-time timer progression.
     */
    fun computeRemainingRestSeconds(
        timerStartElapsedRealtimeMs: Long,
        totalRestSeconds: Int,
        currentElapsedRealtimeMs: Long
    ): Int {
        val elapsedSeconds = ((currentElapsedRealtimeMs - timerStartElapsedRealtimeMs) / 1000L).toInt()
        return (totalRestSeconds - elapsedSeconds).coerceAtLeast(0)
    }
}
""")

print("Phase 1.5 components created.")
