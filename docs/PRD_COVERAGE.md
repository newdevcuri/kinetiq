# Kinetiq Master PRD & Build Spec Coverage Matrix (docs/PRD_COVERAGE.md)

Generated: 2026-08-24
Status: RECONCILED & GATED FOR PHASE A

This matrix tracks 100% of requirements across the Kinetiq Master PRD (Parts A, B, C; Sections 1–34) and the Master Build Prompt v2 explicit modifications.

## Legend
- **Phase A**: Provisioning & Audit
- **Phase 0**: Foundation (Schema, Design System, Animation Pipeline, ETL Seed DB)
- **Phase 1**: Core Experience (Onboarding, Generator, Player, Library, Rings, 4 Goal Types, Readiness v1, Cardio Track, Time Constraints)
- **Phase 1.5**: Polish Gate (Performance, JankStats, Macrobenchmark, 12 Motion Fallbacks, Clinical Edge Cases, TalkBack)
- **Phase 2**: Depth (Hall Forecast UI, HR-Blended Keytel Calorie Engine, Boss Fights, Symmetry, Widgets, PDF Export)
- **Phase 3**: Intelligence & Ecosystem (MediaPipe Pose Form Coach, TTS, Voice Logging, Local P2P Sync)

---

## 1. Master PRD Section Coverage Matrix

| PRD Section | Title & Requirement Scope | Target Phase | Implementation Module / Component | Verification Method | Status |
|---|---|---|---|---|---|
| **PRD §1** | Executive Summary & Vision (Offline-first, zero-paywall, zero-ads, privacy-first) | All (A–3) | Entire Architecture | Airplane mode tests, no network permissions in manifest | Planned |
| **PRD §2** | User Personas & Journey (Home lifter, Busy professional, Safety-conscious user) | Phase 1 | `:feature:onboarding`, `:feature:train` | UI flows & preference adaptation tests | Planned |
| **PRD §3** | Information Architecture & Nav (Summary, Train, Library, Progress 4-tab model) | Phase 0, 1 | `:app`, `:core:designsystem` | Compose Navigation & screenshot baselines | Planned |
| **PRD §4** | Onboarding & Safety Intake (PAR-Q+, injury tags, equipment, experience, split) | Phase 1 | `:feature:onboarding` | Flow unit tests, contraindication rule tests | Planned |
| **PRD §5** | Biomechanical Engine & Session Structure (4-phase strength: Warmup+SRS, Primary, Accessory, Cooldown) | Phase 1 | `:core:engine`, `:feature:workout` | Unit tests with golden session fixtures | Planned |
| **PRD §6** | Metabolic Modeling & Hall Energy Balance (Mifflin-St Jeor, Hall model TDEE decay) | Phase 1, 2 | `:core:engine` | Mathematical golden fixture tests against Lancet papers | Planned |
| **PRD §7** | Adaptive Workout Progression & Double Progression (RIR-based, deload detection, missed workouts) | Phase 1 | `:core:engine` | Unit test state machine & progression fixtures | Planned |
| **PRD §8** | Exercise Substitution Engine (Biomechanics & fatigue-cost graph) | Phase 1 | `:core:engine` | Graph traversal & constraint satisfaction unit tests | Planned |
| **PRD §9** | *REVISED*: Anti-Cheat / Shadowban (*Explicitly Removed per v2 Spec*) | N/A | Removed (Decision #01 in DECISION_LOG) | Verified absent from schema and logic | Removed |
| **PRD §10** | Gamification & Tiers (Tiers 1–2 consistency in P1; Tiers 4–5 Boss Fights in P2; XP, Streaks, Freezes) | Phase 1, 2 | `:core:engine`, `:core:database` | XP & streak state tests, tier unlocking tests | Planned |
| **PRD §11** | Exercise Library & Detail Screens (Search/filter, muscle maps, tempo cues, safety notes) | Phase 1 | `:feature:library` | UI tests, filter verification tests | Planned |
| **PRD §12** | Workout Player UX & State Management (Per-set logging, rest timer dropdown, haptics, recovery) | Phase 1 | `:feature:workout` | Process-death restore tests, timer accuracy tests | Planned |
| **PRD §13** | Activity Rings & Dashboard UX (3 Canvas rings: Move, Exercise, Stand/Rest, weekly bars) | Phase 0, 1 | `:core:designsystem`, `:feature:dashboard` | Canvas draw tests, animation tests, TalkBack | Planned |
| **PRD §14** | Spaced Repetition System (SRS for Form Cues & Biomechanical Technique) | Phase 1 | `:core:engine`, `:core:database` | SuperMemo-2 / Leitner modified algorithm unit tests | Planned |
| **PRD §15** | Bilateral Symmetry Logging & Auto-Prescription | Phase 2 | `:core:engine`, `:feature:progress` | Imbalance threshold & prescription unit tests | Planned |
| **PRD §16** | Health Connect & Samsung Health Integration (Steps, HR, Sleep reads; Session writes) | Phase 1, 2 | `:core:healthconnect` | Mock HealthConnectClient tests, permission denial tests | Planned |
| **PRD §17** | Calorie Calculation Engines (v1 MET-only, v2 Keytel HR-blended) | Phase 1, 2 | `:core:engine` | Keytel formula unit tests, gap-filling fallback tests | Planned |
| **PRD §18** | Clinical-Honesty PDF Export (Encrypted/plain SAF export of logs & PAR-Q+) | Phase 2 | `:core:data`, `:feature:progress` | PDF generator integration tests, SAF intent tests | Planned |
| **PRD §19** | Glance App Widgets (Today Ring, No-Excuse Micro-HIIT Launcher) | Phase 2 | `:app:glance` | Glance UI tests, offline widget update tests | Planned |
| **PRD §20** | Live Notifications & ProgressStyle (Rest countdown, active session banner) | Phase 1, 2 | `:app:notifications` | Notification channel & permission fallback tests | Planned |
| **PRD §21** | Midnight Auto-Regulation & WorkManager Tasks (Day reset, streak reconciliation, DST safe) | Phase 1 | `:app:workmanager` | WorkManager test runner, simulated midnight triggers | Planned |
| **PRD §22** | MediaPipe On-Device Pose Form Coach & Rep Counter | Phase 3 | `:feature:pose` | Feature flag test, offline frame processing test | Planned |
| **PRD §23** | TTS Workout Buddy & Voice-Activated Set Logging | Phase 3 | `:feature:voice` | Android TTS & SpeechRecognizer fallback tests | Planned |
| **PRD §24** | Soreness-Based Dynamic Warmup Generator | Phase 3 | `:core:engine` | Muscle soreness mapping unit tests | Planned |
| **PRD §25** | Local P2P Sync (Wi-Fi Direct / WebRTC Same-Room Sync) | Phase 3 | `:core:sync` | Local socket / NSD discovery tests | Planned |
| **PRD §26** | Wear OS Companion & Sensor Streaming | Phase 3 | `:wear` | DataClient / MessageClient offline tests | Planned |
| **PRD §27** | Design System & Motion Physics (OLED Black, Frosted Chrome, Spring constants) | Phase 0, 1.5 | `:core:designsystem` | Screenshot tests, 12 §5b Motion Catalog tests | Planned |
| **PRD §28** | Room Database Architecture & Migrations (Schema v2, SQLite WAL, encrypted backup opt-out) | Phase 0 | `:core:database` | Room migration tests, foreign key integrity tests | Planned |
| **PRD §29** | Seed Database ETL Pipeline (`prepackaged_exercises.db`, Wger + ExerciseDB) | Phase 0 | `scripts/etl_seed_database.py` | Hash manifest verification, license metadata check | Planned |
| **PRD §30** | Security, Privacy & Backup Policy (Biometric lock, `allowBackup=false`, AES-GCM SAF) | Phase 1, 2 | `:core:data`, `:app` | BiometricPrompt tests, backup manifest audit | Planned |
| **PRD §31** | Mathematical & Biomechanical Golden Fixtures (Hall model, Mifflin-St Jeor, Keytel) | Phase 1, 2 | `:core:engine:test` | Golden reference fixture assertion suite | Planned |
| **PRD §32** | Branding, Icons & Typography (Adaptive Squircle ring icon, Inter font, no Apple marks) | Phase 0 | `:core:designsystem`, `:app` | Asset audit, icon renderer tests | Planned |
| **PRD §33** | Reliability Register & Edge Cases (Process death, Doze timers, incoming calls, font scaling) | Phase 1.5 | Entire App | Automated edge-case integration suite | Planned |
| **PRD §34** | Scope Boundaries, Explicit Non-Goals & Phase Review Rules | All | Project Management | Phase DoD review and DECISION_LOG tracking | Enforced |

---

## 2. Master Build Prompt v2 Specific Reconciliations & Extensions

| v2 Spec Item | Extension Detail | Target Phase | Implementation Module | Verification Method |
|---|---|---|---|---|
| **§5a** | **Exercise Animation Quality Bar**: 2D stylized human figure, proportional anatomy, muscle shading, biomechanical weight shift, Lottie vector format | Phase 0, 1 | `assets/animations/`, `:feature:library` | Human-readability review gate, zero stick-figure audit |
| **§5b** | **12-Item Motion Catalog**: 1. Hero Expansion, 2. Progress Rings, 3. Bar Charts, 4. HR Pulse, 5. Streak Particles, 6. Checkmark Morph, 7. Elastic FAB, 8. Pager Slide, 9. Dropdown Timer, 10. Shimmer Skeleton, 11. Shared Element, 12. Bottom Sheet | Phase 0, 1, 1.5 | `:core:designsystem`, all feature modules | Interaction tests + individual Reduce-Motion fallback tests for all 12 |
| **§7 / §7b** | **Goal-Setting & Feasibility Engine (4 Goal Types)**: Weight Loss (Hall model + 1% safety cap), Muscle Gain (TDEE + surplus + volume), Strength (Target 1RM + rep scheme), Endurance (Milestone + cardio track) | Phase 1 | `:core:engine`, `:feature:onboarding`, `:feature:progress` | Shared simulation engine tests; projection matches progress line |
| **§7a** | **Readiness-Adaptive Training Engine**: Sleep, HR baseline delta, soreness map, yesterday volume fallback -> Low/Normal/High transparent session adjustments | Phase 1 (fallback signal), Phase 2 (enriched HR/sleep) | `:core:engine`, `:core:database`, `:feature:train` | Unit tests for 3-band adjustment; degrade to Normal when no signals |
| **§7c** | **Cardio / Endurance Programming Track**: Warmup, Interval/Steady Main sets with HR zones / RPE cues, double progression, Cooldown, equipment awareness | Phase 1 | `:core:engine`, `:feature:train`, `:feature:workout` | Session template generation unit tests & player execution |
| **§7d** | **Time-Constrained Generation**: 15/30/45/60 min constraint with protected warmup/cooldown floors | Phase 1 | `:core:engine`, `:feature:train` | Time budget compression unit tests; floor invariant assertions |
| **§8** | **Samsung Health via Health Connect**: Unbundled consent, steps/HR/sleep readers, ExerciseSessionRecord writes, SecurityException handling | Phase 1, 2 | `:core:healthconnect` | Integration tests with simulated Health Connect provider |
| **§10** | **Clinical-Logic Edge-Case Register**: Tag-conflict floor set, 90-day PAR-Q+ re-screening, locked-tier transparency, non-clinical honest copy | Phase 1, 1.5 | `:core:engine`, `:feature:onboarding`, `:feature:train` | Edge-case unit test suite (empty result set fallback, re-screening) |

---

## 3. Phase A Verification Statement
This coverage matrix provides full traceable linkage for every requirement, ensuring zero silent descoping and exact alignment with the Master PRD and v2 Build Spec.
