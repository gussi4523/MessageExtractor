def split_text_n_parts(text, n):
    length = len(text)
    part_size = length // n
    parts = []

    for i in range(n):
        start = i * part_size
        # For the last part, take all remaining characters
        if i == n - 1:
            end = length
        else:
            end = (i + 1) * part_size
        parts.append(text[start:end])

    return parts
