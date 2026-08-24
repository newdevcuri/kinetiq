package com.kinetiq.fitness.core.database

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :id LIMIT 1")
    fun getUserFlow(id: String = "primary_user"): Flow<UserEntity?>

    @Query("SELECT * FROM users WHERE id = :id LIMIT 1")
    suspend fun getUser(id: String = "primary_user"): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateUser(user: UserEntity)
}

@Dao
interface ExerciseDao {
    @Query("SELECT * FROM exercises WHERE id = :id")
    suspend fun getExerciseById(id: String): ExerciseEntity?

    @Query("SELECT * FROM exercises ORDER BY name ASC")
    fun getAllExercisesFlow(): Flow<List<ExerciseEntity>>

    @Query("SELECT * FROM exercises WHERE category = :category ORDER BY name ASC")
    fun getExercisesByCategoryFlow(category: String): Flow<List<ExerciseEntity>>

    @Query("SELECT * FROM exercises WHERE movementPattern = :pattern")
    suspend fun getExercisesByMovementPattern(pattern: String): List<ExerciseEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertExercises(exercises: List<ExerciseEntity>)
}

@Dao
interface WorkoutSessionDao {
    @Query("SELECT * FROM workout_sessions ORDER BY dateEpochMs DESC")
    fun getAllSessionsFlow(): Flow<List<WorkoutSessionEntity>>

    @Query("SELECT * FROM workout_sessions WHERE id = :id")
    suspend fun getSessionById(id: String): WorkoutSessionEntity?

    @Query("SELECT * FROM workout_sessions WHERE completed = 0 ORDER BY dateEpochMs DESC LIMIT 1")
    suspend fun getActiveIncompleteSession(): WorkoutSessionEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateSession(session: WorkoutSessionEntity)
}

@Dao
interface SetLogDao {
    @Query("SELECT * FROM set_logs WHERE sessionId = :sessionId ORDER BY setNumber ASC")
    fun getSetLogsForSessionFlow(sessionId: String): Flow<List<SetLogEntity>>

    @Query("SELECT * FROM set_logs WHERE sessionId = :sessionId ORDER BY setNumber ASC")
    suspend fun getSetLogsForSession(sessionId: String): List<SetLogEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateSetLog(setLog: SetLogEntity)
}

@Dao
interface DailyReadinessDao {
    @Query("SELECT * FROM daily_readiness_logs WHERE dateEpochDay = :epochDay LIMIT 1")
    suspend fun getReadinessForDay(epochDay: Long): DailyReadinessLogEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdateReadiness(readiness: DailyReadinessLogEntity)
}

@Dao
interface BodyWeightDao {
    @Query("SELECT * FROM body_weight_logs ORDER BY dateEpochMs ASC")
    fun getWeightLogsFlow(): Flow<List<BodyWeightLogEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertWeightLog(weightLog: BodyWeightLogEntity)
}
