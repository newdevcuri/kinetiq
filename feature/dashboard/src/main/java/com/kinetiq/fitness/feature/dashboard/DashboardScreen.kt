package com.kinetiq.fitness.feature.dashboard

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.kinetiq.fitness.core.designsystem.components.ActivityRingsCanvas
import com.kinetiq.fitness.core.designsystem.theme.*

@Composable
fun DashboardScreen(
    moveCalories: Int = 420,
    moveGoal: Int = 600,
    exerciseMinutes: Int = 35,
    exerciseGoal: Int = 30,
    standHours: Int = 8,
    standGoal: Int = 12,
    readinessScore: Int = 85,
    readinessNote: String = "Balanced recovery — ready for your standard planned session."
) {
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
                text = "SUMMARY",
                color = KinetiqTextSecondary,
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.5.sp
            )
            Text(
                text = "Today",
                color = KinetiqTextPrimary,
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(16.dp))

            // Activity Rings Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(24.dp),
                colors = CardDefaults.cardColors(containerColor = KinetiqDarkSlate)
            ) {
                Row(
                    modifier = Modifier.padding(20.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    ActivityRingsCanvas(
                        moveProgress = moveCalories.toFloat() / moveGoal.toFloat(),
                        exerciseProgress = exerciseMinutes.toFloat() / exerciseGoal.toFloat(),
                        standProgress = standHours.toFloat() / standGoal.toFloat(),
                        size = 140.dp,
                        strokeWidth = 14.dp
                    )
                    Spacer(modifier = Modifier.width(20.dp))
                    Column {
                        MetricRow("Move", "$moveCalories / $moveGoal CAL", KinetiqMoveRedStart)
                        Spacer(modifier = Modifier.height(12.dp))
                        MetricRow("Exercise", "$exerciseMinutes / $exerciseGoal MIN", KinetiqExerciseGreenEnd)
                        Spacer(modifier = Modifier.height(12.dp))
                        MetricRow("Stand", "$standHours / $standGoal HRS", KinetiqStandCyanStart)
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Readiness Banner Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = KinetiqElevatedSurface)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Readiness Score", color = KinetiqTextPrimary, fontWeight = FontWeight.Bold)
                        Text("$readinessScore / 100", color = KinetiqExerciseGreenEnd, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.height(6.dp))
                    Text(readinessNote, color = KinetiqTextSecondary, fontSize = 13.sp)
                }
            }
        }
    }
}

@Composable
private fun MetricRow(label: String, value: String, color: Color) {
    Column {
        Text(label, color = color, fontSize = 13.sp, fontWeight = FontWeight.Bold)
        Text(value, color = KinetiqTextPrimary, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
    }
}
