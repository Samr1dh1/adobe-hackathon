import os
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from src.extractor.pdf_reader import extract_pdf_data
from src.extractor.heading_detector import detect_headings
from src.extractor.outline_builder import build_outline

MAX_WORKERS = min(8, os.cpu_count())

def process_single_pdf(pdf_file, output_dir):
    try:
        pages_data = extract_pdf_data(str(pdf_file))
        title, outline = detect_headings(pages_data)
        result = build_outline(title, outline)

        for item in result["outline"]:
            item["level"] = str(item["level"])
            item["text"] = str(item["text"])
            item["page"] = int(item["page"])

        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Processed {pdf_file.name} -> {output_file.name}")

    except Exception as e:
        print(f"Failed to process {pdf_file.name}: {e}")

def process_pdf_wrapper(args):
    return process_single_pdf(*args)

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in /app/input.")
        return

    args = [(pdf_file, output_dir) for pdf_file in pdf_files]

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_pdf_wrapper, args)

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs()
    print("Completed processing pdfs")
