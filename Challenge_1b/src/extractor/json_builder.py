import os
import sys
import re
from datetime import datetime

# ✅ Fix Python path for Docker
sys.path.append("/app/Challenge_1a/src")

# ✅ Correct imports from Challenge_1a
from extractor.heading_detector import detect_headings
from extractor.pdf_reader import extract_pdf_data  # 🧠 FIXED: was extract_layout before

# 🧠 Heuristic fallback title generator
def extract_section_title(text):
    lines = text.strip().split("\n")
    for line in lines:
        clean = line.strip("-• ").strip()
        if 8 < len(clean) < 80 and clean[0].isupper():
            return clean[:80]
    sentences = re.split(r'\.|\n', text)
    for sentence in sentences:
        clean = sentence.strip("-• ").strip()
        if clean:
            return clean[:80]
    return "Untitled Section"

def build_json(instructions, chunks, filenames):
    output = {
        "metadata": {
            "input_documents": filenames,
            "persona": instructions["persona"]["role"],
            "job_to_be_done": instructions["job_to_be_done"]["task"],
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    seen_titles = set()

    # ✅ Build heading map for each document
    heading_cache = {}
    for fname in filenames:
        try:
            challenge_folder = "Challenge1" if "Challenge1" in instructions["job_to_be_done"]["task"] else "Challenge2"
            pdf_path = os.path.join("input", challenge_folder, "PDFs", fname)

            # ✅ Fixed: use extract_pdf_data not extract_layout
            pages_data = extract_pdf_data(pdf_path)
            _, headings = detect_headings(pages_data)

            heading_map = {h["page"]: h["text"] for h in headings}
            heading_cache[fname] = heading_map
        except Exception as e:
            print(f"⚠️ Failed to extract headings for {fname}: {e}")
            heading_cache[fname] = {}

    # ✅ Process each chunk
    for chunk in chunks:
        doc = chunk["document"]
        page = chunk["page_number"]
        fallback_title = extract_section_title(chunk["text"])
        heading_title = heading_cache.get(doc, {}).get(page, fallback_title)
        title = heading_title.strip()

        if title not in seen_titles:
            output["extracted_sections"].append({
                "document": doc,
                "section_title": title,
                "importance_rank": len(seen_titles) + 1,
                "page_number": page
            })
            seen_titles.add(title)

        output["subsection_analysis"].append({
            "document": doc,
            "refined_text": chunk["summary"],
            "page_number": page
        })

    return output
