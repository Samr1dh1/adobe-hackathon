import os
from src.extractor.pdf_reader_1a import extract_pdf_data
from src.extractor.heading_detector import detect_headings

def extract_sections_from_pdf(pdf_path):
    """
    Extract section-wise chunks from the PDF using heading detection.
    """
    pages_data = extract_pdf_data(pdf_path)
    title, headings = detect_headings(pages_data)

    # Map of page → all spans on that page
    page_to_spans = {}
    for spans in pages_data:
        for span in spans:
            pg = span["page"]
            page_to_spans.setdefault(pg, []).append(span)

    filename = os.path.basename(pdf_path)
    sections = []

    for i, heading in enumerate(headings):
        page = heading["page"]
        section_title = heading["text"]
        font_size = heading["font_size"]
        y_pos = None

        # Get this heading's span y-position
        for span in page_to_spans.get(page, []):
            if span["text"].strip() == section_title and abs(span["font_size"] - font_size) < 0.1:
                y_pos = span["y"]
                break

        if y_pos is None:
            continue  # skip if we couldn't find matching heading

        # Determine the range: from this heading to next heading
        next_page = headings[i + 1]["page"] if i + 1 < len(headings) else None
        next_y = None
        if next_page == page:
            for span in page_to_spans.get(page, []):
                if span["text"] == headings[i + 1]["text"]:
                    next_y = span["y"]
                    break

        # Gather all spans within the section
        collected = []
        if next_page is not None:
            for pg in range(page, next_page + 1):
                for span in page_to_spans.get(pg, []):
                    if pg == page:
                        if span["y"] > y_pos and (next_y is None or span["y"] < next_y):
                            collected.append(span["text"])
                    elif pg < next_page:
                        collected.append(span["text"])
        else:
            # If no next page, collect from current page onwards
            for pg in range(page, max(page_to_spans.keys()) + 1):
                for span in page_to_spans.get(pg, []):
                    if pg == page:
                        if span["y"] > y_pos:
                            collected.append(span["text"])
                    else:
                        collected.append(span["text"])

        if collected:
            text = " ".join(collected).strip()
            if len(text) > 30:
                sections.append({
                    "document": filename,
                    "page_number": page,
                    "section_title": section_title,
                    "text": text
                })

    return sections

def extract_all_documents(pdf_folder):
    all_sections = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            file_path = os.path.join(pdf_folder, file)
            chunks = extract_sections_from_pdf(file_path)
            all_sections.extend(chunks)
    return all_sections