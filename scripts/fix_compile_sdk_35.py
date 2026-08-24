import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Updated: {rel_path}")

# 1. libs.versions.toml
write_file("gradle/libs.versions.toml", """[versions]
agp = "8.6.0"
kotlin = "2.0.20"
compose-bom = "2024.09.00"
core-ktx = "1.13.1"
lifecycle = "2.8.5"
activity-compose = "1.9.2"
navigation-compose = "2.8.0"
room = "2.6.1"
health-connect = "1.1.0-alpha10"
lottie = "6.4.1"
vico = "2.0.0-alpha.28"
work = "2.9.1"
coroutines = "1.8.1"
turbine = "1.1.0"
junit = "4.13.2"
junit-ext = "1.2.1"
espresso = "3.6.1"
robolectric = "4.13"
assertj = "3.26.0"
material3 = "1.3.0"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "core-ktx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycle" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activity-compose" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigation-compose" }

# Compose BOM & UI
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-compose-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-compose-animation = { group = "androidx.compose.animation", name = "animation" }
androidx-compose-foundation = { group = "androidx.compose.foundation", name = "foundation" }

# Room
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
androidx-room-testing = { group = "androidx.room", name = "room-testing", version.ref = "room" }

# Health Connect
androidx-health-connect = { group = "androidx.health.connect", name = "connect-client", version.ref = "health-connect" }

# Lottie & Charting
airbnb-lottie-compose = { group = "com.airbnb.android", name = "lottie-compose", version.ref = "lottie" }
vico-compose-m3 = { group = "com.patrykandpatrick.vico", name = "compose-m3", version.ref = "vico" }

# WorkManager
androidx-work-runtime-ktx = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "work" }
androidx-work-testing = { group = "androidx.work", name = "work-testing", version.ref = "work" }

# Coroutines
kotlinx-coroutines-core = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core", version.ref = "coroutines" }
kotlinx-coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }
kotlinx-coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "coroutines" }

# Testing
junit = { group = "junit", name = "junit", version.ref = "junit" }
androidx-junit = { group = "androidx.test.ext", name = "junit", version.ref = "junit-ext" }
androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version.ref = "espresso" }
cashapp-turbine = { group = "app.cash.turbine", name = "turbine", version.ref = "turbine" }
robolectric = { group = "org.robolectric", name = "robolectric", version.ref = "robolectric" }
assertj-core = { group = "org.assertj", name = "assertj-core", version.ref = "assertj" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
android-library = { id = "com.android.library", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
""")

# 2. Helper to generate build.gradle.kts with compileSdk 35
def make_module_build(path, is_app=False, deps=""):
    plugin_header = """plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}""" if is_app else """plugins {
    alias(libs.plugins.android.library)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}"""
    
    app_specific = """
    defaultConfig {
        applicationId = "com.kinetiq.fitness"
        minSdk = 28
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
        debug {
            isMinifyEnabled = false
        }
    }
""" if is_app else """
    defaultConfig {
        minSdk = 28
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        consumerProguardFiles("consumer-rules.pro")
    }
"""

    content = f"""{plugin_header}

android {{
    namespace = "{"com.kinetiq.fitness" if is_app else "com.kinetiq.fitness." + path.replace("/", ".").replace(":", ".")}"
    compileSdk = 35
{app_specific}
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

make_module_build("app", is_app=True, deps="""    implementation(project(":core:designsystem"))
    implementation(project(":core:database"))
    implementation(project(":core:model"))
    implementation(project(":core:data"))
    implementation(project(":core:engine"))
    implementation(project(":core:healthconnect"))
    implementation(project(":feature:onboarding"))
    implementation(project(":feature:dashboard"))
    implementation(project(":feature:train"))
    implementation(project(":feature:workout"))
    implementation(project(":feature:library"))
    implementation(project(":feature:progress"))

    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.navigation.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
""")

make_module_build("core/designsystem", is_app=False, deps="""    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.animation)
    implementation(libs.androidx.compose.foundation)
    implementation(libs.airbnb.lottie.compose)
""")

make_module_build("core/model", is_app=False, deps="""    implementation(libs.kotlinx.coroutines.core)
""")

make_module_build("core/database", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    testImplementation(libs.androidx.room.testing)
    testImplementation(libs.junit)
    testImplementation(libs.robolectric)
""")

make_module_build("core/engine", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(libs.kotlinx.coroutines.core)
    testImplementation(libs.junit)
    testImplementation(libs.assertj.core)
""")

make_module_build("core/data", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:database"))
    implementation(project(":core:engine"))
    implementation(libs.kotlinx.coroutines.core)
""")

make_module_build("core/healthconnect", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(libs.androidx.health.connect)
    implementation(libs.kotlinx.coroutines.core)
""")

make_module_build("feature/onboarding", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:engine"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.navigation.compose)
""")

make_module_build("feature/dashboard", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
""")

make_module_build("feature/train", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:engine"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
""")

make_module_build("feature/workout", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.airbnb.lottie.compose)
""")

make_module_build("feature/library", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.airbnb.lottie.compose)
""")

make_module_build("feature/progress", is_app=False, deps="""    implementation(project(":core:model"))
    implementation(project(":core:designsystem"))
    implementation(project(":core:engine"))
    implementation(project(":core:data"))
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.material3)
    implementation(libs.vico.compose.m3)
""")

print("All build.gradle.kts files updated to compileSdk 35 with jvmToolchain(17).")
