# Challenge 1A – Approach Explanation

This solution for Challenge 1A is designed to extract a structured outline from PDFs, including a `title` and an `outline` of headings (up to H4). The goal is to maximize heading detection accuracy across various types of PDFs—including structured reports, forms, and posters—while adhering to strict performance constraints.

---

## 📘 Core Approach

### 1. **Text Extraction with Fallback to OCR**
Text is extracted from each PDF using `PyMuPDF` (`fitz`). If a page has very few spans (e.g. in a poster), we fall back to OCR using Tesseract. This ensures that even scanned or visually styled PDFs can be parsed.

### 2. **Document Style Classification**
Each document is classified as either:
- **Poster-style** (single-page, high font size, short lines)
- **Structured** (multi-page with regular formatting)

This classification determines which heading detection strategy to apply.

---

## 🧠 Heading Detection Strategies

### A. **Strict Strategy (for structured documents)**
We cluster font sizes and pick the top 4 sizes (excluding body size) as heading candidates. Headings are detected based on:
- Font size rank (H1–H4)
- Vertical alignment (y-axis binning)
- Text filters (no punctuation endings, word count < 12, capitalization)

We cap the output at H4 and ensure:
- If the body font is among the top 4 sizes, we discard it and smaller ones.
- Headings in the same size as body text are only accepted if they are **bold**, which often indicates section headers.

### B. **Poster Strategy**
For single-page flyers or event posters, we use a keyword-driven approach. Lines are classified into semantic categories like:
- **Date/Time**, **Address**, **Website**, **RSVP**, etc.

These are mapped to H2–H4 levels based on detected keywords and their font sizes. Sorting is done by vertical position on the page.

---

## 🚫 Body Text Filtering
To avoid including paragraphs or body text as headings:
- We calculate average word count for each font size.
- The first font size with average word count > 6 is treated as **body size**.
- We exclude any headings at or below this size unless bolded.

---

## ⚙️ Performance & Constraints
- Full CPU-only pipeline using up to 8 cores
- Processes 50-page PDFs in ≤10 seconds
- Model size ≤200MB (none used)
- Outputs valid JSON conforming to the `output_schema.json`

---

## ✅ Key Strengths
- Handles complex layouts (e.g., nested headings, tables)
- Auto-detects and filters out non-heading body text
- Capable of working across scanned and structured PDFs
- Robust to noisy formatting and inconsistent styles

This makes the solution highly accurate, scalable, and production-ready across diverse PDF datasets.

