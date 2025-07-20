from collections import Counter

def detect_headings(pages_data):
    font_sizes = []
    for page in pages_data:
        for item in page:
            font_sizes.append(item["font_size"])
    
    # Most common sizes → used to guess title and headings
    top_sizes = [size for size, _ in Counter(font_sizes).most_common(4)]
    top_sizes.sort(reverse=True)  # larger = more important
    
    title_font = top_sizes[0]
    h1_font = top_sizes[1] if len(top_sizes) > 1 else title_font
    h2_font = top_sizes[2] if len(top_sizes) > 2 else h1_font
    h3_font = top_sizes[3] if len(top_sizes) > 3 else h2_font
    
    title = None
    outline = []
    
    for page_index, page in enumerate(pages_data):
        for item in page:
            text = item["text"]
            font_size = item["font_size"]
            page_number = item["page"]
            y = item["y"]
    
            if page_index == 0 and font_size == title_font and not title:
                title = text
    
            elif font_size == h1_font and y < 200:
                outline.append({"level": "H1", "text": text, "page": page_number})
            elif font_size == h2_font and y < 300:
                outline.append({"level": "H2", "text": text, "page": page_number})
            elif font_size == h3_font and y < 400:
                outline.append({"level": "H3", "text": text, "page": page_number})
    
    return title or "Untitled", outline