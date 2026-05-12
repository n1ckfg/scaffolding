import os
import shutil

root_dir = "."
skip_files = {".DS_Store", "find_dupes.py", "delete_dupes.py", "convert_to_pdf.py", "remaining_non_pdf_files.txt", "rename_files.py"}

moved_count = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    for f in filenames:
        if f in skip_files:
            continue
        
        full_path = os.path.join(dirpath, f)
        rel_path = os.path.relpath(full_path, root_dir)
        
        # If the file is already in the root directory, it has no parent folders to prefix
        if os.path.dirname(rel_path) == "":
            continue
            
        parts = rel_path.split(os.sep)
        new_name = "__".join(parts)
        new_full_path = os.path.join(root_dir, new_name)
        
        try:
            shutil.move(full_path, new_full_path)
            moved_count += 1
        except Exception as e:
            print(f"Failed to rename {rel_path}: {e}")

print(f"Successfully renamed {moved_count} files, flattening them into the root directory.")
