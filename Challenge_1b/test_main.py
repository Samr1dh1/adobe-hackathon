# test_main.py

from src.extractor.pdf_reader import extract_all_documents

pdf_folder = "input/PDFs"
chunks = extract_all_documents(pdf_folder)

for c in chunks[:5]:
    print(f"[{c['document']} - Page {c['page_number']}] → {c['text'][:80]}...")
