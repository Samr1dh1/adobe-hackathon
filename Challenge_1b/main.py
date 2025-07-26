import os
import json
from datetime import datetime
from src.extractor.pdf_reader import extract_all_documents
from src.extractor.chunker import split_chunks
from src.extractor.relevance_scorer import score_relevance
from src.extractor.summarizer import summarize_chunks
from src.extractor.json_builder import build_json

INPUT_ROOT = "/app/input"
OUTPUT_ROOT = "/app/output"

def process_collection(collection_path, output_path):
    input_json = os.path.join(collection_path, "challenge1b_input.json")
    pdf_folder = os.path.join(collection_path, "PDFs")

    if not os.path.exists(input_json) or not os.path.exists(pdf_folder):
        print(f"⚠️  Skipping {collection_path} — input.json or PDFs folder missing.")
        return

    print(f"📂 Processing: {collection_path}")
    with open(input_json, "r", encoding="utf-8") as f:
        instructions = json.load(f)

    persona_text = instructions["persona"]["role"]
    task_text = instructions["job_to_be_done"]["task"]

    chunks = extract_all_documents(pdf_folder)
    print(f"🔍 Extracted {len(chunks)} chunks")

    refined_chunks = split_chunks(chunks)
    print(f"✂️ Refined to {len(refined_chunks)} chunks")

    filtered_chunks = score_relevance(refined_chunks, persona_text, task_text)

    summarized_chunks = summarize_chunks(filtered_chunks, persona_text, task_text)

    final_json = build_json(instructions, summarized_chunks)

    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, "challenge1b_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2, ensure_ascii=False)
    print(f"✅ Output saved to {output_file}\n")

def main():
    print("🔄 Running Challenge 1B collections batch processor...\n")
    for name in os.listdir(INPUT_ROOT):
        collection_path = os.path.join(INPUT_ROOT, name)
        if os.path.isdir(collection_path):
            output_path = os.path.join(OUTPUT_ROOT, name)
            process_collection(collection_path, output_path)
    print("🎉 All collections processed.")

if __name__ == "__main__":
    main()
