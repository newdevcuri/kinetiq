import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# FEATURE: TRAIN
write_file("feature/train/src/main/java/com/kinetiq/fitness/feature/train/TrainScreen.kt", """package com.kinetiq.fitness.feature.train

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kinetiq.fitness.core.designsystem.theme.*

@Composable
fun TrainScreen(
    onStartWorkout: (Int) -> Unit
) {
    var selectedDuration by remember { mutableStateOf(45) }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = KinetiqOledBlack
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 20.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "TRAIN",
                color = KinetiqTextSecondary,
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.5.sp
            )
            Text(
                text = "Today’s Session",
                color = KinetiqTextPrimary,
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))

            Text("Available Time", color = KinetiqTextSecondary, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf(15, 30, 45, 60).forEach { mins ->
                    val isSelected = selectedDuration == mins
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .background(
                                color = if (isSelected) KinetiqExerciseGreenEnd else KinetiqDarkSlate,
                                shape = RoundedCornerShape(12.dp)
                            )
                            .clickable { selectedDuration = mins }
                            .padding(vertical = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = mins.toString() + "m",
                            color = if (isSelected) Color.Black else KinetiqTextPrimary,
                            fontWeight = FontWeight.Bold,
                            fontSize = 15.sp
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(20.dp))

            WorkoutCategoryCard(
                title = "Full Body Double Progression",
                subtitle = "Warmup, Goblet Squats, Push-Ups, RDLs, Core",
                durationMin = selectedDuration,
                tint = KinetiqStrengthTint,
                accent = KinetiqExerciseGreenEnd,
                onClick = { onStartWorkout(selectedDuration) }
            )

            Spacer(modifier = Modifier.height(12.dp))

            WorkoutCategoryCard(
                title = "High-Intensity Interval Conditioning",
                subtitle = "Warmup, 4x4 Intervals, Jumping Jacks, Mobility Cooldown",
                durationMin = selectedDuration,
                tint = KinetiqCardioTint,
                accent = KinetiqMoveRedStart,
                onClick = { onStartWorkout(selectedDuration) }
            )
        }
    }
}

@Composable
private fun WorkoutCategoryCard(
    title: String,
    subtitle: String,
    durationMin: Int,
    tint: Color,
    accent: Color,
    onClick: () -> Unit
) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = tint)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = durationMin.toString() + " MIN / SESSION",
                    color = accent,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 1.sp
                )
                Text("Plan Preview", color = KinetiqTextSecondary, fontSize = 13.sp)
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(title, color = KinetiqTextPrimary, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(subtitle, color = KinetiqTextSecondary, fontSize = 14.sp)
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = onClick,
                colors = ButtonDefaults.buttonColors(containerColor = accent),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("Let's Go", color = Color.Black, fontWeight = FontWeight.Bold)
            }
        }
    }
}
""")

# FEATURE: WORKOUT
write_file("feature/workout/src/main/java/com/kinetiq/fitness/feature/workout/WorkoutPlayerScreen.kt", """package com.kinetiq.fitness.feature.workout

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kinetiq.fitness.core.designsystem.theme.*

@Composable
fun WorkoutPlayerScreen(
    onFinish: () -> Unit
) {
    var currentSet by remember { mutableStateOf(1) }
    var repsLogged by remember { mutableStateOf(10) }
    var weightLogged by remember { mutableStateOf(20.0) }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = KinetiqOledBlack
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("SET " + currentSet + " OF 3", color = KinetiqExerciseGreenEnd, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Text("RIR Target: 2", color = KinetiqTextSecondary, fontSize = 14.sp)
            }

            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Dumbbell Goblet Squat", color = KinetiqTextPrimary, fontSize = 26.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Tempo: 3s Down • 1s Pause • 1s Up", color = KinetiqTextSecondary, fontSize = 14.sp)
                Spacer(modifier = Modifier.height(24.dp))
                
                Box(
                    modifier = Modifier
                        .size(240.dp)
                        .background(KinetiqDarkSlate, RoundedCornerShape(20.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Humanoid Lottie Player", color = KinetiqTextSecondary, fontSize = 14.sp)
                }
            }

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = KinetiqElevatedSurface)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(20.dp),
                    horizontalArrangement = Arrangement.SpaceAround,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("Weight (kg)", color = KinetiqTextSecondary, fontSize = 13.sp)
                        Text(weightLogged.toString(), color = KinetiqTextPrimary, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("Reps", color = KinetiqTextSecondary, fontSize = 13.sp)
                        Text(repsLogged.toString(), color = KinetiqTextPrimary, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }

            Button(
                onClick = {
                    if (currentSet < 3) {
                        currentSet++
                    } else {
                        onFinish()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = KinetiqExerciseGreenEnd),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text(
                    text = if (currentSet < 3) "Complete Set " + currentSet else "Finish Workout",
                    color = Color.Black,
                    fontWeight = FontWeight.Bold,
                    fontSize = 17.sp
                )
            }
        }
    }
}
""")

# FEATURE: LIBRARY & PROGRESS
write_file("feature/library/src/main/java/com/kinetiq/fitness/feature/library/ExerciseLibraryScreen.kt", """package com.kinetiq.fitness.feature.library

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kinetiq.fitness.core.designsystem.theme.*

@Composable
fun ExerciseLibraryScreen() {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = KinetiqOledBlack
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 20.dp)
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            Text("LIBRARY", color = KinetiqTextSecondary, fontSize = 13.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.5.sp)
            Text("Exercise Library", color = KinetiqTextPrimary, fontSize = 32.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(16.dp))

            val exercises = listOf(
                "Bodyweight Air Squat" to "Quadriceps • Bodyweight",
                "Dumbbell Romanian Deadlift" to "Hamstrings • Dumbbell",
                "Standard Push-Up" to "Chest • Bodyweight",
                "Single-Arm Dumbbell Row" to "Latissimus Dorsi • Dumbbell",
                "Front Forearm Plank" to "Core • Bodyweight"
            )

            LazyColumn(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                items(exercises.size) { idx ->
                    val (name, desc) = exercises[idx]
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = KinetiqDarkSlate)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(name, color = KinetiqTextPrimary, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(desc, color = KinetiqTextSecondary, fontSize = 13.sp)
                        }
                    }
                }
            }
        }
    }
}
""")

write_file("feature/progress/src/main/java/com/kinetiq/fitness/feature/progress/ProgressScreen.kt", """package com.kinetiq.fitness.feature.progress

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kinetiq.fitness.core.designsystem.theme.*

@Composable
fun ProgressScreen() {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = KinetiqOledBlack
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 20.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            Text("PROGRESS", color = KinetiqTextSecondary, fontSize = 13.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.5.sp)
            Text("Weight & Forecast", color = KinetiqTextPrimary, fontSize = 32.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(16.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(containerColor = KinetiqDarkSlate)
            ) {
                Column(modifier = Modifier.padding(20.dp)) {
                    Text("Dynamic Hall Model Trajectory", color = KinetiqExerciseGreenEnd, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(6.dp))
                    Text("Target Date: Safe pacing via 1% weekly cap", color = KinetiqTextPrimary, fontSize = 18.sp, fontWeight = FontWeight.SemiBold)
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Current Weight: 84.0 kg • Target: 75.0 kg", color = KinetiqTextSecondary, fontSize = 14.sp)
                }
            }
        }
    }
}
""")

print("Feature screens written successfully.")
