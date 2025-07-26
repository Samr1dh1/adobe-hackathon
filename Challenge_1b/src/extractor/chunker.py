def split_chunks(blocks, max_length=500):
    refined_chunks = []
    for block in blocks:
        text = block["text"]
        if len(text) <= max_length:
            refined_chunks.append(block)
        else:
            parts = text.split(". ")
            chunk = ""
            for part in parts:
                if len(chunk) + len(part) < max_length:
                    chunk += part + ". "
                else:
                    refined_chunks.append({**block, "text": chunk.strip()})
                    chunk = part + ". "
            if chunk:
                refined_chunks.append({**block, "text": chunk.strip()})
    return refined_chunks
