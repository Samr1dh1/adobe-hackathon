import fitz  # PyMuPDF
import os

def extract_chunks_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    chunks = []
    filename = os.path.basename(pdf_path)

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if text and len(text) > 30:
                chunks.append({
                    "document": filename,
                    "page_number": page_number,
                    "text": text
                })

    return chunks

def extract_all_documents(pdf_folder):
    all_chunks = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            file_path = os.path.join(pdf_folder, file)
            print(f"Reading: {file}")
            chunks = extract_chunks_from_pdf(file_path)
            all_chunks.extend(chunks)  # ✅ Flatten the list of chunks
    return all_chunks
