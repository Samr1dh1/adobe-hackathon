# Adobe India Hackathon 2025 – PDF Processing Suite 🧠📄

This repository is a comprehensive solution for Adobe's India Hackathon 2025, featuring two core challenges:

- **Challenge 1A**: Extracting structured outlines (titles and headings) from a set of unstructured PDFs.
- **Challenge 1B**: Persona- and task-aware content extraction and summarization from a PDF collection.

Both solutions prioritize **accuracy**, **performance**, and **scalability**, with full Docker support and multiprocessing.

---

## 🗂️ Folder Structure

```
.
├── Challenge_1a/           # Challenge 1A: PDF Outline Extractor
│   ├── src/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── Challenge_1b/           # Challenge 1B: PDF Document Processor
│   ├── src/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── input/                  # Input files for both challenges
├── output/                 # Output directory
├── README.md               # 🔹 (This file)
├── approach_explanation_1a.md
├── approach_explanation_1b.md
└── ...
```

---

## 🔗 Quick Links

| Challenge | Description | Link |
|----------|-------------|------|
| 🚀 [Challenge 1A](./Challenge_1a/README.md) | Extract a structured heading outline (title + H1–H4) from raw PDFs using font metadata and OCR fallback. | `Challenge_1a/README.md` |
| 📚 [Challenge 1B](./Challenge_1b/README.md) | Extract relevant and diverse content from multiple PDFs based on user persona and task. Includes summarization, heading detection, and output generation. | `Challenge_1b/README.md` |

---

## 🧰 System Requirements

- Python 3.8+
- Docker (recommended for easy setup)
- Tesseract OCR (`sudo apt install tesseract-ocr`)
- Dependencies in `requirements.txt` inside each challenge folder

---

## 🐳 Docker Usage (Recommended)

### Build and run Challenge 1A

```bash
cd Challenge_1a
docker build --platform linux/amd64 -t challenge-1a .
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/:/app/output --network none challenge-1a
```

### Build and run Challenge 1B

```bash
cd Challenge_1b
docker build --platform linux/amd64 -t challenge-1b .
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/:/app/output --network none challenge-1b
```

---

## 📦 Output Samples

Each challenge generates its respective `*.json` output inside the `/output` directory, following strict schema guidelines provided in the problem statement.

---

## 🧠 Highlights

- 🧩 Modular architecture with reusable components
- ⚡ Multiprocessing for fast batch PDF processing
- 📐 Layout-aware and OCR-resilient
- 🧠 Language-Agnostic Heuristic Parsing (Challenge 1A)
- 🎯 High precision filtering and scoring (Challenge 1B)

---

## 📝 Team Members

Samridhi Tiwari
Email: [tiwarisamridhi1405@gmail.com]
GitHub: [https://github.com/Samr1dh1]

Shouraya Mishra
Email: [shouraya.mishra1604@gmail.com]
GitHub: [https://github.com/Shouraya16]

---

> Made for the Adobe India Hackathon 2025 with ❤️ and a lot of PDFs.