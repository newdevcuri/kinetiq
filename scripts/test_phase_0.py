import unittest
import sqlite3
import json
import os
import hashlib

class TestKinetiqDatabaseAndSchema(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/working_dir/c_4f0cf643cbef2d9c"
        self.db_path = os.path.join(self.base_dir, "datasets", "prepackaged_exercises.db")
        self.manifest_path = os.path.join(self.base_dir, "datasets", "MANIFEST.json")
        self.index_path = os.path.join(self.base_dir, "datasets", "INDEX.txt")

    def test_database_exists_and_matches_manifest(self):
        self.assertTrue(os.path.exists(self.db_path), "Seed database must exist")
        self.assertTrue(os.path.exists(self.manifest_path), "Manifest must exist")
        
        with open(self.manifest_path, "r") as f:
            manifest = json.load(f)
            
        with open(self.db_path, "rb") as f:
            computed_sha = hashlib.sha256(f.read()).hexdigest()
            
        self.assertEqual(manifest["sha256_checksum"], computed_sha, "Manifest SHA256 must match database file hash exactly")

    def test_exercise_data_integrity(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Total exercises count
        cursor.execute("SELECT COUNT(*) FROM exercises")
        count = cursor.fetchone()[0]
        self.assertGreaterEqual(count, 15, "Database must contain at least 15 home-gym exercises")
        
        # 2. Check no empty or null essential fields
        cursor.execute("""
            SELECT id, name, category, movement_pattern, primary_muscle, equipment, 
                   tempo_eccentric, tempo_isometric, tempo_concentric,
                   animation_asset_path, safety_notes
            FROM exercises
        """)
        rows = cursor.fetchall()
        for row in rows:
            for i, val in enumerate(row):
                self.assertIsNotNone(val, f"Field {i} in exercise {row[0]} should not be None")
                if isinstance(val, str):
                    self.assertNotEqual(val.strip(), "", f"Field {i} in exercise {row[0]} should not be empty")

        # 3. Check tri-phasic tempo values are positive or zero
        for row in rows:
            self.assertGreaterEqual(row[6], 0)
            self.assertGreaterEqual(row[7], 0)
            self.assertGreaterEqual(row[8], 0)

        # 4. Check license attribution table
        cursor.execute("SELECT COUNT(*) FROM exercise_license_meta")
        license_count = cursor.fetchone()[0]
        self.assertGreaterEqual(license_count, 2, "License metadata must contain Wger and ExerciseDB entries")

        # 5. Check substitutions table
        cursor.execute("SELECT COUNT(*) FROM exercise_substitutions")
        sub_count = cursor.fetchone()[0]
        self.assertGreaterEqual(sub_count, 5, "Substitutions graph must contain at least 5 links")

        conn.close()

    def test_lottie_animations_exist_and_valid_json(self):
        anim_dir = os.path.join(self.base_dir, "app", "src", "main", "assets", "animations")
        self.assertTrue(os.path.exists(anim_dir), "Animation assets directory must exist")
        
        required_anims = [
            "exercise_bodyweight_squat.json",
            "exercise_push_up.json",
            "exercise_plank.json",
            "exercise_dumbbell_row.json",
            "exercise_jumping_jacks.json"
        ]
        
        for anim in required_anims:
            p = os.path.join(anim_dir, anim)
            self.assertTrue(os.path.exists(p), f"Animation {anim} must exist")
            with open(p, "r") as f:
                data = json.load(f)
                self.assertIn("layers", data, f"Lottie file {anim} must have layers")
                self.assertIn("fr", data, f"Lottie file {anim} must have frame rate")

if __name__ == "__main__":
    unittest.main(verbosity=2)
