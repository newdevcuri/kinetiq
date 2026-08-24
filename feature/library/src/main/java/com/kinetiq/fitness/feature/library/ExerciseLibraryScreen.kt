package com.kinetiq.fitness.feature.library

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
