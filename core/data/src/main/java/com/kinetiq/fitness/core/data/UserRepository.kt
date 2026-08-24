package com.kinetiq.fitness.core.data

import com.kinetiq.fitness.core.database.UserDao
import com.kinetiq.fitness.core.database.UserEntity
import com.kinetiq.fitness.core.model.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class UserRepository(private val userDao: UserDao) {
    fun getUserProfileFlow(): Flow<UserProfile?> {
        return userDao.getUserFlow().map { entity ->
            entity?.let {
                UserProfile(
                    id = it.id,
                    heightCm = it.heightCm,
                    currentWeightKg = it.currentWeightKg,
                    targetWeightKg = it.targetWeightKg,
                    sex = BiologicalSex.valueOf(it.sex),
                    ageYears = it.ageYears,
                    activityLevel = ActivityLevel.valueOf(it.activityLevel),
                    goalType = GoalType.valueOf(it.goalType),
                    goalMode = it.goalMode?.let { m -> GoalMode.valueOf(m) },
                    pacePreset = it.pacePreset,
                    targetDateEpochMs = it.targetDateEpochMs,
                    target1RmKg = it.target1RmKg,
                    targetDurationSeconds = it.targetDurationSeconds,
                    targetDistanceMeters = it.targetDistanceMeters,
                    workoutLocation = WorkoutLocation.valueOf(it.workoutLocation),
                    equipmentInventory = it.equipmentInventoryJson.removeSurrounding("[", "]").replace(""", "").split(",").map { s -> s.trim() }.filter { s -> s.isNotEmpty() },
                    parqPassed = it.parqPassed,
                    parqDateEpochMs = it.parqDateEpochMs,
                    injuryTags = it.injuryTagsJson.removeSurrounding("[", "]").replace(""", "").split(",").map { s -> s.trim() }.filter { s -> s.isNotEmpty() },
                    experienceLevel = TrainingExperience.valueOf(it.experienceLevel),
                    preferredSplit = PreferredSplit.valueOf(it.preferredSplit),
                    createdAtEpochMs = it.createdAtEpochMs
                )
            }
        }
    }

    suspend fun saveUserProfile(profile: UserProfile) {
        val entity = UserEntity(
            id = profile.id,
            heightCm = profile.heightCm,
            currentWeightKg = profile.currentWeightKg,
            targetWeightKg = profile.targetWeightKg,
            sex = profile.sex.name,
            ageYears = profile.ageYears,
            activityLevel = profile.activityLevel.name,
            goalType = profile.goalType.name,
            goalMode = profile.goalMode?.name,
            pacePreset = profile.pacePreset,
            targetDateEpochMs = profile.targetDateEpochMs,
            target1RmKg = profile.target1RmKg,
            targetDurationSeconds = profile.targetDurationSeconds,
            targetDistanceMeters = profile.targetDistanceMeters,
            workoutLocation = profile.workoutLocation.name,
            equipmentInventoryJson = profile.equipmentInventory.joinToString(prefix = "[", postfix = "]", separator = ",") { "\"$it\"" },
            parqPassed = profile.parqPassed,
            parqDateEpochMs = profile.parqDateEpochMs,
            injuryTagsJson = profile.injuryTags.joinToString(prefix = "[", postfix = "]", separator = ",") { "\"$it\"" },
            experienceLevel = profile.experienceLevel.name,
            preferredSplit = profile.preferredSplit.name,
            createdAtEpochMs = profile.createdAtEpochMs
        )
        userDao.insertOrUpdateUser(entity)
    }
}
