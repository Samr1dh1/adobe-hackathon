import re

def extract_section_title(text):
    """
    Heuristically generate a clean section title from a text chunk.
    """
    # Clean the text
    text = text.strip()
    
    # Split into lines and look for potential headings
    lines = text.split("\n")
    for line in lines:
        clean = line.strip("-• ").strip()
        # Look for lines that could be headings
        if (8 < len(clean) < 80 and 
            clean[0].isupper() and 
            not clean.endswith('.') and
            not clean.endswith(':') and
            len(clean.split()) <= 8):
            return clean[:80]
    
    # If no good heading found, try to extract from first sentence
    sentences = re.split(r'\.\s+|\n', text)
    for sentence in sentences:
        clean = sentence.strip("-• ").strip()
        if clean and len(clean) > 10:
            # Take first part of sentence as title
            words = clean.split()[:6]  # Take first 6 words
            title = " ".join(words)
            if len(title) > 5:
                return title[:80]
    
    # Final fallback
    if text:
        return text[:50] + "..." if len(text) > 50 else text
    return "Untitled Section"
