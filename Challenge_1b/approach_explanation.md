# Challenge 1B – Approach Explanation

This solution for Challenge 1B focuses on extracting the most relevant sections from a collection of PDF documents in response to a given persona and task. The goal is to accurately identify, refine, rank, and summarize the most contextually relevant parts of multiple documents while adhering to strict performance and system constraints.

## 🔍 Step-by-Step Pipeline

### 1. **PDF Parsing**
We start by extracting text content from the input PDFs using `PyMuPDF (fitz)`. The content is segmented into blocks or paragraphs. Each block is associated with its source document and page number, forming an initial set of raw chunks.

### 2. **Chunk Refinement**
Large chunks are split into smaller, readable segments (around 500 characters each) using sentence-based splitting. This ensures manageable context for downstream summarization and relevance evaluation.

### 3. **Relevance Scoring**
Each chunk is scored based on how well it overlaps with keywords from the persona and job-to-be-done. Instead of relying solely on keyword count, we perform token-level preprocessing (lowercasing, punctuation removal, stopword filtering) and apply a weighted overlap strategy. To ensure diversity, we limit how many chunks can be selected from a single document (`max_per_doc`) and enforce a fallback mechanism in case relevance hits are sparse.

### 4. **Summarization**
Top-ranked chunks undergo lightweight extractive summarization. Each chunk is split into sentences, and the most relevant sentences (again based on keyword overlap with persona/task context) are retained and trimmed to 400 characters. This produces refined, focused summaries per chunk.

### 5. **Section Title Inference**
For each chunk, a section title is inferred heuristically. We use the most prominent heading detected on the corresponding page from Challenge 1A output. If no heading is available, a fallback method selects a clean, capitalized line from the top of the text chunk or generates a concise pseudo-title from its content.

### 6. **JSON Output Construction**
The final JSON is constructed as per the schema in `output_schema.json`, with `extracted_sections` and `subsection_analysis` clearly separated. Titles are made unique, ranked by appearance, and the entire output is timestamped.

## ⚙️ Performance & System Design

- All processing is CPU-bound and optimized for ≤10s runtime per 50-page document.
- A lightweight parallel processing pipeline uses `ProcessPoolExecutor` to utilize up to 8 cores.
- No models >200MB are used; the entire codebase is model-free and relies on symbolic heuristics for speed and determinism.

## ✅ Strengths

- Plug-and-play design across both structured and unstructured PDFs
- Consistent results across multilingual, noisy, or formatted data
- Strong diversity control across documents
- Compact and accurate JSON output, tuned to evaluation schema

---

This approach balances interpretability, precision, and speed — making it highly suitable for real-world document processing scenarios within constrained environments.
