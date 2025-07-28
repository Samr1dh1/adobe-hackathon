import os
import json
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.extractor.pdf_reader import extract_all_documents
from src.extractor.chunker import split_chunks
from src.extractor.relevance_scorer import score_relevance
from src.extractor.summarizer import summarize_chunks
from src.extractor.json_builder import build_json

INPUT_ROOT = "input"
OUTPUT_ROOT = "output"

def process_collection(collection_path, output_path):
    input_json = os.path.join(collection_path, "challenge1b_input.json")
    pdf_folder = os.path.join(collection_path, "PDFs")

    if not os.path.exists(input_json) or not os.path.exists(pdf_folder):
        print(f"⚠️  Skipping {collection_path} — challenge1b_input.json or PDFs folder missing.")
        return

    print(f"\n📂 Processing: {collection_path}")
    try:
        with open(input_json, "r", encoding="utf-8") as f:
            instructions = json.load(f)

        persona_text = instructions["persona"]["role"]
        task_text = instructions["job_to_be_done"]["task"]

        chunks = extract_all_documents(pdf_folder)
        print(f"🔍 Extracted {len(chunks)} chunks")

        refined_chunks = split_chunks(chunks)
        print(f"✂️ Refined to {len(refined_chunks)} chunks")

        filtered_chunks = score_relevance(refined_chunks, persona_text, task_text)
        print(f"🎯 Filtered to {len(filtered_chunks)} relevant chunks")

        summarized_chunks = summarize_chunks(filtered_chunks, persona_text, task_text)
        print(f"📝 Summarized {len(summarized_chunks)} chunks")

        # Collect filenames
        filenames = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

        final_json = build_json(instructions, summarized_chunks, filenames)

        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(output_path, "challenge1b_output.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_json, f, indent=2, ensure_ascii=False)
        print(f"✅ Output saved to {output_file}\n")
        
    except Exception as e:
        print(f"❌ Error processing {collection_path}: {str(e)}")

def main():
    print("🔄 Running Challenge 1B collections batch processor...\n")
    
    if not os.path.exists(INPUT_ROOT):
        print(f"❌ Input directory '{INPUT_ROOT}' not found!")
        return
        
    for name in os.listdir(INPUT_ROOT):
        collection_path = os.path.join(INPUT_ROOT, name)
        if os.path.isdir(collection_path):
            output_path = os.path.join(OUTPUT_ROOT, name)
            process_collection(collection_path, output_path)
    print("🎉 All collections processed.")

if __name__ == "__main__":
    main()
