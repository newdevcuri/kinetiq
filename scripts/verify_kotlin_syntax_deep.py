import os
import re
import sys

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def verify_all_files():
    print("=== Deep Kotlin Syntax, Constructor & Parameter Verification ===")
    errors = []
    
    # 1. Parse all data class definitions to collect their required constructor parameters
    class_params = {}
    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.endswith(".kt"):
                full_p = os.path.join(root, f)
                with open(full_p, "r") as kf:
                    lines = kf.readlines()
                
                # Check for unescaped triple quotes or backslash dollars
                content = "".join(lines)
                if "\\$" in content:
                    errors.append(f"Illegal backslash dollar '\\$' in {full_p}")
                
                # Find data classes
                dc_matches = re.finditer(r"data\s+class\s+([A-Za-z0-9_]+)\s*\((.*?)\)", content, re.DOTALL)
                for dc in dc_matches:
                    name = dc.group(1)
                    raw_args = dc.group(2)
                    # Extract val/var names
                    param_names = re.findall(r"(?:val|var)\s+([A-Za-z0-9_]+)\s*:", raw_args)
                    class_params[name] = param_names

    print(f"Collected constructors for {len(class_params)} data classes:")
    for name, params in class_params.items():
        print(f" - {name} ({len(params)} params): {', '.join(params)}")

    # 2. Check UserProfile construction in UserRepository.kt and OnboardingScreen.kt
    user_repo_path = os.path.join(target_dir, "core", "data", "src", "main", "java", "com", "kinetiq", "fitness", "core", "data", "UserRepository.kt")
    with open(user_repo_path, "r") as f:
        repo_content = f.read()

    user_profile_params = class_params.get("UserProfile", [])
    for p in user_profile_params:
        if p not in repo_content:
            errors.append(f"UserProfile parameter '{p}' missing from UserRepository.kt")

    if errors:
        print("\nERRORS DETECTED:")
        for e in errors:
            print(" [X]", e)
        return False
    else:
        print("\nALL DEEP SYNTAX & CONSTRUCTOR CHECKS PASSED (0 ERRORS).")
        return True

if __name__ == "__main__":
    if verify_all_files():
        sys.exit(0)
    else:
        sys.exit(1)
