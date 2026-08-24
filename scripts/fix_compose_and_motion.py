import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Updated: {rel_path}")

# 1. Fix MotionCatalog.kt and KinetiqMotion.kt
write_file("core/designsystem/src/main/java/com/kinetiq/fitness/core/designsystem/motion/KinetiqMotion.kt", """package com.kinetiq.fitness.core.designsystem.motion

import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.SpringSpec
import androidx.compose.animation.core.spring

object KinetiqMotion {
    val DefaultSpring: SpringSpec<Float> = spring(
        dampingRatio = Spring.DampingRatioNoBouncy,
        stiffness = Spring.StiffnessMedium
    )

    val BouncyTactileSpring: SpringSpec<Float> = spring(
        dampingRatio = Spring.DampingRatioMediumBouncy,
        stiffness = Spring.StiffnessMediumLow
    )

    fun <T> defaultSpring() = spring<T>(
        dampingRatio = Spring.DampingRatioNoBouncy,
        stiffness = Spring.StiffnessMedium
    )
}
""")

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
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import com.kinetiq.fitness.core.designsystem.theme.KinetiqDarkSlate
import com.kinetiq.fitness.core.designsystem.theme.KinetiqElevatedSurface

object MotionCatalog {
    
    // 1. Hero Expansion
    val HeroExpansionSpec = KinetiqMotion.DefaultSpring

    // 2. Animated Progress Rings
    fun ringAnimationSpec(reduceMotion: Boolean): AnimationSpec<Float> =
        if (reduceMotion) snap() else KinetiqMotion.DefaultSpring

    // 3. Animate-on-Scroll Bar Charts
    fun barChartAnimationSpec(reduceMotion: Boolean): AnimationSpec<Float> =
        if (reduceMotion) snap() else KinetiqMotion.DefaultSpring

    // 4. Heart Rate Pulsing Effect
    fun hrPulseScale(liveBpm: Int?, reduceMotion: Boolean): Float =
        if (reduceMotion || liveBpm == null) 1.0f else 1.08f

    // 5. Streak Celebration Burst
    fun showCelebrationParticles(reduceMotion: Boolean): Boolean = !reduceMotion

    // 6. Springy Checkmark Morph
    val CheckmarkMorphSpring = KinetiqMotion.BouncyTactileSpring

    // 7. Elastic FAB Pop
    val ElasticFabSpring = KinetiqMotion.BouncyTactileSpring

    // 8. Horizontal Carousel Slide
    fun carouselParallaxMultiplier(reduceMotion: Boolean): Float = if (reduceMotion) 0f else 0.25f

    // 9. Dropdown Timer Slide-In (IntOffset Spring Spec)
    fun timerDropdownTransition(reduceMotion: Boolean): EnterTransition =
        if (reduceMotion) fadeIn(animationSpec = snap())
        else slideInVertically(animationSpec = spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = Spring.StiffnessMedium)) + expandVertically()

    // 10. Shimmer Loading Skeletons
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
    val SharedElementSpec = KinetiqMotion.DefaultSpring

    // 12. Bottom-Sheet Modal Slide-Up
    val BottomSheetSlideSpec = KinetiqMotion.DefaultSpring
}
""")

# 2. Update Module Build Files
# Helper for non-compose library module
def make_pure_library_build(path, deps=""):
    content = f"""plugins {{
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
}}

android {{
    namespace = "com.kinetiq.fitness.{path.replace('/', '.').replace(':', '.')}"
    compileSdk = 35

    defaultConfig {{
        minSdk = 28
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        consumerProguardFiles("consumer-rules.pro")
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
}}

kotlin {{
    jvmToolchain(17)
}}

dependencies {{
{deps}
}}
"""
    write_file(f"{path}/build.gradle.kts", content)

# Helper for compose library module
def make_compose_library_build(path, deps=""):
    content = f"""plugins {{
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}}

android {{
    namespace = "com.kinetiq.fitness.{path.replace('/', '.').replace(':', '.')}"
    compileSdk = 35

    defaultConfig {{
        minSdk = 28
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        consumerProguardFiles("consumer-rules.pro")
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}
    buildFeatures {{
        compose = true
    }}
}}

kotlin {{
    jvmToolchain(17)
}}

dependencies {{
{deps}
}}
"""
    write_file(f"{path}/build.gradle.kts", content)

# NON-COMPOSE MODULES:
make_pure_library_build("core/model", """    implementation(libs.kotlinx.coroutines.core)
""")

make_pure_library_build("core/database", """    implementation(project(":core:model"))
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    testImplementation(libs.androidx.room.testing)
    testImplementation(libs.junit)
    testImplementation(libs.robolectric)
""")

make_pure_library_build("core/engine", """    implementation(project(":core:model"))
    implementation(libs.kotlinx.coroutines.core)
    testImplementation(libs.junit)
    testImplementation(libs.assertj.core)
""")

make_pure_library_build("core/data", """    implementation(project(":core:model"))
    implementation(project(":core:database"))
    implementation(project(":core:engine"))
    implementation(libs.kotlinx.coroutines.core)
""")

make_pure_library_build("core/healthconnect", """    implementation(project(":core:model"))
    implementation(libs.androidx.health.connect)
    implementation(libs.kotlinx.coroutines.core)
""")

# COMPOSE MODULES:
make_compose_library_build("core/designsystem", """    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.animation)
    implementation(libs.androidx.compose.foundation)
    implementation(libs.airbnb.lottie.compose)
""")

make_compose_library_build("feature/onboarding", """    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:engine"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.navigation.compose)
""")

make_compose_library_build("feature/dashboard", """    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
""")

make_compose_library_build("feature/train", """    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:engine"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
""")

make_compose_library_build("feature/workout", """    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.airbnb.lottie.compose)
""")

make_compose_library_build("feature/library", """    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.airbnb.lottie.compose)
""")

make_compose_library_build("feature/progress", """    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:engine"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.vico.compose.m3)
""")

print("Compose plugins and motion types successfully fixed.")
