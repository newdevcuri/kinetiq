package com.kinetiq.fitness.feature.workout

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
