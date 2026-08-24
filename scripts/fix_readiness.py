import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"
readiness_file = os.path.join(target_dir, "core", "engine", "src", "main", "java", "com", "kinetiq", "fitness", "core", "engine", "ReadinessEngine.kt")

with open(readiness_file, "r") as f:
    code = f.read()

fixed_code = code.replace("if (yesterdayIntensityVolume != null && yesterdayIntensityVolume > 10000.0) {\n            score -= 15\n        }", "if (yesterdayIntensityVolume != null && yesterdayIntensityVolume > 10000.0) {\n            score -= 25\n        }")

with open(readiness_file, "w") as f:
    f.write(fixed_code)

print("ReadinessEngine.kt updated.")
