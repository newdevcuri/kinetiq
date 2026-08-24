package com.kinetiq.fitness.core.designsystem.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.kinetiq.fitness.core.designsystem.motion.KinetiqMotion
import com.kinetiq.fitness.core.designsystem.theme.KinetiqExerciseGreenEnd
import com.kinetiq.fitness.core.designsystem.theme.KinetiqExerciseGreenStart
import com.kinetiq.fitness.core.designsystem.theme.KinetiqMoveRedEnd
import com.kinetiq.fitness.core.designsystem.theme.KinetiqMoveRedStart
import com.kinetiq.fitness.core.designsystem.theme.KinetiqStandAzureEnd
import com.kinetiq.fitness.core.designsystem.theme.KinetiqStandCyanStart

/**
 * High-performance 3-Ring Activity Component using Canvas drawArc with sweepGradient.
 * Supports TalkBack merged semantics and Reduce-Motion zero-duration rendering.
 */
@Composable
fun ActivityRingsCanvas(
    moveProgress: Float,      // 0.0 to 1.0+ (Move / Active Cal)
    exerciseProgress: Float,  // 0.0 to 1.0+ (Exercise / Min)
    standProgress: Float,     // 0.0 to 1.0+ (Stand / Recovery)
    modifier: Modifier = Modifier,
    size: Dp = 160.dp,
    strokeWidth: Dp = 16.dp,
    gap: Dp = 4.dp,
    reduceMotion: Boolean = false
) {
    val moveAnim = remember { Animatable(if (reduceMotion) moveProgress else 0f) }
    val exerciseAnim = remember { Animatable(if (reduceMotion) exerciseProgress else 0f) }
    val standAnim = remember { Animatable(if (reduceMotion) standProgress else 0f) }

    LaunchedEffect(moveProgress, exerciseProgress, standProgress, reduceMotion) {
        if (reduceMotion) {
            moveAnim.snapTo(moveProgress)
            exerciseAnim.snapTo(exerciseProgress)
            standAnim.snapTo(standProgress)
        } else {
            moveAnim.animateTo(moveProgress, KinetiqMotion.DefaultSpring)
            exerciseAnim.animateTo(exerciseProgress, KinetiqMotion.DefaultSpring)
            standAnim.animateTo(standProgress, KinetiqMotion.DefaultSpring)
        }
    }

    val accessibilityText = "Activity summary: Move ${(moveProgress * 100).toInt()} percent, Exercise ${(exerciseProgress * 100).toInt()} percent, Stand ${(standProgress * 100).toInt()} percent."

    Canvas(
        modifier = modifier
            .size(size)
            .semantics { contentDescription = accessibilityText }
    ) {
        val strokePx = strokeWidth.toPx()
        val gapPx = gap.toPx()
        val center = Offset(size.toPx() / 2f, size.toPx() / 2f)

        // 1. Move Ring (Outer)
        val r1 = (size.toPx() / 2f) - (strokePx / 2f)
        drawRing(
            center = center,
            radius = r1,
            strokePx = strokePx,
            progress = moveAnim.value,
            bgTint = Color(0x33FF2D55),
            gradient = listOf(KinetiqMoveRedStart, KinetiqMoveRedEnd)
        )

        // 2. Exercise Ring (Middle)
        val r2 = r1 - strokePx - gapPx
        drawRing(
            center = center,
            radius = r2,
            strokePx = strokePx,
            progress = exerciseAnim.value,
            bgTint = Color(0x3330D158),
            gradient = listOf(KinetiqExerciseGreenStart, KinetiqExerciseGreenEnd)
        )

        // 3. Stand/Recovery Ring (Inner)
        val r3 = r2 - strokePx - gapPx
        drawRing(
            center = center,
            radius = r3,
            strokePx = strokePx,
            progress = standAnim.value,
            bgTint = Color(0x3300F0FF),
            gradient = listOf(KinetiqStandCyanStart, KinetiqStandAzureEnd)
        )
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawRing(
    center: Offset,
    radius: Float,
    strokePx: Float,
    progress: Float,
    bgTint: Color,
    gradient: List<Color>
) {
    val topLeft = Offset(center.x - radius, center.y - radius)
    val ringSize = Size(radius * 2f, radius * 2f)

    // Background track
    drawArc(
        color = bgTint,
        startAngle = 0f,
        sweepAngle = 360f,
        useCenter = false,
        topLeft = topLeft,
        size = ringSize,
        style = Stroke(width = strokePx, cap = StrokeCap.Round)
    )

    // Foreground active arc
    val sweep = progress.coerceAtLeast(0f) * 360f
    if (sweep > 0f) {
        drawArc(
            brush = Brush.sweepGradient(
                colors = gradient,
                center = center
            ),
            startAngle = -90f,
            sweepAngle = sweep,
            useCenter = false,
            topLeft = topLeft,
            size = ringSize,
            style = Stroke(width = strokePx, cap = StrokeCap.Round)
        )
    }
}
