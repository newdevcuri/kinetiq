package com.kinetiq.fitness

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
