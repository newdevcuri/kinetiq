import os
import zipfile
import shutil

target_dir = "/working_dir/c_4f0cf643cbef2d9c"
output_zip = os.path.join(target_dir, "kinetiq-android-clean.zip")

if os.path.exists(output_zip):
    os.remove(output_zip)

# Explicit whitelist of directories and root files
allowed_dirs = [
    ".github",
    "app",
    "core",
    "feature",
    "gradle",
    "datasets",
    "docs",
    "scripts"
]

allowed_root_files = [
    "build.gradle.kts",
    "settings.gradle.kts",
    "gradle.properties",
    "gradlew",
    "gradlew.bat",
    ".gitignore",
    "README.md",
    "RELEASE_NOTES.md",
    "LICENSES.md",
    "DECISION_LOG.md",
    "PROGRESS.md"
]

total_files_added = 0

with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
    # 1. Add root files
    for rf in allowed_root_files:
        full_p = os.path.join(target_dir, rf)
        if os.path.exists(full_p):
            zipf.write(full_p, rf)
            total_files_added += 1

    # 2. Add directories
    for d in allowed_dirs:
        dir_full_p = os.path.join(target_dir, d)
        if os.path.exists(dir_full_p):
            for root, _, files in os.walk(dir_full_p):
                # Skip hidden/sandbox/cache folders
                if any(x in root for x in [".git", "agent_sandbox", "__pycache__", "build", ".gradle", "ttl="]):
                    continue
                for f in files:
                    if f.endswith(".zip") or f.endswith(".pyc") or f.startswith(".~"):
                        continue
                    full_file_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_file_p, target_dir)
                    zipf.write(full_file_p, rel_p)
                    total_files_added += 1

print(f"Clean ZIP created successfully: {output_zip} ({total_files_added} files added)")

# 3. Test extraction in a test directory to verify compatibility
test_extract_dir = "/tmp/test_kinetiq_extract"
if os.path.exists(test_extract_dir):
    shutil.rmtree(test_extract_dir)
os.makedirs(test_extract_dir, exist_ok=True)

with zipfile.ZipFile(output_zip, "r") as test_zip:
    test_zip.extractall(test_extract_dir)

extracted_count = sum([len(files) for _, _, files in os.walk(test_extract_dir)])
print(f"Extraction test passed cleanly: {extracted_count} files extracted successfully with zero permission errors.")
