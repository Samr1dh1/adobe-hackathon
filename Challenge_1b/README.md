# Challenge 1B - PDF Document Processor

A comprehensive PDF document processing system that extracts relevant information based on persona and job requirements.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python setup.py
```

### 2. Run the System
```bash
python main.py
```

### 3. Test the System
```bash
python test_system.py
```

## 📁 Project Structure

```
Challenge_1b/
├── main.py                 # Main entry point
├── setup.py               # Setup script
├── test_system.py         # System test script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── input/                # Input challenges
│   ├── Challenge1/
│   │   ├── PDFs/         # PDF documents
│   │   └── challenge1b_input.json
│   └── Challenge2/
│       ├── PDFs/
│       └── challenge1b_input.json
├── output/               # Generated outputs
└── src/extractor/        # Core processing modules
    ├── pdf_reader.py     # PDF text extraction
    ├── chunker.py        # Text chunking
    ├── relevance_scorer.py # Content relevance scoring
    ├── summarizer.py     # Text summarization
    ├── heading_detector.py # Heading detection
    ├── title_generator.py # Section title generation
    ├── json_builder.py   # Output JSON generation
    └── pdf_reader_1a.py  # Advanced PDF processing
```

## 🔧 System Features

### Core Pipeline
1. **PDF Extraction**: Extracts text chunks from PDF documents
2. **Text Chunking**: Splits large text blocks into manageable chunks
3. **Relevance Scoring**: Scores chunks based on persona and task context
4. **Summarization**: Creates focused summaries of relevant content
5. **Heading Detection**: Identifies document structure and headings
6. **Title Generation**: Generates meaningful section titles
7. **JSON Output**: Produces structured output with metadata

### Key Capabilities
- **Multi-document processing**: Handles collections of PDFs
- **Persona-aware filtering**: Tailors extraction to specific roles
- **OCR fallback**: Uses Tesseract when PyMuPDF fails
- **Diversity enforcement**: Ensures variety in extracted content
- **Error handling**: Graceful degradation for problematic files

## 📊 Output Format

The system generates a structured JSON output with:

```json
{
  "metadata": {
    "input_documents": ["file1.pdf", "file2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-01-XX..."
  },
  "extracted_sections": [
    {
      "document": "file1.pdf",
      "section_title": "Travel Planning Guide",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "file1.pdf",
      "refined_text": "Extracted and summarized content...",
      "page_number": 1
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
docker build -t challenge1b .

# Run with mounted volumes
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output challenge1b
```

## 🔍 Troubleshooting

### Common Issues

1. **Import errors**: Run `python setup.py` to install dependencies
2. **PDF processing errors**: Check if PDFs are corrupted or password-protected
3. **OCR issues**: Ensure Tesseract is installed on your system
4. **Path errors**: Make sure input/output directories exist

### Testing

Run the test suite to verify everything works:
```bash
python test_system.py
```

## 📝 Input Format

Each challenge should have:
- `PDFs/` folder containing PDF documents
- `challenge1b_input.json` with persona and task information

Example input JSON:
```json
{
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

## 🎯 Performance

- Processes 3-10 PDFs per challenge
- Extracts 5-10 most relevant sections
- Generates summaries within 400 characters
- Handles various PDF formats and layouts 