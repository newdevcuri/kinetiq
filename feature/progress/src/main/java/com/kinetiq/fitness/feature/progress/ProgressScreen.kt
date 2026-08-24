package com.kinetiq.fitness.feature.progress

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
