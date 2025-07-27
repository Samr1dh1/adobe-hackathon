import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

# Trigger OCR when a page has too few spans
MIN_SPANS = 3

def ocr_page(pdf_path, page_number):
    """
    Render the page to image and extract text via OCR.
    """
    print(f"[OCR] Falling back to OCR for page {page_number + 1} of {pdf_path}")
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)
    zoom = 2  # 2x scale for better OCR accuracy
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    doc.close()

    img = Image.open(io.BytesIO(pix.tobytes()))
    lines = pytesseract.image_to_string(img).splitlines()

    spans = []
    synthetic_font_size = 40.0  # Make sure this appears at top of cluster
    for i, line in enumerate(lines):
        text = line.strip()
        if not text:
            continue
        spans.append({
            "text": text,
            "font_size": synthetic_font_size,
            "font": "OCR",
            "bold": False,
            "caps": text.isupper(),
            "x": 0.0,
            "y": i * 20.0,
            "page": page_number + 1
        })
    return spans


def extract_pdf_data(pdf_path):
    """
    Extracts structured spans from each page. Uses OCR fallback if PyMuPDF fails.
    """
    doc = fitz.open(pdf_path)
    pages_data = []

    for page_number, page in enumerate(doc, start=0):
        spans = []
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    x0, y0, x1, y1 = span["bbox"]
                    spans.append({
                        "text": text,
                        "font_size": round(span["size"], 1),
                        "font": span["font"],
                        "bold": "Bold" in span["font"],
                        "caps": text.isupper(),
                        "x": round(x0, 1),
                        "y": round(y0, 1),
                        "page": page_number + 1
                    })

        # Fallback to OCR if not enough content
        if len(spans) < MIN_SPANS:
            spans = ocr_page(pdf_path, page_number)

        pages_data.append(spans)

    doc.close()
    return pages_data
