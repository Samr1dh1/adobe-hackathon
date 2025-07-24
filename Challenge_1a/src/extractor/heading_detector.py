from collections import Counter

def cluster_font_sizes(font_sizes, precision=1):
    rounded = [round(size, precision) for size in font_sizes]
    counts = Counter(rounded)
    sorted_sizes = sorted(counts.items(), key=lambda x: (-x[0], -x[1]))
    return [size for size, _ in sorted_sizes]

def detect_headings(pages_data):
    font_sizes = [item["font_size"] for page in pages_data for item in page]
    clusters = cluster_font_sizes(font_sizes)

    if not clusters:
        return "Untitled", []

    title_font = clusters[0]
    heading_fonts = clusters[1:]

    title = None
    outline = []
    seen_headings = set()

    for page_index, page in enumerate(pages_data):
        for item in page:
            text = item["text"]
            font_size = item["font_size"]
            page_number = item["page"]
            y = item["y"]
            is_bold = item.get("bold", False)
            is_caps = item.get("caps", False)

            if page_index == 0 and font_size == title_font and not title and y < 200:
                title = text

            if font_size in heading_fonts and len(text) < 80:
                level_idx = heading_fonts.index(font_size) + 1
                level_idx = min(level_idx, 6)  # Cap to H6
                level = f"H{level_idx}"
                key = (text, level, page_number)
                if key not in seen_headings:
                    outline.append({"level": level, "text": text, "page": page_number})
                    seen_headings.add(key)

    return title or "Untitled", outline
