import re
from collections import Counter, defaultdict

NUMERIC_PREFIX = re.compile(r"^\d+\.$")

def cluster_font_sizes(font_sizes, precision=1):
    rounded = [round(sz, precision) for sz in font_sizes]
    counts = Counter(rounded)
    ordered = sorted(counts.items(), key=lambda x: (-x[0], -x[1]))
    return [size for size, _ in ordered]

def is_poster(pages_data):
    if len(pages_data) > 1:
        return False
    lines = [it for pg in pages_data for it in pg]
    avg_font = sum(it["font_size"] for it in lines) / max(1, len(lines))
    short_lines = [it for it in lines if len(it["text"].split()) <= 6]
    return avg_font >= 20 or len(short_lines) / len(lines) > 0.8

def detect_headings(pages_data):
    all_sizes = [item["font_size"] for pg in pages_data for item in pg]
    clusters = cluster_font_sizes(all_sizes)
    if not clusters:
        return "Untitled", []

    title_font = clusters[0]
    heading_fonts = clusters[1:5]

    title = None
    first_page = pages_data[0]
    title_cands = [it for it in first_page if it["font_size"] == title_font]
    if title_cands:
        title = min(title_cands, key=lambda it: it["y"])["text"]

    if is_poster(pages_data):
        return detect_headings_poster(pages_data, heading_fonts, title)
    return detect_headings_strict(pages_data, heading_fonts, title)

def detect_headings_strict(pages_data, heading_fonts, title):
    BIN = 5
    buckets = defaultdict(list)
    for pg in pages_data:
        for it in pg:
            sz = it["font_size"]
            if sz not in heading_fonts:
                continue
            lvl = heading_fonts.index(sz) + 1
            yb = int((it["y"] + BIN / 2) // BIN) * BIN
            buckets[(it["page"], lvl, yb)].append(it)

    outline = []
    seen = set()
    for (pg, lvl, yb) in sorted(buckets):
        spans = sorted(buckets[(pg, lvl, yb)], key=lambda it: it["x"])
        text = " ".join(it["text"] for it in spans).strip()
        # --- STRONGER FILTERS ---
        if len(text) < 3 or (pg, text) in seen:
            continue
        if len(text.split()) > 10:  # stricter: max 10 words
            continue
        if text.endswith((".", ":", ";")):
            continue
        if not text[0].isupper():
            continue
        outline.append({
            "level": f"H{lvl}",
            "text": text,
            "page": pg,
            "font_size": heading_fonts[lvl - 1]
        })
        seen.add((pg, text))
    return title or "Untitled", outline

def detect_headings_poster(pages_data, heading_fonts, title):
    import re
    from collections import defaultdict

    KEYWORD_RULES = {
        "date_time": re.compile(r"(date|time|am|pm|july|saturday|sunday)", re.I),
        "address":   re.compile(r"(address|parkway|forge|street|road)", re.I),
        "rsvp":      re.compile(r"(rsvp|contact|call|phone|email|text)", re.I),
        "website":   re.compile(r"(www\.|\.com|topjump)", re.I),
        "waiver":    re.compile(r"(waiver|fill out|form|visit)", re.I),
        "dress_code":re.compile(r"(shoes|required|dress code|wear)", re.I)
    }

    def classify(text):
        for label, regex in KEYWORD_RULES.items():
            if regex.search(text):
                return label
        return None

    BIN = 5
    grouped = defaultdict(list)
    for pg in pages_data:
        for it in pg:
            yb = int((it["y"] + BIN/2) // BIN) * BIN
            grouped[(it["page"], it["font_size"], yb)].append(it)

    outline = []
    seen = set()

    for (pg, sz, yb) in sorted(grouped):
        spans = sorted(grouped[(pg, sz, yb)], key=lambda it: it["x"])
        text = " ".join(it["text"] for it in spans).strip()
        if not text or (pg, text) in seen:
            continue

        category = classify(text)
        if category:
            level = {
                "date_time": "H2",
                "address":   "H3",
                "rsvp":      "H4",
                "website":   "H4",
                "waiver":    "H4",
                "dress_code":"H4"
            }[category]
        elif sz in heading_fonts:
            level = f"H{heading_fonts.index(sz) + 1}"
        else:
            continue

        if len(text) < 3 or len(text.split()) > 20:
            continue

        outline.append({
            "level": level,
            "text":  text,
            "page":  pg,
            "font_size": sz,
            "_y":    yb
        })
        seen.add((pg, text))

    outline.sort(key=lambda it: (it["page"], it["_y"]))

    for it in outline:
        del it["_y"]

    return title or "Untitled", outline