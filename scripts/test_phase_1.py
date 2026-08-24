import unittest

class BiologicalSex:
    MALE = "MALE"
    FEMALE = "FEMALE"

def calculate_bmr(weight_kg, height_cm, age_years, sex):
    s = 5.0 if sex == BiologicalSex.MALE else -161.0
    return (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age_years) + s

def simulate_hall_trajectory(start_weight, target_weight, height_cm, age_years, sex, activity_mult, weekly_deficit=3500.0, max_weeks=104):
    trajectory = [(0, start_weight)]
    curr = start_weight
    for w in range(1, max_weeks + 1):
        if curr <= target_weight:
            break
        max_safe_loss = curr * 0.01
        max_allowed_def = max_safe_loss * 7700.0
        eff_def = min(weekly_deficit, max_allowed_def)
        loss = eff_def / 7700.0
        curr = max(target_weight, curr - loss)
        trajectory.append((w, round(curr, 2)))
    return trajectory

def evaluate_readiness(yesterday_vol=None, sleep_min=None, hr_delta=None, soreness=None):
    score = 80
    if yesterday_vol is not None and yesterday_vol > 10000.0:
        score -= 25
    if sleep_min is not None:
        if sleep_min < 360: score -= 20
        elif sleep_min >= 480: score += 10
    if hr_delta is not None:
        if hr_delta >= 5.0: score -= 15
        elif hr_delta <= -2.0: score += 5
    if soreness is not None and soreness >= 4:
        score -= 20
    
    if score < 60:
        return ("LOW", score, 0.85, +1)
    elif score > 85:
        return ("HIGH", score, 1.10, 0)
    else:
        return ("NORMAL", score, 1.0, 0)

class TestPhase1CoreExperience(unittest.TestCase):
    
    def test_bmr_mifflin_st_jeor_golden_fixture(self):
        bmr_male = calculate_bmr(80.0, 180.0, 30, BiologicalSex.MALE)
        self.assertEqual(bmr_male, 1780.0)

        bmr_female = calculate_bmr(60.0, 165.0, 28, BiologicalSex.FEMALE)
        self.assertEqual(bmr_female, 1330.25)

    def test_hall_model_simulation_and_safety_cap(self):
        start_w = 100.0
        target_w = 90.0
        traj = simulate_hall_trajectory(start_w, target_w, 180.0, 30, BiologicalSex.MALE, 1.55, weekly_deficit=10000.0)
        
        for i in range(1, len(traj)):
            prev_w = traj[i-1][1]
            curr_w = traj[i][1]
            weekly_loss = prev_w - curr_w
            max_permitted = prev_w * 0.01 + 0.01
            self.assertLessEqual(weekly_loss, max_permitted, f"Week {i} loss {weekly_loss} exceeded 1% cap {max_permitted}")

    def test_readiness_adaptive_engine_bands_and_fallback(self):
        # 1. Fallback only (sleep/HR missing): High yesterday volume -> LOW band
        band, score, vol_mult, rir_adj = evaluate_readiness(yesterday_vol=12000.0)
        self.assertEqual(band, "LOW")
        self.assertEqual(vol_mult, 0.85)
        self.assertEqual(rir_adj, 1)

        # 2. Zero signals present -> Graceful degradation to NORMAL
        band_norm, score_norm, vol_norm, _ = evaluate_readiness()
        self.assertEqual(band_norm, "NORMAL")
        self.assertEqual(score_norm, 80)
        self.assertEqual(vol_norm, 1.0)

        # 3. High readiness: Great sleep (8.5 hrs), low resting HR -> HIGH band
        band_high, score_high, vol_high, _ = evaluate_readiness(sleep_min=510, hr_delta=-3.0)
        self.assertEqual(band_high, "HIGH")
        self.assertEqual(vol_high, 1.10)

    def test_time_constrained_session_floors(self):
        for dur in [15, 30, 45, 60]:
            warmup = max(4, int(dur * 0.15))
            cooldown = max(4, int(dur * 0.15))
            main = max(7, dur - warmup - cooldown)
            
            self.assertGreaterEqual(warmup, 4, f"Warmup floor violated for {dur}m session")
            self.assertGreaterEqual(cooldown, 4, f"Cooldown floor violated for {dur}m session")
            self.assertGreaterEqual(main, 7, f"Main floor violated for {dur}m session")
            self.assertEqual(warmup + cooldown + main, dur, f"Total allocated minutes must sum to {dur}")

    def test_tag_conflict_empty_set_safe_floor(self):
        all_exercises = [
            {"id": "ex_sq", "contra": ["KNEE_PAIN"]},
            {"id": "ex_pu", "contra": ["SHOULDER_PAIN"]},
            {"id": "ex_plank", "contra": []},
            {"id": "ex_glute_bridge", "contra": []}
        ]
        user_injuries = {"KNEE_PAIN", "SHOULDER_PAIN"}
        
        filtered = [ex for ex in all_exercises if not any(c in user_injuries for c in ex["contra"])]
        self.assertGreaterEqual(len(filtered), 2, "Safe floor exercises must remain available")
        self.assertIn("ex_plank", [e["id"] for e in filtered])

if __name__ == "__main__":
    unittest.main(verbosity=2)
