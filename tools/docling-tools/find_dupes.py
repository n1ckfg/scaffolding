import os
import hashlib

root_dir = "."
office_exts = {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}

deleted_files = []

print("Phase 1: Removing MS Office files that have a PDF duplicate in the same folder...")
for dirpath, dirnames, filenames in os.walk(root_dir):
    base_map = {}
    for f in filenames:
        base, ext = os.path.splitext(f)
        ext = ext.lower()
        if base not in base_map:
            base_map[base] = []
        base_map[base].append((ext, f))
    
    for base, files in base_map.items():
        exts = [e for e, _ in files]
        if ".pdf" in exts:
            for e, f in files:
                if e in office_exts:
                    full_path = os.path.join(dirpath, f)
                    try:
                        os.remove(full_path)
                        deleted_files.append(full_path)
                    except Exception as ex:
                        print(f"Error deleting {full_path}: {ex}")

if deleted_files:
    print(f"Deleted {len(deleted_files)} files:")
    for df in deleted_files:
        print("  - " + df)
else:
    print("No matching MS Office duplicates found.")

print("\nPhase 2: Scanning for duplicate files by content...")

def get_hash(filepath):
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None

hashes = {}

for dirpath, dirnames, filenames in os.walk(root_dir):
    for f in filenames:
        if f == ".DS_Store": continue
        if f == "find_dupes.py": continue
        full_path = os.path.join(dirpath, f)
        if not os.path.isfile(full_path): continue
        h = get_hash(full_path)
        if h:
            if h in hashes:
                hashes[h].append(full_path)
            else:
                hashes[h] = [full_path]

found_dupes = False
for h, paths in hashes.items():
    if len(paths) > 1:
        found_dupes = True
        print(f"\nIdentical files (MD5: {h}):")
        for p in paths:
            print(f"  {p}")

if not found_dupes:
    print("No identical files found.")

