package com.kinetiq.fitness.core.database

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [
        UserEntity::class,
        ExerciseEntity::class,
        WorkoutSessionEntity::class,
        SetLogEntity::class,
        DailyReadinessLogEntity::class,
        BodyWeightLogEntity::class,
        SrsReviewEntity::class
    ],
    version = 2,
    exportSchema = false
)
abstract class KinetiqDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun exerciseDao(): ExerciseDao
    abstract fun workoutSessionDao(): WorkoutSessionDao
    abstract fun setLogDao(): SetLogDao
    abstract fun dailyReadinessDao(): DailyReadinessDao
    abstract fun bodyWeightDao(): BodyWeightDao
}
