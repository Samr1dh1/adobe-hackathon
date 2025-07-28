import os
from datetime import datetime

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
        page = int(float(chunk.get("page_number", 0)))
        title = chunk.get("section_title", "").strip() or "Untitled Section"

        if len(title) > 80:
            title = title[:77] + "..."

        original_title = title
        counter = 1
        while title in seen_titles:
            title = f"{original_title} ({counter})"
            counter += 1

        output["extracted_sections"].append({
            "document": doc,
            "section_title": title,
            "importance_rank": len(seen_titles) + 1,
            "page_number": page
        })
        seen_titles.add(title)

        output["subsection_analysis"].append({
            "document": doc,
            "refined_text": chunk.get("summary", chunk.get("text", "")[:200]),
            "page_number": page
        })

    return output