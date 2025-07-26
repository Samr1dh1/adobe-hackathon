import re
import string

def preprocess(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    return text

def summarize_chunks(chunks, persona_text, task_text, max_lines=3, max_length=400):
    """
    Generate persona-task-aware extractive summaries.
    Picks lines overlapping most with persona/job context.
    """
    context_words = set(preprocess(persona_text).split()) | set(preprocess(task_text).split())
    summarized = []

    for chunk in chunks:
        text = chunk["text"]
        lines = re.split(r'\.\s+|\n', text)  # split on sentence end or newlines
        scored = sorted(
            lines,
            key=lambda line: -len(set(preprocess(line).split()) & context_words)
        )
        # pick top lines and clean
        selected = [line.strip("-• ").strip() for line in scored[:max_lines] if line.strip()]
        summary = ". ".join(selected).strip()[:max_length]

        chunk["summary"] = summary
        summarized.append(chunk)

    return summarized
