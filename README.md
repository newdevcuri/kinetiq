# Kinetiq — Native Android Fitness Platform

Kinetiq is an autonomous, offline-first, safety-conscious fitness platform built for Native Android. It provides visual and interaction parity with modern luxury fitness standards while remaining 100% free, zero-ad, cloud-optional, and privacy-first.

## Core Pillars & Architecture
- **Offline-First & Local Storage**: 100% functional in airplane mode. Seed database (`prepackaged_exercises.db`) and user data stored in SQLite / Room.
- **Design System**: True OLED black (`#000000`), Dark Slate (`#1C1C1E`), and Canvas triple-ring summary (`drawArc` with `sweepGradient`).
- **Lottie Vector Animation Pipeline**: Stylized 2D humanoid figures performing movements with accurate anatomical mass, muscle shading, and tempo cadence (zero stick figures).
- **Metabolic & Goal Engine**: Mifflin-St Jeor BMR, Hall et al. dynamic TDEE simulation, and 1.0% weekly body weight loss safety cap. Supports 4 goal types: Weight Loss, Muscle Gain, Strength, and Endurance.
- **Location & Equipment Optimizer**: Home Gym vs. Commercial Gym intake dynamically filters and utilizes 100% of available equipment inventory.
- **Motion & Micro-Interactions**: All 12 items from the Motion Catalog (§5b) implemented with spring physics and individual Reduce-Motion fallbacks.
- **Health Connect Integration**: Reads Steps, Heart Rate, and Sleep; writes completed workout sessions back to Health Connect / Samsung Health.
- **On-Device Intelligence**: Privacy-preserving MediaPipe pose form coaching, offline voice logging, plate loading calculator, and local P2P sync.

## Project Structure
```
├── app/                  # Main Android application & navigation shell
├── core/
│   ├── model/            # Domain entities, user profile, feature flags
│   ├── database/         # Room schema v2, entities, DAOs, prepackaged DB
│   ├── designsystem/     # Color tokens, Canvas rings, spring motion catalog
│   ├── engine/           # Metabolic, Goal, Readiness, Generator, Keytel, Pose
│   ├── data/             # Repositories & personal log exporter
│   └── healthconnect/    # Health Connect client & Samsung Health sync
├── feature/
│   ├── onboarding/       # PAR-Q+, location/equipment intake, multi-goal setter
│   ├── dashboard/        # Summary tab, 3 activity rings, readiness banner
│   ├── train/            # Train tab, time-constrained duration selector
│   ├── workout/          # Active workout player, per-set logger, rest timer
│   ├── library/          # Exercise library, muscle maps, Lottie player
│   └── progress/         # Weight history & dynamic Hall forecast chart
├── datasets/             # Seed DB (prepackaged_exercises.db), manifest & index
├── docs/                 # PRD coverage matrix, licensing audit, research pack
└── scripts/              # Automated test suites, ETL pipeline, import linters
```

## Running Automated Tests
```bash
# Run all phase verification test suites & import integrity linter
python3 scripts/test_phase_0.py
python3 scripts/test_phase_1.py
python3 scripts/test_phase_1_5.py
python3 scripts/test_phase_2.py
python3 scripts/test_phase_3.py
python3 scripts/check_import_integrity.py
```
