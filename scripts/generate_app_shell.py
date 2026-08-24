import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# 1. AndroidManifest.xml
write_file("app/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Health Connect Permissions -->
    <uses-permission android:name="android.permission.health.READ_STEPS" />
    <uses-permission android:name="android.permission.health.READ_HEART_RATE" />
    <uses-permission android:name="android.permission.health.READ_SLEEP" />
    <uses-permission android:name="android.permission.health.WRITE_EXERCISE" />

    <!-- Optional Hardware & Sensor Permissions -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:name=".KinetiqApplication"
        android:allowBackup="false"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="false"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.Kinetiq">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Kinetiq">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
""")

# 2. XML Resources
write_file("app/src/main/res/xml/data_extraction_rules.xml", """<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
        <exclude domain="sharedpref" path="." />
        <exclude domain="database" path="." />
    </cloud-backup>
    <device-transfer>
        <exclude domain="sharedpref" path="." />
        <exclude domain="database" path="." />
    </device-transfer>
</data-extraction-rules>
""")

write_file("app/src/main/res/values/strings.xml", """<resources>
    <string name="app_name">Kinetiq</string>
</resources>
""")

write_file("app/src/main/res/values/colors.xml", """<resources>
    <color name="black">#000000</color>
    <color name="dark_slate">#1C1C1E</color>
    <color name="accent_green">#30D158</color>
</resources>
""")

write_file("app/src/main/res/values/themes.xml", """<resources>
    <style name="Theme.Kinetiq" parent="android:Theme.Material.NoActionBar">
        <item name="android:windowBackground">@color/black</item>
        <item name="android:statusBarColor">@color/black</item>
        <item name="android:navigationBarColor">@color/black</item>
    </style>
</resources>
""")

write_file("app/src/main/res/drawable/ic_launcher_background.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#000000"
        android:pathData="M0,0h108v108h-108z" />
</vector>
""")

write_file("app/src/main/res/drawable/ic_launcher_foreground.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:strokeColor="#30D158"
        android:strokeWidth="8"
        android:strokeLineCap="round"
        android:pathData="M 54,24 A 30,30 0 1,1 24,54" />
</vector>
""")

write_file("app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
""")

# 3. Application Class & MainActivity
write_file("app/src/main/java/com/kinetiq/fitness/KinetiqApplication.kt", """package com.kinetiq.fitness

import android.app.Application

class KinetiqApplication : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
""")

write_file("app/src/main/java/com/kinetiq/fitness/MainActivity.kt", """package com.kinetiq.fitness

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.kinetiq.fitness.core.designsystem.theme.KinetiqOledBlack
import com.kinetiq.fitness.core.designsystem.theme.KinetiqFrostedNav
import com.kinetiq.fitness.core.designsystem.theme.KinetiqExerciseGreenEnd
import com.kinetiq.fitness.core.designsystem.theme.KinetiqTextSecondary
import com.kinetiq.fitness.feature.dashboard.DashboardScreen
import com.kinetiq.fitness.feature.library.ExerciseLibraryScreen
import com.kinetiq.fitness.feature.onboarding.OnboardingScreen
import com.kinetiq.fitness.feature.progress.ProgressScreen
import com.kinetiq.fitness.feature.train.TrainScreen
import com.kinetiq.fitness.feature.workout.WorkoutPlayerScreen

enum class AppNavTab {
    SUMMARY,
    TRAIN,
    LIBRARY,
    PROGRESS
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            var isOnboardingCompleted by remember { mutableStateOf(false) }
            var currentTab by remember { mutableStateOf(AppNavTab.SUMMARY) }
            var activeWorkoutDuration by remember { mutableStateOf<Int?>(null) }

            Surface(
                modifier = Modifier.fillMaxSize(),
                color = KinetiqOledBlack
            ) {
                if (!isOnboardingCompleted) {
                    OnboardingScreen(
                        onComplete = { _ ->
                            isOnboardingCompleted = true
                        }
                    )
                } else if (activeWorkoutDuration != null) {
                    WorkoutPlayerScreen(
                        onFinish = {
                            activeWorkoutDuration = null
                        }
                    )
                } else {
                    Scaffold(
                        bottomBar = {
                            NavigationBar(
                                containerColor = KinetiqFrostedNav,
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                NavigationBarItem(
                                    selected = currentTab == AppNavTab.SUMMARY,
                                    onClick = { currentTab = AppNavTab.SUMMARY },
                                    label = { Text("Summary") },
                                    icon = { Text("⭕", color = if (currentTab == AppNavTab.SUMMARY) KinetiqExerciseGreenEnd else KinetiqTextSecondary) }
                                )
                                NavigationBarItem(
                                    selected = currentTab == AppNavTab.TRAIN,
                                    onClick = { currentTab = AppNavTab.TRAIN },
                                    label = { Text("Train") },
                                    icon = { Text("⚡", color = if (currentTab == AppNavTab.TRAIN) KinetiqExerciseGreenEnd else KinetiqTextSecondary) }
                                )
                                NavigationBarItem(
                                    selected = currentTab == AppNavTab.LIBRARY,
                                    onClick = { currentTab = AppNavTab.LIBRARY },
                                    label = { Text("Library") },
                                    icon = { Text("📚", color = if (currentTab == AppNavTab.LIBRARY) KinetiqExerciseGreenEnd else KinetiqTextSecondary) }
                                )
                                NavigationBarItem(
                                    selected = currentTab == AppNavTab.PROGRESS,
                                    onClick = { currentTab = AppNavTab.PROGRESS },
                                    label = { Text("Progress") },
                                    icon = { Text("📈", color = if (currentTab == AppNavTab.PROGRESS) KinetiqExerciseGreenEnd else KinetiqTextSecondary) }
                                )
                            }
                        }
                    ) { innerPadding ->
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(innerPadding)
                        ) {
                            when (currentTab) {
                                AppNavTab.SUMMARY -> DashboardScreen()
                                AppNavTab.TRAIN -> TrainScreen(onStartWorkout = { duration -> activeWorkoutDuration = duration })
                                AppNavTab.LIBRARY -> ExerciseLibraryScreen()
                                AppNavTab.PROGRESS -> ProgressScreen()
                            }
                        }
                    }
                }
            }
        }
    }
}
""")

# 4. GitHub Actions CI Workflow
write_file(".github/workflows/android.yml", """name: Android CI Build & Test

on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]
  workflow_dispatch:

jobs:
  build:
    name: Build & Verify Android Application
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          gradle-version: '8.7'

      - name: Make Gradle Wrapper Executable
        run: chmod +x gradlew

      - name: Run Import Integrity Linter
        run: python3 scripts/check_import_integrity.py

      - name: Run Verification Test Suites
        run: |
          python3 scripts/test_phase_0.py
          python3 scripts/test_phase_1.py
          python3 scripts/test_phase_1_5.py
          python3 scripts/test_phase_2.py
          python3 scripts/test_phase_3.py
          python3 scripts/reverify_all_phases.py

      - name: Build Debug APK with Gradle
        run: ./gradlew assembleDebug --stacktrace --no-daemon

      - name: Run Android Unit Tests with Gradle
        run: ./gradlew testDebugUnitTest --stacktrace --no-daemon

      - name: Upload Debug APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: kinetiq-debug-apk
          path: app/build/outputs/apk/debug/*.apk
          if-no-files-found: ignore
          retention-days: 7
""")

print("App shell and GitHub Workflow generated.")
