from datetime import datetime
from src.extractor.title_generator import extract_section_title

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
    for chunk in chunks:
        doc = chunk["document"]
        title = extract_section_title(chunk["text"])  # ✅ clean title

        if title not in seen_titles:
            output["extracted_sections"].append({
                "document": doc,
                "section_title": title,
                "importance_rank": len(seen_titles) + 1,
                "page_number": chunk["page_number"]
            })
            seen_titles.add(title)

        output["subsection_analysis"].append({
            "document": doc,
            "refined_text": chunk["summary"],
            "page_number": chunk["page_number"]
        })

    return output
