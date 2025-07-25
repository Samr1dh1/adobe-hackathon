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
        pages = extract_pdf_data(str(pdf_file))
        title, outline = detect_headings(pages)
        result = build_outline(title, outline)

        # enforce types
        for item in result["outline"]:
            item["level"] = str(item["level"])
            item["text"]  = str(item["text"])
            item["page"]  = int(item["page"])

        out_path = output_dir / f"{pdf_file.stem}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Processed {pdf_file.name} → {out_path.name}")
    except Exception as e:
        print(f"Failed {pdf_file.name}: {e}")

def _wrapper(args):
    return process_single_pdf(*args)

def process_pdfs():
    inp = Path("/app/input")
    out = Path("/app/output")
    out.mkdir(parents=True, exist_ok=True)

    pdfs = list(inp.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found.")
        return

    args = [(p, out) for p in pdfs]
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as exe:
        exe.map(_wrapper, args)

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs()
    print("Completed processing pdfs")
