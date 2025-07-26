import re

def extract_section_title(text):
    """
    Heuristically generate a clean section title from a text chunk.
    """
    lines = text.strip().split("\n")
    for line in lines:
        clean = line.strip("-• ").strip()
        if 8 < len(clean) < 80 and clean[0].isupper():
            return clean[:80]
    sentences = re.split(r'\.|\n', text)
    for sentence in sentences:
        clean = sentence.strip("-• ").strip()
        if clean:
            return clean[:80]
    return "Untitled Section"
