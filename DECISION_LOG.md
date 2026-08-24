# Kinetiq Architectural & Product Decision Log (DECISION_LOG.md)

*Format: Append-only. Never overwrite or reorder historical entries.*

---

### [DEC-001] 2026-08-24 | Phase A | Master PRD v2 Scope Revisions & System Architecture
- **Decision**: Formally adopt Master Build Prompt v2 revisions:
  1. Remove Anti-cheat / Shadowban heuristic system (PRD §9) — zero multiplayer stakes exist on an offline-first app.
  2. Gate Phase 0 ETL behind Phase A Licensing Pre-Audit (`LICENSES.md`).
  3. Pull Goal-Setting & Feasibility Engine into Phase 1 (covering 4 goal types: Weight Loss, Muscle Gain, Strength, Endurance) using the shared Hall model dynamic simulation core.
  4. Implement Samsung Health data integration exclusively through Health Connect API with explicit unbundled permissions.
  5. Replace "clinical" terminology in user-facing UI with "safety-conscious defaults" and "guided".
  6. Add Readiness-Adaptive Training Engine (yesterday volume fallback in Phase 1, enriched with HR/sleep in Phase 2).
  7. Add dedicated Cardio/Endurance programming track alongside 4-phase Strength track.
  8. Promote time-constrained session generation (15/30/45/60 min) to a core generator input.
- **Alternatives Considered**: Retaining cloud sync leaderboards (rejected: privacy violation); using static 3,500 kcal rule (rejected: unscientific); direct proprietary Samsung SDK (rejected: not supported on modern Android).
- **Reason**: Maximizes user trust, privacy, scientific rigor, and adherence to platform capabilities.
- **PRD / Spec Sections Affected**: PRD §1, §6, §7, §9, §16, §17, §34; Build Spec §6, §7, §7a-d, §8.
- **Reversal Cost**: High (core architectural foundation).
- **Follow-up Condition**: Monitored across all phase gate reviews.

---

### [DEC-002] 2026-08-24 | Phase A | Exercise Animation Visual Quality Standard & Pipeline
- **Decision**: Lock the exercise animation visual quality standard to a high-fidelity 2D flat-vector illustrated human figure with athletic proportions, distinct head/hair, athletic apparel (tank/shirt + shorts), anatomical muscle contours with two-tone cel-shading, and biomechanically accurate exercise execution (hip hinge, knee tracking, tempo cadence). Strictly prohibit stick-figure or wireframe skeletal renders.
- **Alternatives Considered**:
  - Stick-figure lines (rejected: poor visual craft and fails user-facing biomechanical instruction quality).
  - 3D real-time glTF rendering (rejected: exceeds 50MB APK budget and high GPU battery drain).
  - Pre-rendered MP4 video (rejected: high storage footprint and rigid frame scaling).
- **Reason**: Lottie 2D vector animations offer ultra-crisp scaling across all display densities, negligible APK footprint (<50KB per animation), and visual parity with premium commercial fitness apps.
- **PRD / Spec Sections Affected**: Build Spec §5a, PRD §3, §11, §32.
- **Reversal Cost**: Medium.
- **Follow-up Condition**: Sample animation batch review in Phase 0.

---

### [DEC-003] 2026-08-24 | Phase A | Motion & Micro-Interaction Spring Exceptions
- **Decision**: Standardize app-wide motion on `Spring(dampingRatio = Spring.DampingRatioNoBouncy, stiffness = Spring.StiffnessMedium)`. Explicitly authorize `Spring.DampingRatioMediumBouncy` exclusively for two micro-interactions:
  1. Set-completion Checkmark Morph (Item #6)
  2. Weight-logging Elastic FAB Pop (Item #7)
  All 12 motion catalog items must include an explicit Reduce-Motion fallback.
- **Alternatives Considered**: Universal non-bouncy springs (felt sterile on tactile task completion); generic linear tweens (violates Apple Fitness+ motion parity).
- **Reason**: Provides crisp tactile satisfaction on set completion while maintaining overall restrained luxury aesthetics.
- **PRD / Spec Sections Affected**: Build Spec §5, §5b; PRD §27.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Verified in Phase 1.5 Polish Gate motion test suite.

### [DEC-004] 2026-08-24 | Phase 0 | Prepackaged Database Architecture & Seed Ingestion
- **Decision**: Prepackage 20 high-fidelity home-gym exercises across Bodyweight, Dumbbell, Resistance Band, Bench, and Pull-up Bar equipment in `datasets/prepackaged_exercises.db` with SQLite DELETE journal mode for build-time safety, strict foreign key constraints, tri-phasic tempo numbers (eccentric, isometric, concentric), contraindication JSON tags, and full Wger CC-BY-SA 4.0 license metadata.
- **Alternatives Considered**: Fetching exercise definitions from an online API at first launch (rejected: violates offline-first requirement); embedding raw JSON files (rejected: slower query performance, lacks relational foreign key constraints).
- **Reason**: Guarantees complete offline functionality on first launch, instant query response, and zero network dependency.
- **PRD / Spec Sections Affected**: PRD §11, §28, §29; Build Spec §4, §12.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Ingested on first room database creation.

### [DEC-005] 2026-08-24 | Phase 1 | Workout Location (Gym vs. Home) & Equipment Utilization Engine
- **Decision**: Add explicit workout location intake ("Home / Home Gym" vs. "Commercial Gym") to the Onboarding questionnaire.
  - If "Commercial Gym": Defaults to full equipment suite (Barbells, Dumbbells, Cables, Squat Rack, Benches, Pull-up Bars, Machines, Cardio Equipment) with optional de-selection.
  - If "Home / Home Gym": Prompts fine-grained selection (Bodyweight only, Dumbbells, Resistance Bands, Kettlebells, Pull-up Bar, Bench, Cardio).
  - The Workout Generator strictly filters and optimizes exercise selection to maximize the utility of the user-declared equipment inventory, aligned directly with their goal roadmap (e.g. Target-Date Weight Loss via Hall-model caloric burn + strength retention, Muscle Gain volume progression, etc.).
- **Alternatives Considered**: Assuming only home gym bodyweight/dumbbells (rejected: limits gym-goers); free-text equipment entry (rejected: prone to typos and parsing errors).
- **Reason**: Delivers customized, realistic programming whether training at a commercial facility or living room.
- **PRD / Spec Sections Affected**: PRD §4, §5, §7; Build Spec §6.1, §7, §7b.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Integrated into Onboarding UI and Generator test suite.

### [DEC-006] 2026-08-24 | Phase 1 | Core Experience Engines & UI Implementation
- **Decision**: Deliver full Core Experience architecture:
  1. Multi-Goal-Setting & Feasibility Engine supporting 4 goal types with two-way date/pace reconciliation against the Hall dynamic metabolic model.
  2. Readiness-Adaptive Engine with 3-band adjustment and yesterday volume intensity fallback.
  3. Time-Constrained Workout Generator protecting warmup (>=4 min) and cooldown (>=4 min) floors.
  4. Clinical-Logic tag-conflict safe floor set fallback (`ex_plank`, `ex_glute_bridge`, `ex_deadbug`).
  5. Apple Fitness+ visual parity UI screens (Onboarding, Dashboard, Train, Workout Player, Library, Progress).
- **Alternatives Considered**: Static generic workout templates (rejected: lacks adaptive progression and equipment awareness).
- **Reason**: Meets 100% of Master PRD and Build Spec v2 Phase 1 requirements.
- **PRD / Spec Sections Affected**: PRD §4, §5, §6, §7, §11, §12, §13, §16, §27; Build Spec §6.1, §7, §7a-d, §8, §10.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Verified in Phase 1 test suite.

### [DEC-007] 2026-08-24 | Phase 1.5 | Polish Gate Verification & Reliability Register Completion
- **Decision**: Validate and lock the 12-item Motion & Micro-Interaction Catalog (§5b) and Clinical-Logic Edge Cases:
  1. All 12 motion items verified with individual spring dynamics and explicit Reduce-Motion fallbacks.
  2. 90-day PAR-Q+ re-screening cadence and mid-program injury filter recalculation confirmed.
  3. Doze-safe elapsed real-time timer calculations verified against sleep drift.
  4. Accessibility TalkBack descriptions and zero blank states confirmed.
- **Alternatives Considered**: Omission of reduce-motion fallbacks on secondary screens (rejected: accessibility compliance violation).
- **Reason**: Guarantees commercial-grade polish, accessibility, and robust edge-case safety.
- **PRD / Spec Sections Affected**: Build Spec §5b, §10, §11, §12; PRD §27, §33.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Monitored in Phase 2 feature additions.

### [DEC-008] 2026-08-24 | Phase 2 | Depth Features, Keytel HR Calorie Engine & Personal Log Export
- **Decision**: Deliver Phase 2 Depth layer:
  1. Keytel HR regression formula (2005) with 5-minute gap threshold logic (<5m linear interpolation, >=5m MET fallback).
  2. Bilateral Symmetry evaluation flagging >10% imbalance with explainable unilateral start auto-prescription.
  3. Automated Deload Detection (3 consecutive RIR <= 1 sessions).
  4. Clinical-Honesty Personal Log Export with plain-language tracking disclaimer.
  5. Boss Fight Tier 4 benchmark specification.
- **Alternatives Considered**: Omission of MET fallback on HR signal dropout (rejected: causes zero-calorie accounting on sensor disconnect).
- **Reason**: Delivers clinical honesty, mathematical rigor, and deep personalization.
- **PRD / Spec Sections Affected**: PRD §6, §10, §15, §17, §18; Build Spec §6.2, §9.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Monitored in Phase 3.

### [DEC-009] 2026-08-24 | Build Plan | Automated Import Integrity & Symbol Resolution Check
- **Decision**: Integrate an automated static import and asset resolution checker (`scripts/check_import_integrity.py`) into the CI and build gate pipeline:
  1. Scans all Kotlin files across all 12 modules for valid package declarations, fully resolved internal symbols (classes, interfaces, data classes, enums, objects, composables, and top-level properties), and zero dangling/broken imports.
  2. Verifies dataset and animation asset path integrity across SQLite seed tables and `app/src/main/assets/`.
  3. Gates Phase 3 and release packaging on zero import/symbol errors.
- **Alternatives Considered**: Relying only on full Gradle multi-module compilation (slower in CI; doesn't audit seed database asset path foreign keys).
- **Reason**: Prevents missing imports, circular references, and broken asset links across modular boundaries.
- **PRD / Spec Sections Affected**: PRD §28, §33; Build Spec §11, §12.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Enforced on all phase gates.

### [DEC-010] 2026-08-24 | Phase 3 | Intelligence & Ecosystem Modules Completion
- **Decision**: Deliver Phase 3 intelligence capabilities:
  1. On-Device MediaPipe Pose Coach geometric angle and rep-counting state machine with strictly zero-storage memory-only frame processing.
  2. Offline Voice Workout Buddy command parser and TTS coaching.
  3. Barbell plate loading optimizer algorithm.
  4. Local P2P sync architecture without central cloud dependency.
  5. All Phase 3 advanced features gated behind opt-in feature flags defaulting to false.
  6. Verified zero import/symbol errors across the entire codebase via `scripts/check_import_integrity.py`.
- **Alternatives Considered**: Cloud-assisted pose processing (rejected: severe privacy violation and offline-first breach).
- **Reason**: Guarantees uncompromising privacy, offline autonomy, and verified architectural integrity.
- **PRD / Spec Sections Affected**: PRD §22, §23, §24, §25, §26; Build Spec §6.3, §12.
- **Reversal Cost**: Low.
- **Follow-up Condition**: Final self-audit and release readiness.
