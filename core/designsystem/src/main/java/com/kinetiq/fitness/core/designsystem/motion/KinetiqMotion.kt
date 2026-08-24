package com.kinetiq.fitness.core.designsystem.motion

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring

object KinetiqMotion {
    // App-wide restrained default spring (PRD §27 / Build Spec §5)
    val DefaultSpring = spring<Float>(
        dampingRatio = Spring.DampingRatioNoBouncy,
        stiffness = Spring.StiffnessMedium
    )

    // Explicit sanctioned exception for Checkmark Morph & Elastic FAB Pop (Build Spec §5b #6, #7, DEC-003)
    val BouncyTactileSpring = spring<Float>(
        dampingRatio = Spring.DampingRatioMediumBouncy,
        stiffness = Spring.StiffnessMediumLow
    )
}
