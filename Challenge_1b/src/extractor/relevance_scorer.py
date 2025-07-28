from collections import defaultdict
import string
import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def score_relevance(chunks, persona_text, task_text, top_n=10, max_per_doc=2, min_required=5):
    persona_words = set(preprocess(persona_text).split())
    task_words = set(preprocess(task_text).split())
    context_keywords = persona_words | task_words

    # Score chunks
    scored_chunks = []
    for chunk in chunks:
        chunk_text = preprocess(chunk["text"])
        chunk_words = set(chunk_text.split())
        overlap = context_keywords & chunk_words
        score = len(overlap)
        if score > 0:
            chunk["importance"] = score
            scored_chunks.append(chunk)

    # Sort by score
    scored_chunks.sort(key=lambda c: -c["importance"])

    # Diversity enforcement
    doc_count = defaultdict(int)
    diverse_chunks = []
    fallback_chunks = []

    for chunk in scored_chunks:
        doc = chunk["document"]
        if doc_count[doc] < max_per_doc:
            diverse_chunks.append(chunk)
            doc_count[doc] += 1
        else:
            fallback_chunks.append(chunk)
        if len(diverse_chunks) >= top_n:
            break

    # Backfill if not enough
    if len(diverse_chunks) < min_required:
        for chunk in fallback_chunks:
            if chunk not in diverse_chunks:
                diverse_chunks.append(chunk)
            if len(diverse_chunks) >= min_required:
                break

    return diverse_chunks
