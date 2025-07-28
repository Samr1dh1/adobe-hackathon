import os
from concurrent.futures import ProcessPoolExecutor
from src.extractor.pdf_reader_1a import extract_pdf_data
from src.extractor.heading_detector import detect_headings

def extract_sections_from_pdf(pdf_path):
    """
    Extract section-wise chunks from the PDF using heading detection from Challenge 1A.
    """
    pages_data = extract_pdf_data(pdf_path)
    title, headings = detect_headings(pages_data)

    # Map page → all spans on that page
    page_to_spans = {}
    for spans in pages_data:
        for span in spans:
            pg = span["page"]
            page_to_spans.setdefault(pg, []).append(span)

    filename = os.path.basename(pdf_path)
    sections = []

    for i, heading in enumerate(headings):
        page       = heading["page"]
        section_title = heading["text"]
        font_size  = heading.get("font_size", None)
        y_pos      = None

        # Find the y‐position of this heading span
        for span in page_to_spans.get(page, []):
            if span["text"].strip() == section_title and (
               font_size is None or abs(span["font_size"] - font_size) < 0.1):
                y_pos = span["y"]
                break
        if y_pos is None:
            continue

        # Determine next heading boundary
        next_hdr = headings[i+1] if i+1 < len(headings) else None
        next_page = next_hdr["page"] if next_hdr else None
        next_y    = None
        if next_hdr and next_hdr["page"] == page:
            for span in page_to_spans.get(page, []):
                if span["text"] == next_hdr["text"]:
                    next_y = span["y"]
                    break

        # Collect all spans under this heading until the next
        collected = []
        if next_page == page:
            for span in page_to_spans.get(page, []):
                if span["y"] > y_pos and (next_y is None or span["y"] < next_y):
                    collected.append(span["text"])
        else:
            # include remainder of this page
            for span in page_to_spans.get(page, []):
                if span["y"] > y_pos:
                    collected.append(span["text"])
            # plus all subsequent pages until the next heading page
            for pg in range(page+1, next_page or (max(page_to_spans.keys())+1)):
                for span in page_to_spans.get(pg, []):
                    collected.append(span["text"])

        text = " ".join(collected).strip()
        if len(text) > 30:
            sections.append({
                "document":      filename,
                "page_number":   page,
                "section_title": section_title,
                "text":          text
            })

    return sections

def extract_all_documents(pdf_folder):
    """
    Parallelize extract_sections_from_pdf over all PDFs in pdf_folder.
    """
    pdfs = [
        os.path.join(pdf_folder, f)
        for f in os.listdir(pdf_folder)
        if f.lower().endswith(".pdf")
    ]
    max_workers = min(8, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=max_workers) as exe:
        results = exe.map(extract_sections_from_pdf, pdfs)

    # Flatten
    all_sections = []
    for sec_list in results:
        all_sections.extend(sec_list)
    return all_sections
