import json
import os
from src.extractor.json_builder import build_json

# Choose challenge
challenge = "Challenge1"  # or "Challenge2"
input_dir = f"input/{challenge}/"
pdf_dir = os.path.join(input_dir, "PDFs")
instruction_path = os.path.join(input_dir, f"challenge1b_input.json")
output_path = f"output/{challenge}/challenge1b_output.json"

# Load instructions
with open(instruction_path, "r") as f:
    instructions = json.load(f)

# Load summaries (already preprocessed chunks)
chunk_path = f"output/{challenge}/challenge1b_chunks.json"
with open(chunk_path, "r") as f:
    chunks = json.load(f)

# Extract document names
filenames = sorted({chunk["document"] for chunk in chunks})

# Build output
output_json = build_json(instructions, chunks, filenames)

# Save result
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(output_json, f, indent=2)

print(f"✅ Output saved to {output_path}")
