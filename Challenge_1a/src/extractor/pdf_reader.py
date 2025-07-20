import fitz # PyMuPDF

def extract_pdf_data(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []
    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_data = []
    
        for block in blocks:
            for line in block.get("lines", []):
                # print(line)
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        page_data.append({
                            "text": text,
                            "font_size": span["size"],
                            "font": span["font"],
                            "bold": "Bold" in span["font"],  
                            "caps": text.isupper(),
                            "y": span["bbox"][1],
                            "page": page_number
                        })
        pages_data.append(page_data)
    return pages_data