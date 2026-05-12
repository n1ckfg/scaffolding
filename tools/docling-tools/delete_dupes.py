import os
import hashlib

def get_hash(filepath):
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None

root_dir = "."
hashes = {}

for dirpath, dirnames, filenames in os.walk(root_dir):
    for f in filenames:
        if f == ".DS_Store" or f == "find_dupes.py" or f == "delete_dupes.py": continue
        full_path = os.path.join(dirpath, f)
        if not os.path.isfile(full_path): continue
        h = get_hash(full_path)
        if h:
            if h in hashes:
                hashes[h].append(full_path)
            else:
                hashes[h] = [full_path]

deleted_count = 0
for h, paths in hashes.items():
    if len(paths) > 1:
        # Sort paths to keep the one with the shortest path
        paths.sort(key=lambda x: (len(x), x))
        
        keeper = paths[0]
        # Prefer keeping a file not in a "draft" or "Incorrect" folder
        for p in paths:
            if "draft" not in p.lower() and "incorrect" not in p.lower():
                keeper = p
                break

        for p in paths:
            if p != keeper:
                try:
                    os.remove(p)
                    print(f"Deleted: {p} (Kept: {keeper})")
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {p}: {e}")

print(f"\nTotal exact duplicate files deleted: {deleted_count}")
