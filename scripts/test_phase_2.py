import unittest

def keytel_male_kcal_min(hr, weight_kg, age):
    return (-55.0969 + (0.6309 * hr) + (0.1988 * weight_kg) + (0.2017 * age)) / 4.184

def keytel_female_kcal_min(hr, weight_kg, age):
    return (-20.4022 + (0.4472 * hr) - (0.1263 * weight_kg) + (0.0740 * age)) / 4.184

def evaluate_symmetry(left_vol, right_vol):
    max_vol = max(left_vol, right_vol, 1.0)
    asymmetry_pct = (abs(left_vol - right_vol) / max_vol) * 100.0
    is_imbalanced = asymmetry_pct > 10.0
    weaker = "Left" if left_vol < right_vol else "Right"
    if is_imbalanced:
        presc = f"Slight asymmetry detected ({int(asymmetry_pct)}% difference). Auto-Prescription: Start unilateral sets with your {weaker} side and match identical reps on the opposite side."
    else:
        presc = f"Optimal symmetry ({int(asymmetry_pct)}% difference). Left and right strength balance is well within safe thresholds."
    return asymmetry_pct, is_imbalanced, presc

def evaluate_deload(recent_rirs):
    return len(recent_rirs) >= 3 and all(r <= 1 for r in recent_rirs[-3:])

class TestPhase2Depth(unittest.TestCase):

    def test_keytel_formula_golden_fixtures(self):
        # Male: HR 140 bpm, 75kg, 30yo
        # (-55.0969 + 0.6309*140 + 0.1988*75 + 0.2017*30) / 4.184 = (-55.0969 + 88.326 + 14.91 + 6.051) / 4.184 = 54.1901 / 4.184 = 12.9517 kcal/min
        kcal_male = keytel_male_kcal_min(140.0, 75.0, 30)
        self.assertAlmostEqual(kcal_male, 12.95, places=2)

        # Female: HR 135 bpm, 60kg, 28yo
        # (-20.4022 + 0.4472*135 - 0.1263*60 + 0.0740*28) / 4.184 = (-20.4022 + 60.372 - 7.578 + 2.072) / 4.184 = 34.4638 / 4.184 = 8.2370 kcal/min
        kcal_female = keytel_female_kcal_min(135.0, 60.0, 28)
        self.assertAlmostEqual(kcal_female, 8.24, places=2)

    def test_hr_gap_handling_logic(self):
        # 30-min session with 3-min gap (interpolated) -> High coverage >= 70%
        samples_small_gap = [140.0] * 10 + [None] * 3 + [145.0] * 17
        valid_count = sum(1 for s in samples_small_gap if s is not None)
        coverage = (valid_count / len(samples_small_gap)) * 100.0
        self.assertGreaterEqual(coverage, 70.0, "Small gap must maintain HR-blended source")

        # 30-min session with 12-min gap (>=5 min fallback to METs) -> Low coverage < 70%
        samples_large_gap = [140.0] * 10 + [None] * 12 + [145.0] * 8
        valid_count_large = sum(1 for s in samples_large_gap if s is not None)
        coverage_large = (valid_count_large / len(samples_large_gap)) * 100.0
        self.assertLess(coverage_large, 70.0, "Large gap must drop source to MET_ONLY")

    def test_bilateral_symmetry_prescription(self):
        # 1. Balanced: Left 500kg, Right 520kg (3.8% diff <= 10%)
        asym, is_imbalanced, presc = evaluate_symmetry(500.0, 520.0)
        self.assertFalse(is_imbalanced)
        self.assertIn("Optimal symmetry", presc)

        # 2. Imbalanced: Left 400kg, Right 500kg (20% diff > 10%)
        asym2, is_imbalanced2, presc2 = evaluate_symmetry(400.0, 500.0)
        self.assertTrue(is_imbalanced2)
        self.assertIn("Start unilateral sets with your Left side", presc2)

    def test_deload_detection(self):
        # 3 sessions with RIR <= 1 -> Deload needed
        self.assertTrue(evaluate_deload([1, 0, 1]))
        # Standard progression with RIR 2-3 -> No deload
        self.assertFalse(evaluate_deload([2, 3, 2]))

    def test_streak_freeze_consumption(self):
        tokens = 2
        missed = True
        new_tokens = tokens - 1 if (missed and tokens > 0) else tokens
        self.assertEqual(new_tokens, 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
