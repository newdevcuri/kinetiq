package com.kinetiq.fitness.core.designsystem.motion

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
        else slideInVertically(
            animationSpec = spring(
                dampingRatio = Spring.DampingRatioNoBouncy,
                stiffness = Spring.StiffnessMedium
            )
        ) + expandVertically()

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
