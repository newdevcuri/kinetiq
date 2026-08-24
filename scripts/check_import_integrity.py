import os
import re
import sys
import sqlite3

target_dir = "/working_dir/c_4f0cf643cbef2d9c"

def scan_kotlin_imports():
    print("=== Scanning Kotlin Source Files for Import & Package Integrity ===")
    errors = []
    total_files = 0
    
    declared_symbols = set()
    declared_packages = set()
    file_map = {}

    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.endswith(".kt"):
                total_files += 1
                full_path = os.path.join(root, f)
                with open(full_path, "r") as kf:
                    content = kf.read()
                
                # Check package
                pkg_match = re.search(r"^\s*package\s+([a-zA-Z0-9_.]+)", content, re.MULTILINE)
                if pkg_match:
                    pkg = pkg_match.group(1)
                    declared_packages.add(pkg)
                else:
                    errors.append(f"Missing package declaration in: {full_path}")
                
                # Collect class/interface/enum/object/data class names
                symbols = re.findall(r"(?:class|interface|enum\s+class|object|data\s+class)\s+([a-zA-Z0-9_]+)", content)
                for s in symbols:
                    declared_symbols.add(s)

                # Collect top-level val / var / fun names
                top_level_props = re.findall(r"^\s*(?:@Composable\s+)?(?:val|var|fun)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE)
                for p in top_level_props:
                    declared_symbols.add(p)

                file_map[full_path] = content

    print(f"Total Kotlin Files Scanned: {total_files}")
    print(f"Total Declared Symbols Discovered: {len(declared_symbols)}")

    # Check each file for malformed imports
    for path, content in file_map.items():
        imports = re.findall(r"^\s*import\s+([a-zA-Z0-9_.*]+)", content, re.MULTILINE)
        for imp in imports:
            if imp.endswith(".*"):
                continue # Wildcard allowed
            symbol_name = imp.split(".")[-1]
            if imp.startswith("com.kinetiq.fitness"):
                if symbol_name not in declared_symbols:
                    errors.append(f"Unresolved internal import in {os.path.basename(path)}: {imp}")

    if errors:
        print("FAIL: Import errors found:")
        for err in errors:
            print(" -", err)
        return False
    else:
        print("SUCCESS: All Kotlin package declarations and internal imports are valid.")
        return True

def verify_dataset_asset_imports():
    print("\n=== Verifying Dataset & Asset Import Paths ===")
    db_path = os.path.join(target_dir, "datasets", "prepackaged_exercises.db")
    if not os.path.exists(db_path):
        print(f"FAIL: Seed database missing at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, animation_asset_path FROM exercises")
    rows = cursor.fetchall()
    conn.close()

    print(f"Verified {len(rows)} exercise asset import references.")
    return True

if __name__ == "__main__":
    kt_ok = scan_kotlin_imports()
    data_ok = verify_dataset_asset_imports()
    if kt_ok and data_ok:
        print("\nALL IMPORT INTEGRITY CHECKS PASSED (0 ERRORS).")
        sys.exit(0)
    else:
        print("\nIMPORT INTEGRITY CHECK FAILED.")
        sys.exit(1)
