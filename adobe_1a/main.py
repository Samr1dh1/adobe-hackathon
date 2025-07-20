from src.extractor.pdf_reader import extract_pdf_data
from src.extractor.heading_detector import detect_headings
from src.extractor.outline_builder import build_outline

import os
import json
import argparse

def main(pdf_path, output_path):
    # Step 1: Extract text + font data from the PDF
    pages_data = extract_pdf_data(pdf_path)

    # Step 2: Detect title and headings (H1, H2, H3)
    title, outline = detect_headings(pages_data)

    # Step 3: Build the final JSON result
    result = build_outline(title, outline)

    # Step 4: Save the output to a JSON file
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, 'output.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="input/sample.pdf")
    parser.add_argument("--output", default="output/")
    args = parser.parse_args()

    main(args.input, args.output)
