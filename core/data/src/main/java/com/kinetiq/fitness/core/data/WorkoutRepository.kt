package com.kinetiq.fitness.core.data

import com.kinetiq.fitness.core.database.SetLogDao
import com.kinetiq.fitness.core.database.SetLogEntity
import com.kinetiq.fitness.core.database.WorkoutSessionDao
import com.kinetiq.fitness.core.database.WorkoutSessionEntity
import com.kinetiq.fitness.core.model.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class WorkoutRepository(
    private val sessionDao: WorkoutSessionDao,
    private val setLogDao: SetLogDao
) {
    fun getSessionsFlow(): Flow<List<WorkoutSession>> {
        return sessionDao.getAllSessionsFlow().map { list ->
            list.map { entity ->
                WorkoutSession(
                    id = entity.id,
                    dateEpochMs = entity.dateEpochMs,
                    plannedDurationMinutes = entity.plannedDurationMinutes,
                    actualDurationMinutes = entity.actualDurationMinutes,
                    trackType = SessionTrackType.valueOf(entity.trackType),
                    readinessBand = ReadinessBand.valueOf(entity.readinessBand),
                    estimatedCaloriesBurned = entity.estimatedCaloriesBurned,
                    calorieSource = CalorieSource.valueOf(entity.calorieSource),
                    completed = entity.completed,
                    notes = entity.notes
                )
            }
        }
    }

    suspend fun saveOrCompleteSession(session: WorkoutSession) {
        val entity = WorkoutSessionEntity(
            id = session.id,
            dateEpochMs = session.dateEpochMs,
            plannedDurationMinutes = session.plannedDurationMinutes,
            actualDurationMinutes = session.actualDurationMinutes,
            trackType = session.trackType.name,
            readinessBand = session.readinessBand.name,
            estimatedCaloriesBurned = session.estimatedCaloriesBurned,
            calorieSource = session.calorieSource.name,
            completed = session.completed,
            notes = session.notes
        )
        sessionDao.insertOrUpdateSession(entity)
    }

    suspend fun logSet(setLog: SetLog) {
        val entity = SetLogEntity(
            id = setLog.id,
            sessionId = setLog.sessionId,
            exerciseId = setLog.exerciseId,
            setNumber = setLog.setNumber,
            phase = setLog.phase.name,
            targetReps = setLog.targetReps,
            actualReps = setLog.actualReps,
            weightKg = setLog.weightKg,
            rir = setLog.rir,
            tempo = setLog.tempo,
            completed = setLog.completed,
            timestampEpochMs = setLog.timestampEpochMs
        )
        setLogDao.insertOrUpdateSetLog(entity)
    }
}
