import sys
import subprocess
import os
import json

def generate_svg_local(input_file, output_file):
    """
    Converts Mermaid text to SVG using the local mermaid-cli (mmdc).
    Requires 'mmdc' or 'npx @mermaid-js/mermaid-cli' to be available.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)

    # Create a mermaid config file to allow large graphs
    config_file = "mermaid-config.json"
    with open(config_file, "w") as f:
        json.dump({"maxEdges": 5000}, f)

    # Try to use 'mmdc' if installed globally, otherwise try npx
    commands = [
        ["mmdc", "-i", input_file, "-o", output_file, "-c", config_file],
        ["npx", "--yes", "-p", "@mermaid-js/mermaid-cli", "mmdc", "-i", input_file, "-o", output_file, "-c", config_file]
    ]

    success = False
    for cmd in commands:
        try:
            print(f"Trying command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Successfully generated {output_file}")
            success = True
            break
        except FileNotFoundError:
            # Command not found
            continue
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(f"Error output: {e.stderr}")
            continue

    # Clean up config file
    if os.path.exists(config_file):
        os.remove(config_file)

    if not success:
        print("\nFailed to generate SVG. Please ensure Mermaid CLI is installed.")
        print("You can install it globally via: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 mermaid_to_svg.py <input.mermaid> <output.svg>")
        sys.exit(1)
        
    generate_svg_local(sys.argv[1], sys.argv[2])
