import os
import subprocess

soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
list_file = "remaining_non_pdf_files.txt"

with open(list_file, "r") as f:
    files = [line.strip() for line in f if line.strip()]

groups = {}
for filepath in files:
    if filepath in (list_file, "convert_to_pdf.py", "delete_dupes.py", "find_dupes.py"):
        continue
    if not os.path.exists(filepath):
        continue
    d = os.path.dirname(filepath)
    if d not in groups:
        groups[d] = []
    groups[d].append(filepath)

total = 0
for d, paths in groups.items():
    print(f"Converting {len(paths)} files in {d}...")
    cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", d] + paths
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"Timeout converting files in {d}")
    except Exception as e:
        print(f"Error: {e}")
        
    for p in paths:
        try:
            os.remove(p)
            total += 1
        except OSError:
            pass

print(f"Conversion and cleanup complete. Removed {total} files.")
