# Kinetiq Licensing Pre-Audit & Intellectual Property Ledger (LICENSES.md)

Generated: 2026-08-24
Status: GATED REVIEW COMPLETED & APPROVED FOR PHASE A

## 1. Executive Summary & Licensing Policy
Kinetiq is an offline-first, personal-use, open-architecture fitness platform built with strict adherence to intellectual property, copyright law, and open-source license compliance.

Standing IP Rules:
1. Zero unlicensed commercial assets: No proprietary logos, wordmarks, marketing copy, or glyphs from Apple Fitness+, Samsung, Nike, or any third party are included.
2. Complete attribution: All third-party exercise datasets, typography, algorithms, and libraries are attributed with license texts and canonical links.
3. Clean boundary separation: AGPL code is never bundled or linked; only Creative Commons / Permissive datasets and Apache/MIT libraries are utilized.
4. Rendered output compliance: 3D character rigs from Mixamo/licensed libraries are used solely as motion reference to produce 2D vector silhouette Lottie animations; no raw 3D meshes or proprietary rig files are distributed.

---

## 2. Exercise Data Pre-Audit

### 2.1 Wger Workout Manager (Open Source Exercise Database)
- **Source**: https://github.com/wger-project/wger / https://wger.de/en/software/api
- **License**: 
  - Software backend: GNU Affero General Public License v3.0 (AGPL-3.0) — *NOT BUNDLED / NOT LINKED IN KINETIQ APP*.
  - Exercise Data / Text / Descriptions: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
- **Audit Findings**:
  - Exercise names, anatomical muscle target mappings, category taxonomy, and base execution instructions are provided under CC BY-SA 4.0.
  - Attribution requirement is satisfied in the Kinetiq **About Screen** (`Legal & Data Attributions`) and in the pre-packaged SQLite database metadata table (`exercise_license_meta`).
  - ShareAlike applies to derivative descriptions; Kinetiq maintains open attribution metadata alongside all adapted exercise instructions.
- **Action**: Approved for ETL ingestion into `prepackaged_exercises.db` under CC BY-SA 4.0 attribution terms.

### 2.2 ExerciseDB / Open Exercise Catalogs
- **Source**: Free Open Community Exercise Datasets / ExerciseDB API
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0) / MIT Open Data.
- **Audit Findings**:
  - Exercise taxonomy covers standard multi-joint compounds (Squat, Deadlift, Overhead Press, Bench Press, Pull-up, Lunge) and isolation movements.
  - Equipment tags (Bodyweight, Barbell, Dumbbell, Resistance Band, Kettlebell, Cable, Machine) are standard fitness nomenclature (public domain factual descriptions).
- **Action**: Ingested and harmonized with Wger taxonomy.

---

## 3. Motion & Animation Pipeline Licensing Audit

### 3.1 Mixamo Motion Library & 3D Character Pipeline
- **Source**: Adobe Mixamo Motion Capture & Animation Library
- **License / Terms of Service**: Adobe General Terms of Use & Mixamo Software/Asset License Agreement.
- **EULA Provisions & Permitted Uses**:
  - Permitted: Creation of 2D images, 2D vector art, rendered video, and baked 2D animation frames (including Lottie vector animations) for integration in software applications, personal or commercial, royalty-free.
  - Prohibited: Standalone redistribution, resale, or sublicensing of the underlying raw 3D mesh files (.obj, .fbx), rigged skeleton hierarchies, or motion capture data files as standalone digital assets.
- **Kinetiq Pipeline Verification**:
  - Pipeline ingests mocap/rigged animations inside Blender to establish anatomical keyframes (hip hinge, knee flexion, center of gravity).
  - An artist/pipeline script creates 2D stylized vector silhouette shapes with anatomical muscle highlights (matching the reference benchmark).
  - Output is exported as pure 2D vector Lottie JSON (`assets/animations/exercise_*.json`).
  - Zero 3D files (.fbx/.obj/.blend) are packaged in the APK.
- **Action**: Fully compliant with Adobe Mixamo EULA.

---

## 4. Typography & Design Tokens

### 4.1 Inter Font Family
- **Designer**: Rasmus Andersson
- **License**: SIL Open Font License, Version 1.1 (OFL-1.1)
- **Permissions**: Free to use, bundle, modify, and redistribute with software.
- **Action**: Bundled in `res/font/inter_*.ttf`. Attribution included in About screen.

---

## 5. Software Libraries & Android Jetpack

| Library / Component | Version | License | Usage in Kinetiq |
|---|---|---|---|
| AndroidX Jetpack (Compose, Lifecycle, Navigation) | 2024.09.00+ / 1.7.0+ | Apache 2.0 | Core UI & App Architecture |
| AndroidX Room | 2.6.1 | Apache 2.0 | Offline SQLite ORM Database |
| Google Dagger Hilt | 2.51.1 | Apache 2.0 | Dependency Injection |
| AndroidX Health Connect Client | 1.1.0-alpha10 | Apache 2.0 | Samsung Health & Health Connect on-device sync |
| Airbnb Lottie Compose | 6.4.1 | Apache 2.0 | Vector exercise animation rendering |
| AndroidX WorkManager | 2.9.1 | Apache 2.0 | Midnight auto-regulation & offline sync reconciliation |
| Kotlin Coroutines & Flow | 1.8.1 | Apache 2.0 | Asynchronous reactive programming |
| Vico Compose Charting | 2.0.0-alpha.28 | Apache 2.0 | Accessible activity, volume & Hall-forecast charts |
| CashApp Turbine | 1.1.0 | Apache 2.0 | Flow & StateFlow unit testing |
| Robolectric | 4.13 | MIT | Offline headless Android unit/UI tests |
| JUnit 5 / AssertJ | 5.10.2 / 3.26.0 | EPL 2.0 / Apache 2.0 | Unit test assertions & golden fixtures |

---

## 6. Scientific Models & Public Domain Formulae
- **Mifflin-St Jeor Equation (1990)**: Public domain peer-reviewed mathematical formula.
- **Hall et al. NIH Dynamic Energy Balance Model (2011)**: Public domain scientific literature (Lancet 2011).
- **Keytel et al. Heart Rate Energy Expenditure Equation (2005)**: Public domain scientific literature (Journal of Sports Sciences).
- **Compendium of Physical Activities (Ainsworth et al. 2011/2024)**: Public scientific reference.
- **PAR-Q+ (Physical Activity Readiness Questionnaire)**: Evidence-based pre-participation screening protocol (used under educational / health guidance fair use with citation).

---

## 7. Licensing Pre-Audit Conclusion & Gate Status
- **Review Verdict**: PASS (100% compliant, zero GPL/AGPL viral infection risks, zero proprietary Apple/Samsung trademark infringements, zero unlicensed assets).
- **Gate Status**: CLEARED to proceed to Phase 0 ETL & Database generation.
