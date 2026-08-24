#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kinetiq Build-Time Python ETL Seed Database Generator
Generates: datasets/prepackaged_exercises.db
Manifest: datasets/MANIFEST.json
Index: datasets/INDEX.txt
"""

import os, sqlite3, json, hashlib

def generate_database(output_path):
    if os.path.exists(output_path):
        os.remove(output_path)
    
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()
    
    cursor.executescript("""
    PRAGMA journal_mode = DELETE;
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS exercise_license_meta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        license_type TEXT NOT NULL,
        source_url TEXT NOT NULL,
        attribution_text TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS exercises (
        id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL, -- STRENGTH, CARDIO, MOBILITY
        movement_pattern TEXT NOT NULL, -- SQUAT, HINGE, HORIZONTAL_PUSH, HORIZONTAL_PULL, VERTICAL_PUSH, VERTICAL_PULL, LUNGE, CARRY, CORE, CARDIO_INTERVAL, CARDIO_STEADY
        primary_muscle TEXT NOT NULL,
        secondary_muscles_json TEXT NOT NULL, -- JSON array of strings
        equipment TEXT NOT NULL, -- BODYWEIGHT, DUMBBELL, BARBELL, RESISTANCE_BAND, KETTLEBELL, PULL_UP_BAR, BENCH, CARDIO_MACHINE
        tier INTEGER NOT NULL, -- 1 to 5
        fatigue_cost REAL NOT NULL, -- 1.0 (low) to 5.0 (high)
        contraindications_json TEXT NOT NULL, -- JSON array of condition tags
        instructions TEXT NOT NULL,
        safety_notes TEXT NOT NULL,
        tempo_eccentric INTEGER NOT NULL, -- seconds
        tempo_isometric INTEGER NOT NULL, -- seconds
        tempo_concentric INTEGER NOT NULL, -- seconds
        animation_asset_path TEXT NOT NULL,
        thumbnail_asset_path TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS exercise_substitutions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_exercise_id TEXT NOT NULL,
        substitute_exercise_id TEXT NOT NULL,
        fatigue_difference REAL NOT NULL, -- e.g. -0.5 for lower fatigue variant
        biomechanical_similarity REAL NOT NULL, -- 0.0 to 1.0
        FOREIGN KEY (original_exercise_id) REFERENCES exercises(id) ON DELETE CASCADE,
        FOREIGN KEY (substitute_exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS form_cues_srs (
        id TEXT PRIMARY KEY NOT NULL,
        exercise_id TEXT NOT NULL,
        cue_title TEXT NOT NULL,
        cue_description TEXT NOT NULL,
        phase_cue TEXT NOT NULL, -- ECCENTRIC, ISOMETRIC, CONCENTRIC, SETUP
        common_fault TEXT NOT NULL,
        correction_strategy TEXT NOT NULL,
        FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
    );
    """)

    # Insert License Metadata
    licenses = [
        ("Wger Workout Manager", "CC BY-SA 4.0", "https://wger.de", "Exercise anatomical taxonomy and base kinesiology data sourced under Creative Commons Attribution-ShareAlike 4.0 International."),
        ("ExerciseDB Open Catalog", "CC BY 4.0", "https://github.com/yuhonas/free-exercise-db", "Biomechanical movement naming and equipment classification."),
        ("Kinetiq Safety & Clinical Team", "Proprietary / Open In-App", "https://kinetiq.fitness", "Tri-phasic tempo cadence, contraindication tagging, fatigue indices, and safety cues.")
    ]
    cursor.executemany("""
        INSERT INTO exercise_license_meta (dataset_name, license_type, source_url, attribution_text)
        VALUES (?, ?, ?, ?)
    """, licenses)

    # Curated Home-Gym Exercise Catalog (High-Quality, Contraindication-Tagged, Home-Gym Filtered)
    exercises_data = [
        # SQUATS & LEGS
        (
            "ex_bodyweight_squat",
            "Bodyweight Air Squat",
            "STRENGTH",
            "SQUAT",
            "Quadriceps",
            json.dumps(["Glutes", "Hamstrings", "Core"]),
            "BODYWEIGHT",
            1,
            2.0,
            json.dumps(["KNEE_PAIN_SEVERE"]),
            "Stand with feet shoulder-width apart. Push hips back and bend knees until thighs are parallel to floor. Keep chest tall and heels planted. Drive through midfoot to stand.",
            "Maintain neutral spine; ensure knees track in line with toes. Do not let knees cave inward.",
            3, 1, 1,
            "animations/exercise_bodyweight_squat.json",
            "thumbnails/exercise_bodyweight_squat.png"
        ),
        (
            "ex_goblet_squat",
            "Dumbbell Goblet Squat",
            "STRENGTH",
            "SQUAT",
            "Quadriceps",
            json.dumps(["Glutes", "Core", "Upper Back"]),
            "DUMBBELL",
            1,
            2.8,
            json.dumps(["KNEE_PAIN_SEVERE", "LOWER_BACK_ACUTE"]),
            "Hold a dumbbell vertically against your sternum with both hands. Squat down between your legs until elbows gently touch inside knees. Drive upwards back to start.",
            "The front-loaded weight acts as a counterbalance, helping maintain an upright torso and reducing lumbar shear stress.",
            3, 1, 1,
            "animations/exercise_goblet_squat.json",
            "thumbnails/exercise_goblet_squat.png"
        ),
        (
            "ex_romanian_deadlift_db",
            "Dumbbell Romanian Deadlift (RDL)",
            "STRENGTH",
            "HINGE",
            "Hamstrings",
            json.dumps(["Glutes", "Erector Spinae", "Forearms"]),
            "DUMBBELL",
            2,
            3.5,
            json.dumps(["LOWER_BACK_ACUTE", "DISC_HERNIATION"]),
            "Hold dumbbells in front of thighs. With a soft knee bend, hinge at hips by pushing hips backward while keeping spine straight. Lower dumbbells to mid-shin until hamstring stretch is felt. Drive hips forward to stand.",
            "Keep dumbbells close to legs throughout movement. Never round the lumbar spine.",
            3, 1, 2,
            "animations/exercise_romanian_deadlift_db.json",
            "thumbnails/exercise_romanian_deadlift_db.png"
        ),
        (
            "ex_glute_bridge",
            "Bodyweight Glute Bridge",
            "STRENGTH",
            "HINGE",
            "Glutes",
            json.dumps(["Hamstrings", "Core"]),
            "BODYWEIGHT",
            1,
            1.5,
            json.dumps([]),
            "Lie on your back with knees bent and feet flat on floor hip-width apart. Drive through heels to lift hips until thighs and torso form a straight line. Squeeze glutes at top, then lower.",
            "Safe posterior chain movement for individuals with lower back sensitivity.",
            2, 2, 1,
            "animations/exercise_glute_bridge.json",
            "thumbnails/exercise_glute_bridge.png"
        ),
        (
            "ex_reverse_lunge",
            "Dumbbell Reverse Lunge",
            "STRENGTH",
            "LUNGE",
            "Quadriceps",
            json.dumps(["Glutes", "Hamstrings", "Calves"]),
            "DUMBBELL",
            2,
            3.0,
            json.dumps(["KNEE_PAIN_SEVERE"]),
            "Stand tall holding dumbbells at sides. Step backward with one leg and lower back knee toward floor until both knees are bent at 90 degrees. Push through front heel to return to start.",
            "Stepping backward reduces anterior patellar shear stress compared to forward lunges.",
            2, 1, 1,
            "animations/exercise_reverse_lunge.json",
            "thumbnails/exercise_reverse_lunge.png"
        ),

        # CHEST & HORIZONTAL PUSH
        (
            "ex_push_up",
            "Standard Push-Up",
            "STRENGTH",
            "HORIZONTAL_PUSH",
            "Chest",
            json.dumps(["Triceps", "Anterior Deltoids", "Core"]),
            "BODYWEIGHT",
            1,
            2.5,
            json.dumps(["WRIST_PAIN_SEVERE", "SHOULDER_IMPINGEMENT_ACUTE"]),
            "Place hands slightly wider than shoulder-width in a high plank position. Lower body in a straight line until chest is 2 inches off the ground. Press firmly through palms back to start.",
            "Maintain 45-degree elbow angle relative to torso; avoid flaring elbows out at 90 degrees.",
            3, 1, 1,
            "animations/exercise_push_up.json",
            "thumbnails/exercise_push_up.png"
        ),
        (
            "ex_incline_push_up",
            "Incline Push-Up (Bench/Elevation)",
            "STRENGTH",
            "HORIZONTAL_PUSH",
            "Chest",
            json.dumps(["Triceps", "Anterior Deltoids", "Core"]),
            "BENCH",
            1,
            1.8,
            json.dumps([]),
            "Place hands on an elevated bench or sturdy surface. Lower chest toward edge with straight body line, then press back up.",
            "Excellent regression for beginners or those managing wrist/shoulder rehabilitation.",
            3, 1, 1,
            "animations/exercise_incline_push_up.json",
            "thumbnails/exercise_incline_push_up.png"
        ),
        (
            "ex_db_floor_press",
            "Dumbbell Floor Press",
            "STRENGTH",
            "HORIZONTAL_PUSH",
            "Chest",
            json.dumps(["Triceps", "Anterior Deltoids"]),
            "DUMBBELL",
            2,
            3.0,
            json.dumps([]),
            "Lie on back on floor with knees bent. Hold dumbbells over chest with elbows at 45 degrees. Lower dumbbells until triceps gently touch floor, pause, and press back up.",
            "Floor limits shoulder extension, making this extremely shoulder-friendly.",
            3, 1, 1,
            "animations/exercise_db_floor_press.json",
            "thumbnails/exercise_db_floor_press.png"
        ),

        # BACK & PULL
        (
            "ex_dumbbell_row",
            "Single-Arm Dumbbell Row",
            "STRENGTH",
            "HORIZONTAL_PULL",
            "Latissimus Dorsi",
            json.dumps(["Rhomboids", "Biceps", "Rear Deltoids", "Core"]),
            "DUMBBELL",
            1,
            2.6,
            json.dumps([]),
            "Place one hand and knee on a bench (or hinge supported). Hold dumbbell in free hand. Pull dumbbell up towards your hip, driving elbow toward ceiling. Squeeze shoulder blade, then lower under control.",
            "Pull elbow back toward hip rather than straight up to maximize lat engagement.",
            3, 1, 1,
            "animations/exercise_dumbbell_row.json",
            "thumbnails/exercise_dumbbell_row.png"
        ),
        (
            "ex_band_pull_apart",
            "Resistance Band Pull-Apart",
            "MOBILITY",
            "HORIZONTAL_PULL",
            "Rear Deltoids",
            json.dumps(["Rhomboids", "Rotator Cuff", "Trapezius"]),
            "RESISTANCE_BAND",
            1,
            1.2,
            json.dumps([]),
            "Hold resistance band with arms straight out in front of chest at shoulder width. Pull band apart by squeezing shoulder blades together until band touches chest. Slowly return.",
            "Essential postural and rotator cuff health exercise.",
            2, 2, 1,
            "animations/exercise_band_pull_apart.json",
            "thumbnails/exercise_band_pull_apart.png"
        ),
        (
            "ex_pull_up",
            "Overhand Pull-Up",
            "STRENGTH",
            "VERTICAL_PULL",
            "Latissimus Dorsi",
            json.dumps(["Biceps", "Rhomboids", "Brachialis", "Forearms"]),
            "PULL_UP_BAR",
            3,
            4.2,
            json.dumps(["SHOULDER_IMPINGEMENT_ACUTE", "ELBOW_TENDINITIS"]),
            "Grip pull-up bar with overhand grip slightly wider than shoulders. Pull chest up toward bar by driving elbows down and back. Lower all the way to full dead-hang.",
            "Do not kip or swing; control the descent to protect the shoulder joint.",
            3, 1, 1,
            "animations/exercise_pull_up.json",
            "thumbnails/exercise_pull_up.png"
        ),

        # SHOULDERS & VERTICAL PUSH
        (
            "ex_db_overhead_press",
            "Seated Dumbbell Overhead Press",
            "STRENGTH",
            "VERTICAL_PUSH",
            "Anterior Deltoids",
            json.dumps(["Lateral Deltoids", "Triceps", "Upper Trapezius"]),
            "DUMBBELL",
            2,
            3.4,
            json.dumps(["SHOULDER_IMPINGEMENT_ACUTE", "CERVICAL_SPINE"]),
            "Sit upright with dumbbells at shoulder height, palms forward or neutral. Press weights overhead until arms are fully extended. Lower with control back to shoulders.",
            "Seated posture provides lumbar stability. Keep core braced.",
            3, 1, 1,
            "animations/exercise_db_overhead_press.json",
            "thumbnails/exercise_db_overhead_press.png"
        ),
        (
            "ex_lateral_raise_db",
            "Dumbbell Lateral Raise",
            "STRENGTH",
            "ISOLATION",
            "Lateral Deltoids",
            json.dumps(["Supraspinatus", "Trapezius"]),
            "DUMBBELL",
            1,
            1.8,
            json.dumps(["SHOULDER_IMPINGEMENT_ACUTE"]),
            "Stand tall with light dumbbells at sides. Raise arms out to sides with slight elbow bend until parallel with floor (in scapular plane, 30 deg forward). Lower slowly.",
            "Move in the scapular plane (slightly in front of the body) to prevent subacromial impingement.",
            3, 1, 1,
            "animations/exercise_lateral_raise_db.json",
            "thumbnails/exercise_lateral_raise_db.png"
        ),

        # ARMS (BICEPS / TRICEPS)
        (
            "ex_db_bicep_curl",
            "Dumbbell Bicep Curl",
            "STRENGTH",
            "ISOLATION",
            "Biceps",
            json.dumps(["Brachialis", "Forearms"]),
            "DUMBBELL",
            1,
            1.5,
            json.dumps([]),
            "Hold dumbbells at sides with palms forward. Keeping elbows pinned at sides, curl weights up toward shoulders. Squeeze at top, then lower with control.",
            "Avoid swinging the torso to generate momentum.",
            3, 1, 1,
            "animations/exercise_db_bicep_curl.json",
            "thumbnails/exercise_db_bicep_curl.png"
        ),
        (
            "ex_overhead_tricep_ext",
            "Dumbbell Overhead Triceps Extension",
            "STRENGTH",
            "ISOLATION",
            "Triceps",
            json.dumps(["Anconeous"]),
            "DUMBBELL",
            1,
            1.8,
            json.dumps(["ELBOW_TENDINITIS"]),
            "Hold a dumbbell with both hands overhead. Lower the dumbbell behind head by bending at elbows while keeping upper arms vertical. Extend back to top.",
            "Targets long head of triceps. Keep ribs pulled down to prevent hyperextending lower back.",
            3, 1, 1,
            "animations/exercise_overhead_tricep_ext.json",
            "thumbnails/exercise_overhead_tricep_ext.png"
        ),

        # CORE
        (
            "ex_plank",
            "Front Forearm Plank",
            "STRENGTH",
            "CORE",
            "Rectus Abdominis",
            json.dumps(["Transverse Abdominis", "Glutes", "Shoulders"]),
            "BODYWEIGHT",
            1,
            1.8,
            json.dumps([]),
            "Rest on forearms and toes with elbows directly below shoulders. Squeeze glutes and brace core, keeping body in a rigid straight line from head to heels.",
            "Do not let hips sag or pike up. Focus on steady diaphragmatic breathing.",
            0, 45, 0, # Isometric duration
            "animations/exercise_plank.json",
            "thumbnails/exercise_plank.png"
        ),
        (
            "ex_deadbug",
            "Deadbug",
            "MOBILITY",
            "CORE",
            "Transverse Abdominis",
            json.dumps(["Rectus Abdominis", "Hip Flexors"]),
            "BODYWEIGHT",
            1,
            1.4,
            json.dumps([]),
            "Lie on back with arms pointing to ceiling and knees bent at 90 degrees above hips. Slowly lower right arm and left leg toward floor while pressing lower back flat. Return and alternate sides.",
            "Lower back must stay glued to the floor throughout the entire movement.",
            3, 1, 2,
            "animations/exercise_deadbug.json",
            "thumbnails/exercise_deadbug.png"
        ),

        # CARDIO & CONDITIONING
        (
            "ex_jumping_jacks",
            "Jumping Jacks (Interval Cardio)",
            "CARDIO",
            "CARDIO_INTERVAL",
            "Cardiovascular System",
            json.dumps(["Calves", "Deltoids", "Core"]),
            "BODYWEIGHT",
            1,
            2.2,
            json.dumps(["ANKLE_INJURY_ACUTE", "KNEE_PAIN_SEVERE"]),
            "Jump feet out wide while swinging arms overhead to clap. Jump feet back together while lowering arms to sides. Maintain light, rhythmic bouncing on balls of feet.",
            "Land softly with slightly bent knees to absorb impact.",
            1, 0, 1,
            "animations/exercise_jumping_jacks.json",
            "thumbnails/exercise_jumping_jacks.png"
        ),
        (
            "ex_high_knees",
            "High Knees Running in Place",
            "CARDIO",
            "CARDIO_INTERVAL",
            "Cardiovascular System",
            json.dumps(["Hip Flexors", "Quadriceps", "Calves"]),
            "BODYWEIGHT",
            2,
            3.2,
            json.dumps(["KNEE_PAIN_SEVERE", "ANKLE_INJURY_ACUTE"]),
            "Run in place, driving knees up toward chest at a rapid pace while pumping arms in rhythm.",
            "Stay tall through torso and drive through the balls of feet.",
            1, 0, 1,
            "animations/exercise_high_knees.json",
            "thumbnails/exercise_high_knees.png"
        ),
        (
            "ex_mountain_climbers",
            "Mountain Climbers",
            "CARDIO",
            "CARDIO_INTERVAL",
            "Cardiovascular System",
            json.dumps(["Core", "Shoulders", "Hip Flexors"]),
            "BODYWEIGHT",
            2,
            3.0,
            json.dumps(["WRIST_PAIN_SEVERE"]),
            "Start in high plank. Alternately drive knees forward toward chest in a rapid running motion while maintaining flat back and stable shoulders.",
            "Keep hips level with shoulders; avoid bouncing hips up and down.",
            1, 0, 1,
            "animations/exercise_mountain_climbers.json",
            "thumbnails/exercise_mountain_climbers.png"
        )
    ]

    cursor.executemany("""
        INSERT INTO exercises (
            id, name, category, movement_pattern, primary_muscle, secondary_muscles_json,
            equipment, tier, fatigue_cost, contraindications_json, instructions, safety_notes,
            tempo_eccentric, tempo_isometric, tempo_concentric, animation_asset_path, thumbnail_asset_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, exercises_data)

    # Insert Substitutions
    substitutions_data = [
        ("ex_push_up", "ex_incline_push_up", -0.7, 0.90),
        ("ex_push_up", "ex_db_floor_press", 0.5, 0.85),
        ("ex_goblet_squat", "ex_bodyweight_squat", -0.8, 0.95),
        ("ex_pull_up", "ex_dumbbell_row", -1.6, 0.80),
        ("ex_romanian_deadlift_db", "ex_glute_bridge", -2.0, 0.75),
        ("ex_db_overhead_press", "ex_lateral_raise_db", -1.6, 0.70),
        ("ex_high_knees", "ex_jumping_jacks", -1.0, 0.85)
    ]

    cursor.executemany("""
        INSERT INTO exercise_substitutions (
            original_exercise_id, substitute_exercise_id, fatigue_difference, biomechanical_similarity
        ) VALUES (?, ?, ?, ?)
    """, substitutions_data)

    # Insert Form Cues for SRS
    form_cues = [
        ("cue_squat_knees", "ex_bodyweight_squat", "Knee Tracking", "Knees track over 2nd and 3rd toes", "ECCENTRIC", "Knees caving inward (valgus collapse)", "Actively push knees outward against an imaginary band"),
        ("cue_squat_chest", "ex_bodyweight_squat", "Upright Torso", "Chest proud, spine neutral", "ISOMETRIC", "Excessive forward torso lean", "Pick a fixed eye-level focus point in front of you"),
        ("cue_pushup_elbows", "ex_push_up", "Elbow Tuck Angle", "Keep elbows at 45 degrees to torso", "ECCENTRIC", "Flaring elbows out to 90 degrees", "Create an arrow shape with head and elbows, not a T-shape"),
        ("cue_pushup_core", "ex_push_up", "Plank Alignment", "Glutes clenched, abs tight", "ISOMETRIC", "Lumbar sagging / hip drop", "Brace stomach as if expecting a punch before initiating descent"),
        ("cue_rdl_hips", "ex_romanian_deadlift_db", "Hip Hinge Depth", "Push hips straight back to wall", "ECCENTRIC", "Squatting down and bending knees excessively", "Think of closing a car door behind you with your glutes"),
        ("cue_row_elbow", "ex_dumbbell_row", "Elbow Path", "Drive elbow towards pocket", "CONCENTRIC", "Shrugging weight up toward shoulder with upper trap", "Initiate pull by retracting scapula, then drive elbow to hip")
    ]

    cursor.executemany("""
        INSERT INTO form_cues_srs (
            id, exercise_id, cue_title, cue_description, phase_cue, common_fault, correction_strategy
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, form_cues)

    conn.commit()
    conn.close()
    print(f"Prepackaged database created successfully at: {output_path}")

def generate_manifest(db_path, manifest_path, index_path):
    with open(db_path, "rb") as f:
        db_bytes = f.read()
    
    sha256_hash = hashlib.sha256(db_bytes).hexdigest()
    file_size = len(db_bytes)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM exercises")
    exercise_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM exercise_substitutions")
    sub_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM form_cues_srs")
    cue_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT id, name, category, movement_pattern, equipment, tier FROM exercises ORDER BY tier, name")
    exercise_rows = cursor.fetchall()
    conn.close()

    manifest_data = {
        "dataset_name": "kinetiq_prepackaged_exercises",
        "version": "1.0.0",
        "generated_date": "2026-08-24",
        "file_name": os.path.basename(db_path),
        "sha256_checksum": sha256_hash,
        "file_size_bytes": file_size,
        "metrics": {
            "exercise_count": exercise_count,
            "substitution_count": sub_count,
            "form_cues_srs_count": cue_count
        },
        "license_summary": "CC BY-SA 4.0 (Wger) / CC BY 4.0 (ExerciseDB) / Proprietary Kinetiq Safety Enhancements"
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=2)

    with open(index_path, "w") as f:
        f.write(f"KINETIQ EXERCISE SEED DATABASE INDEX\n")
        f.write(f"Generated: 2026-08-24 | SHA256: {sha256_hash}\n")
        f.write(f"Total Exercises: {exercise_count} | Substitutions: {sub_count} | Form Cues: {cue_count}\n\n")
        f.write(f"{'ID':<26} | {'TIER':<4} | {'CATEGORY':<8} | {'PATTERN':<16} | {'EQUIPMENT':<16} | {'NAME'}\n")
        f.write("-" * 110 + "\n")
        for row in exercise_rows:
            f.write(f"{row[0]:<26} | T{row[5]:<3} | {row[2]:<8} | {row[3]:<16} | {row[4]:<16} | {row[1]}\n")

    print(f"Manifest written to: {manifest_path}")
    print(f"Index written to: {index_path}")


if __name__ == "__main__":
    import shutil
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    d_dir = os.path.join(base_dir, "datasets")
    os.makedirs(d_dir, exist_ok=True)
    tmp_db = "/tmp/prepackaged_exercises.db"
    db_out = os.path.join(d_dir, "prepackaged_exercises.db")
    manifest_out = os.path.join(d_dir, "MANIFEST.json")
    index_out = os.path.join(d_dir, "INDEX.txt")
    
    generate_database(tmp_db)
    shutil.copyfile(tmp_db, db_out)
    generate_manifest(db_out, manifest_out, index_out)
