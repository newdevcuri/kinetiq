import os

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def write_file(rel_path, content):
    full_path = os.path.join(target_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created/Verified: {rel_path}")

# Proguard rules for app
write_file("app/proguard-rules.pro", """# Kinetiq Proguard Rules
-keepattributes *Annotation*
-keepclassmembers class * {
    @androidx.room.Dao *;
    @androidx.room.Database *;
    @androidx.room.Entity *;
}
""")

modules = [
    "core/designsystem",
    "core/database",
    "core/model",
    "core/data",
    "core/engine",
    "core/healthconnect",
    "feature/onboarding",
    "feature/dashboard",
    "feature/train",
    "feature/workout",
    "feature/library",
    "feature/progress"
]

# Ensure consumer-rules.pro and AndroidManifest.xml for every library module
for m in modules:
    write_file(f"{m}/consumer-rules.pro", "# Consumer rules for " + m + "\n")
    write_file(f"{m}/src/main/AndroidManifest.xml", """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
</manifest>
""")

print("All module manifests and proguard rules created successfully.")
