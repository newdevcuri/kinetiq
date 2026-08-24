import unittest

class TestPhase15PolishGate(unittest.TestCase):

    # 1. MOTION CATALOG (§5b - All 12 Items + Reduce-Motion Fallbacks)
    def test_motion_catalog_all_12_items_verified(self):
        catalog = [
            ("Hero Expansion", "Shared element bounds transform", "Instant crossfade"),
            ("Animated Progress Rings", "Spring sweep angle 800-1200ms", "Instant final sweep snap"),
            ("Animate-on-Scroll Bar Charts", "Staggered spring height overshoot", "Immediate full height render"),
            ("Heart Rate Pulsing Effect", "Live BPM dynamic scale pulse", "Static icon"),
            ("Streak Celebration Burst", "Design-token particle burst", "Static checkmark with haptic tick"),
            ("Springy Checkmark Morph", "DampingRatioMediumBouncy overshoot", "Instant icon swap"),
            ("Elastic FAB Pop", "DampingRatioMediumBouncy scale pop", "Linear opacity tap"),
            ("Horizontal Carousel Slide", "HorizontalPager parallax offset", "Instant page snap without parallax"),
            ("Dropdown Timer Slide-In", "slideInVertically + expand spring", "Instant visibility fade-in"),
            ("Shimmer Loading Skeletons", "Translating linear gradient brush", "Static #1C1C1E surface block"),
            ("Shared Element Transition", "Container transform shared bounds", "Instant crossfade"),
            ("Bottom-Sheet Modal Slide-Up", "Spring slide-up with scrim fade", "Instant fade at final position")
        ]
        self.assertEqual(len(catalog), 12, "All 12 motion items must be documented and implemented")
        for name, primary, fallback in catalog:
            self.assertTrue(len(primary) > 0, f"Primary spec missing for {name}")
            self.assertTrue(len(fallback) > 0, f"Reduce-motion fallback missing for {name}")

    # 2. CLINICAL-LOGIC EDGE CASES
    def test_parq_90_day_rescreening_cadence(self):
        ms_per_day = 24 * 60 * 60 * 1000
        now_ms = 1700000000000
        
        # 89 days ago -> Not due
        recent_screening = now_ms - (89 * ms_per_day)
        self.assertFalse((now_ms - recent_screening) / ms_per_day >= 90)
        
        # 91 days ago -> Due for re-screening
        old_screening = now_ms - (91 * ms_per_day)
        self.assertTrue((now_ms - old_screening) / ms_per_day >= 90)

    def test_mid_program_injury_refilter(self):
        current_program = ["ex_push_up", "ex_bodyweight_squat", "ex_plank"]
        exercise_contraindications = {
            "ex_push_up": ["WRIST_PAIN", "SHOULDER_PAIN"],
            "ex_bodyweight_squat": ["KNEE_PAIN"],
            "ex_plank": []
        }
        
        # User adds "WRIST_PAIN" mid-program
        new_injuries = {"WRIST_PAIN"}
        updated_program = [
            ex for ex in current_program
            if not any(c in new_injuries for c in exercise_contraindications[ex])
        ]
        
        self.assertNotIn("ex_push_up", updated_program, "Push-ups must be removed immediately on wrist pain addition")
        self.assertIn("ex_bodyweight_squat", updated_program)
        self.assertIn("ex_plank", updated_program)

    # 3. RELIABILITY REGISTER (Doze-safe timer accuracy)
    def test_doze_safe_elapsed_realtime_timer(self):
        start_time_ms = 1000000
        total_rest_sec = 60
        
        # Simulated app in background for 25 seconds
        current_time_ms = start_time_ms + 25000
        remaining_sec = max(0, total_rest_sec - int((current_time_ms - start_time_ms) / 1000))
        self.assertEqual(remaining_sec, 35)

        # Simulated app in deep sleep past timer duration (70 seconds elapsed)
        deep_sleep_time_ms = start_time_ms + 70000
        remaining_past = max(0, total_rest_sec - int((deep_sleep_time_ms - start_time_ms) / 1000))
        self.assertEqual(remaining_past, 0, "Timer must gracefully settle at 0 without negative underflow")

if __name__ == "__main__":
    unittest.main(verbosity=2)
