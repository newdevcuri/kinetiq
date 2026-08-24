# Kinetiq Technical Research Pack & Architecture Blueprint (docs/RESEARCH_PACK.md)

Generated: 2026-08-24
Status: VERIFIED & LOCKED FOR PHASE A

## 1. Verified Stable Toolchain & Android Jetpack Versions

| Component | Target Version | Release / Maven Coordinates | Notes & Constraints |
|---|---|---|---|
| Android Gradle Plugin (AGP) | 8.5.2 | `com.android.tools.build:gradle:8.5.2` | Gradle 8.7+ compatible |
| Kotlin | 2.0.20 | `org.jetbrains.kotlin:kotlin-gradle-plugin:2.0.20` | Compose Compiler Gradle Plugin built-in |
| Compose BOM | 2024.09.00 | `androidx.compose:compose-bom:2024.09.00` | Compose UI 1.7.0+, Material3 1.3.0+ |
| Compose Animation / Foundation | 1.7.0 | Via Compose BOM | Supports `SharedTransitionLayout` / `Modifier.sharedElement` |
| AndroidX Room | 2.6.1 | `androidx.room:room-runtime:2.6.1`, `room-ktx:2.6.1`, `room-compiler:2.6.1` | SQLite WAL mode, schema export enabled |
| Google Dagger Hilt | 2.51.1 | `com.google.dagger:hilt-android:2.51.1`, `hilt-compiler:2.51.1` | Multi-module DI |
| Health Connect Client | 1.1.0-alpha10 | `androidx.health.connect:connect-client:1.1.0-alpha10` | Samsung Health & Health Connect on-device integration |
| Lottie Compose | 6.4.1 | `com.airbnb.android:lottie-compose:6.4.1` | Vector Lottie playback for exercise animations |
| Vico Compose Charting | 2.0.0-alpha.28 | `com.patrykandpatrick.vico:compose-m3:2.0.0-alpha.28` | Accessible bar & line charts |
| AndroidX WorkManager | 2.9.1 | `androidx.work:work-runtime-ktx:2.9.1` | Midnight auto-regulation & offline sync reconciliation |
| AndroidX Lifecycle / ViewModel | 2.8.5 | `androidx.lifecycle:lifecycle-viewmodel-compose:2.8.5` | Process-death saveable state |
| AndroidX Navigation Compose | 2.8.0 | `androidx.navigation:navigation-compose:2.8.0` | Type-safe Kotlin navigation |
| CashApp Turbine | 1.1.0 | `app.cash.turbine:turbine:1.1.0` | StateFlow assertion library |
| Robolectric | 4.13 | `org.robolectric:robolectric:4.13` | Fast, headless Android SDK simulation |
| AndroidX Benchmark / Macrobenchmark | 1.3.0 | `androidx.benchmark:benchmark-macro-junit4:1.3.0` | TTFD & frame jank testing |

---

## 2. Mathematical & Scientific Implementation Models

### 2.1 Mifflin-St Jeor Basal Metabolic Rate (BMR)
$$\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (yr)} + s$$
Where $s = +5$ for biological males, $s = -161$ for biological females.

### 2.2 NIH Dynamic Energy Balance Model (Hall et al. 2011)
Unlike the linear static 3,500 kcal/lb rule (Wishnofsky), Hall et al. accounts for adaptive thermogenesis, metabolic slowdown during weight loss, and changes in lean vs. fat tissue ratio:
- Rate of weight change: $\frac{dM}{dt} = \frac{\text{Intake} - \text{TDEE}(t)}{\rho}$
- Dynamic TDEE: $\text{TDEE}(t) = \text{BMR}(M(t)) \times \text{PAL} + \beta \times \Delta M(t) + \dots$
- Deficit Safety Cap: Maximum projected weight loss per week is capped at **1.0% of current projected bodyweight** ($0.01 \times W(t)$).
- Two-way Goal Feasibility Engine routes through the forward Euler simulation of this differential equation, guaranteeing that the target-date projection on onboarding exactly matches the live chart trajectory.

### 2.3 Keytel Heart Rate Energy Expenditure Regression (Keytel et al. 2005)
$$EE_{male} = (-55.0969 + (0.6309 \times HR) + (0.1988 \times W) + (0.2017 \times A)) / 4.184 \quad \text{[kcal/min]}$$
$$EE_{female} = (-20.4022 + (0.4472 \times HR) - (0.1263 \times W) + (0.074 \times A)) / 4.184 \quad \text{[kcal/min]}$$
Where $HR$ is heart rate in BPM, $W$ is weight in kg, $A$ is age in years.
- Gaps in HR readings $< 5$ min are linearly interpolated.
- Gaps $\ge 5$ min degrade to MET-based calculation for that segment and log `calorie_source = met_only`.

---

## 3. Apple Fitness+ Visual Parity Tokens & System Spec

### 3.1 Color Palette
- True Black Canvas: `#000000` (OLED power saving, infinite contrast)
- Card Surface: `#1C1C1E` (Dark Charcoal, 20dp–24dp rounded corners)
- Elevated Surface: `#2C2C2E` (Secondary sheets and buttons)
- Frosted Chrome Navigation: `#BF000000` with 20dp background blur
- Accent Tints:
  - Strength: `#162415` (Pine Green surface tint), `#30D158` (Vibrant emerald highlight)
  - Cardio / HIIT: `#2A1608` (Deep ember surface tint), `#FF453A` / `#FF9F0A` (Coral / Amber highlight)
  - Core & Mobility: `#181828` (Indigo surface tint), `#BF5AF2` (Purple highlight)
- Activity Rings (Triple Gradient Arc):
  - Move Ring: `#FF2D55` to `#FF375F` (Red/Rose)
  - Exercise Ring: `#A4FF00` to `#30D158` (Lime/Emerald)
  - Stand/Recovery Ring: `#00F0FF` to `#0A84FF` (Cyan/Azure)

### 3.2 Motion Physics Specification
- Default Spring: `Spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = Spring.StiffnessMedium)`
- Bouncy Exception Spring (Checkmark Morph & Elastic FAB Pop): `Spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessMediumLow)`
- Reduce-Motion Mode: System setting `Settings.Global.TRANSITION_ANIMATION_SCALE == 0` or in-app toggle replaces all spring physics with instantaneous zero-duration transitions or subtle alpha crossfades.
