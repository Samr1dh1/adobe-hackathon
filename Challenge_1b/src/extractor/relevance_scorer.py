import string
from collections import defaultdict

def preprocess(text):
    """
    Lowercases and removes punctuation from input text.
    """
    return text.lower().translate(str.maketrans('', '', string.punctuation))

def enforce_diversity(chunks, max_per_doc=2, limit=7):
    """
    Enforces diversity by limiting the number of chunks per document.
    Stops after reaching the desired limit.
    """
    doc_count = defaultdict(int)
    final = []
    for chunk in chunks:
        doc = chunk["document"]
        if doc_count[doc] < max_per_doc:
            final.append(chunk)
            doc_count[doc] += 1
        if len(final) >= limit:
            break
    return final

def score_relevance(chunks, persona_text, task_text, top_n=10, max_per_doc=2):
    """
    Scores and selects the top-N relevant and diverse chunks.

    Parameters:
    - chunks: List of chunk dicts with 'text' and 'document'.
    - persona_text: String representing persona role.
    - task_text: String representing job to be done.
    - top_n: Final number of chunks to return.
    - max_per_doc: Max chunks per document allowed.

    Returns:
    - List of top_n chunks, ranked by importance and diversity.
    """
    # Build keyword set
    persona_words = set(preprocess(persona_text).split())
    task_words = set(preprocess(task_text).split())
    context_keywords = persona_words | task_words

    # Score each chunk by keyword overlap
    scored_chunks = []
    for chunk in chunks:
        chunk_text = preprocess(chunk["text"])
        chunk_words = set(chunk_text.split())
        overlap = context_keywords & chunk_words
        score = len(overlap)
        if score > 0:
            chunk["importance"] = score
            scored_chunks.append(chunk)

    # Sort by relevance score
    scored_chunks.sort(key=lambda c: -c["importance"])

    # Enforce diversity across top-N selections
    top_chunks = scored_chunks[:top_n * 2]
    diverse_chunks = enforce_diversity(top_chunks, max_per_doc=max_per_doc, limit=top_n)

    return diverse_chunks
