package com.kinetiq.fitness.feature.onboarding

import androidx.compose.foundation.background
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
import com.kinetiq.fitness.core.model.*

@Composable
fun OnboardingScreen(
    onComplete: (UserProfile) -> Unit
) {
    var step by remember { mutableStateOf(1) }
    var location by remember { mutableStateOf(WorkoutLocation.HOME) }
    var selectedEquipment by remember { mutableStateOf(setOf("BODYWEIGHT", "DUMBBELL", "RESISTANCE_BAND")) }
    var goalType by remember { mutableStateOf(GoalType.WEIGHT_LOSS) }
    var targetWeightKg by remember { mutableStateOf(75.0) }
    var currentWeightKg by remember { mutableStateOf(84.0) }
    var heightCm by remember { mutableStateOf(178.0) }
    var ageYears by remember { mutableStateOf(26) }
    var sex by remember { mutableStateOf(BiologicalSex.MALE) }
    var experience by remember { mutableStateOf(TrainingExperience.BEGINNER) }
    var split by remember { mutableStateOf(PreferredSplit.FULL_BODY) }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = KinetiqOledBlack
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    text = "KINETIQ",
                    color = KinetiqExerciseGreenEnd,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 2.sp
                )
                Spacer(modifier = Modifier.height(12.dp))
                
                when (step) {
                    1 -> {
                        Text(
                            text = "Where do you train?",
                            color = KinetiqTextPrimary,
                            fontSize = 28.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "We customize exercise selection around your exact environment and gear.",
                            color = KinetiqTextSecondary,
                            fontSize = 15.sp
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        
                        LocationCard(
                            title = "Home / Home Gym",
                            subtitle = "Bodyweight, dumbbells, bands, or portable equipment",
                            selected = location == WorkoutLocation.HOME,
                            onClick = { location = WorkoutLocation.HOME }
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        LocationCard(
                            title = "Commercial Gym",
                            subtitle = "Full access to racks, barbells, cables, and machines",
                            selected = location == WorkoutLocation.COMMERCIAL_GYM,
                            onClick = { location = WorkoutLocation.COMMERCIAL_GYM }
                        )
                    }
                    2 -> {
                        Text(
                            text = "Available Equipment",
                            color = KinetiqTextPrimary,
                            fontSize = 28.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "Select what you have access to. Kinetiq plans workouts using 100% of these tools.",
                            color = KinetiqTextSecondary,
                            fontSize = 15.sp
                        )
                        Spacer(modifier = Modifier.height(20.dp))

                        val availableList = if (location == WorkoutLocation.HOME) {
                            listOf("BODYWEIGHT", "DUMBBELL", "RESISTANCE_BAND", "KETTLEBELL", "PULL_UP_BAR", "BENCH")
                        } else {
                            listOf("BARBELL", "DUMBBELL", "CABLE_MACHINE", "PULL_UP_BAR", "BENCH", "SQUAT_RACK", "LEG_PRESS")
                        }

                        availableList.forEach { equip ->
                            val isChecked = selectedEquipment.contains(equip)
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 6.dp)
                                    .background(KinetiqDarkSlate, RoundedCornerShape(12.dp))
                                    .padding(16.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(equip.replace("_", " "), color = KinetiqTextPrimary, fontWeight = FontWeight.Medium)
                                Switch(
                                    checked = isChecked,
                                    onCheckedChange = { checked ->
                                        selectedEquipment = if (checked) selectedEquipment + equip else selectedEquipment - equip
                                    }
                                )
                            }
                        }
                    }
                    3 -> {
                        Text(
                            text = "What is your primary goal?",
                            color = KinetiqTextPrimary,
                            fontSize = 28.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(20.dp))
                        GoalCard("Weight Loss", "Burn fat with dynamic metabolic deficit tracking", goalType == GoalType.WEIGHT_LOSS) { goalType = GoalType.WEIGHT_LOSS }
                        GoalCard("Muscle Gain", "Hypertrophy progression with caloric surplus", goalType == GoalType.MUSCLE_GAIN) { goalType = GoalType.MUSCLE_GAIN }
                        GoalCard("Strength", "Progressive overload on key compound lifts", goalType == GoalType.STRENGTH) { goalType = GoalType.STRENGTH }
                        GoalCard("Cardio / Endurance", "Aerobic conditioning, interval sprints, and stamina", goalType == GoalType.ENDURANCE) { goalType = GoalType.ENDURANCE }
                    }
                }
            }

            Button(
                onClick = {
                    if (step < 3) {
                        step++
                    } else {
                        val profile = UserProfile(
                            heightCm = heightCm,
                            currentWeightKg = currentWeightKg,
                            targetWeightKg = targetWeightKg,
                            sex = sex,
                            ageYears = ageYears,
                            activityLevel = ActivityLevel.MODERATELY_ACTIVE,
                            goalType = goalType,
                            workoutLocation = location,
                            equipmentInventory = selectedEquipment.toList(),
                            parqPassed = true,
                            parqDateEpochMs = System.currentTimeMillis(),
                            experienceLevel = experience,
                            preferredSplit = split
                        )
                        onComplete(profile)
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(containerColor = KinetiqExerciseGreenEnd),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text(
                    text = if (step < 3) "Continue" else "Build My Plan",
                    color = Color.Black,
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
private fun LocationCard(title: String, subtitle: String, selected: Boolean, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (selected) KinetiqElevatedSurface else KinetiqDarkSlate
        )
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Text(title, color = if (selected) KinetiqExerciseGreenEnd else KinetiqTextPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(subtitle, color = KinetiqTextSecondary, fontSize = 14.sp)
        }
    }
}

@Composable
private fun GoalCard(title: String, subtitle: String, selected: Boolean, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (selected) KinetiqElevatedSurface else KinetiqDarkSlate
        )
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(title, color = if (selected) KinetiqExerciseGreenEnd else KinetiqTextPrimary, fontWeight = FontWeight.Bold)
            Text(subtitle, color = KinetiqTextSecondary, fontSize = 13.sp)
        }
    }
}
