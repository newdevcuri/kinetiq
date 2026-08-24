package com.kinetiq.fitness.core.engine

data class PlateLoadBreakdown(
    val targetWeightKg: Double,
    val barWeightKg: Double,
    val platesPerSide: List<Double>,
    val actualTotalKg: Double
)

object GymUtilityEngines {
    private val AVAILABLE_PLATES_KG = listOf(20.0, 15.0, 10.0, 5.0, 2.5, 1.25)

    /**
     * Calculates required plates per side for standard barbell loading
     */
    fun calculateBarbellPlates(
        targetWeightKg: Double,
        barWeightKg: Double = 20.0
    ): PlateLoadBreakdown {
        if (targetWeightKg <= barWeightKg) {
            return PlateLoadBreakdown(targetWeightKg, barWeightKg, emptyList(), barWeightKg)
        }

        var weightPerSide = (targetWeightKg - barWeightKg) / 2.0
        val plates = mutableListOf<Double>()

        for (plate in AVAILABLE_PLATES_KG) {
            while (weightPerSide >= plate) {
                plates.add(plate)
                weightPerSide -= plate
            }
        }

        val actualTotal = barWeightKg + (plates.sum() * 2.0)
        return PlateLoadBreakdown(
            targetWeightKg = targetWeightKg,
            barWeightKg = barWeightKg,
            platesPerSide = plates,
            actualTotalKg = actualTotal
        )
    }
}
