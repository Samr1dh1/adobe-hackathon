# Challenge 1A - PDF Outline Extractor

A high-performance, font-aware system that extracts structured outlines from PDF documents by detecting titles and hierarchical headings (H1–H4), with support for OCR fallback and multilingual text.

## 🚀 Quick Start

### Install Dependencies
```bash
pip install --no-cache-dir -r requirements.txt
```

## 📁 Project Structure

```
Challenge_1a/
├── main.py                     # Entry point (multi-core PDF processor)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition
├── input/                      # PDF input directory
│   └── *.pdf                   # Input PDF files
├── output/                     # JSON output directory
└── src/extractor/              # Core modules
    ├── pdf_reader.py           # Text + OCR extraction
    ├── heading_detector.py     # Title & heading detection logic
    ├── outline_builder.py      # JSON schema construction

```

## 🔧 System Features

### Core Pipeline
1. **Text Extraction**: Uses PyMuPDF to extract structured spans from each page.
2. **OCR Fallback**: Automatically invokes Tesseract for pages with too little extractable text.
3. **Heading Detection**: 
      * Classifies headings by clustering top 4 font sizes (capped at H4).
      * Filters body-sized text and applies bold-text overrides.
      * Poster-style PDFs are handled using relaxed, keyword-based rules.
4. **Output Generation**: Produces a valid ```output_schema.json``` for each input PDF.

### Key Capabilities
- **Bold + Font-Aware Heading Detection**: Leverages both font size and bold styling.
- **Poster Detection**: Detects and handles event flyers and announcements.
- **OCR fallback**: Uses Tesseract when PyMuPDF fails
- **Body Text Filtering**: Removes body-sized spans to reduce false positives.
- **Performance Optimized**: Uses multiprocessing for batch document parsing.

## 📊 Output Format

The system generates a structured JSON output with:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Background and Scope",
      "page": 2
    }
  ]
}
```

## 🛠️ Requirements

- Python 3.8+
- PyMuPDF (fitz)
- Pillow
- pytesseract
- Tesseract OCR (system dependency)

## 🐳 Docker Usage

```bash
# Build the container
docker build --platform linux/amd64 -t challenge-1a .

# Run with mounted volumes
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/:/app/output --network none challenge-1a
```

## 🔍 Troubleshooting

### Common Issues

1. **Import errors**: Run `pip install --no-cache-dir -r requirements.txt` to install dependencies
2. **PDF processing errors**: Check if PDFs are corrupted or password-protected
3. **OCR issues**: Ensure Tesseract is installed on your system
4. **Path errors**: Make sure input/output directories exist

## 📝 Input Format

- Place your PDFs inside the `/input` directory
- The system automatically processes all PDFs in batch.

## 🎯 Performance

- Designed for up to **8 CPU cores**
- Processes 50-page PDFs in ≤ 10 seconds
- No internet or external ML models used (≤ 200MB total size)

## ✅ Evaluation Goals

- **High precision & recall** for heading detection
- **Zero inclusion of body-sized spans**
- **OCR fallback** for minimal text PDFs

Built with ❤️ for the Adobe India Hackathon 2025.