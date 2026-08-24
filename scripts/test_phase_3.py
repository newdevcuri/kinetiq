import unittest
import math
import subprocess

def calc_angle(ax, ay, bx, by, cx, cy):
    v1x, v1y = ax - bx, ay - by
    v2x, v2y = cx - bx, cy - by
    dot = (v1x * v2x) + (v1y * v2y)
    mag1 = math.sqrt(v1x**2 + v1y**2)
    mag2 = math.sqrt(v2x**2 + v2y**2)
    if mag1 * mag2 == 0: return 180.0
    cos_theta = max(-1.0, min(1.0, dot / (mag1 * mag2)))
    return math.degrees(math.acos(cos_theta))

def calc_barbell_plates(target_kg, bar_kg=20.0):
    if target_kg <= bar_kg: return []
    side = (target_kg - bar_kg) / 2.0
    available = [20.0, 15.0, 10.0, 5.0, 2.5, 1.25]
    plates = []
    for p in available:
        while side >= p:
            plates.append(p)
            side -= p
    return plates

class TestPhase3Intelligence(unittest.TestCase):

    def test_pose_joint_angle_calculation(self):
        # 1. Straight leg: Hip(0, 0), Knee(0, 50), Ankle(0, 100) -> 180 deg
        angle_straight = calc_angle(0, 0, 0, 50, 0, 100)
        self.assertAlmostEqual(angle_straight, 180.0, places=1)

        # 2. Right angle knee bend: Hip(0, 50), Knee(50, 50), Ankle(50, 100) -> 90 deg
        angle_90 = calc_angle(0, 50, 50, 50, 50, 100)
        self.assertAlmostEqual(angle_90, 90.0, places=1)

    def test_plate_loading_calculator(self):
        # Target 100kg on 20kg bar -> 40kg per side -> 20kg, 20kg
        plates_100 = calc_barbell_plates(100.0)
        self.assertEqual(plates_100, [20.0, 20.0])

        # Target 82.5kg on 20kg bar -> 31.25kg per side -> 20kg, 10kg, 1.25kg
        plates_82_5 = calc_barbell_plates(82.5)
        self.assertEqual(plates_82_5, [20.0, 10.0, 1.25])

    def test_feature_flag_privacy_defaults(self):
        default_flags = {
            "feature_pose_coach": False,
            "feature_voice_logging": False,
            "feature_p2p_sync": False
        }
        for k, v in default_flags.items():
            self.assertFalse(v, f"Feature {k} must default to false for strict privacy")

    def test_import_integrity_full_repo_check(self):
        res = subprocess.run(["python3", "/working_dir/c_4f0cf643cbef2d9c/scripts/check_import_integrity.py"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Import integrity check failed: {res.stdout}\n{res.stderr}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
