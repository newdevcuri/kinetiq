package com.kinetiq.fitness.feature.train

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
