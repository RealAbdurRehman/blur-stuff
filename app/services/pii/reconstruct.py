def make_line(words):
    words = sorted(words, key=lambda w: w.x1)

    text = ""
    tokens = []

    for word in words:
        if text:
            text += " "

        start = len(text)
        text += word.normalized
        end = len(text)
        tokens.append({"token": word, "start": start, "end": end})

    return {"text": text, "tokens": tokens}


def reconstruct(words, y_threshold=15):
    if not words:
        return []

    words = sorted(words, key=lambda w: (w.y1, w.x1))

    lines = []
    current = []
    current_center = None

    for word in words:
        center = word.center_y

        if current_center is None:
            current.append(word)
            current_center = center
            continue

        if abs(center - current_center) <= y_threshold:
            current.append(word)

            current_center = (current_center * (len(current) - 1) + center) / len(
                current
            )
        else:
            lines.append(make_line(current))

            current = [word]
            current_center = center

    lines.append(make_line(current))

    return lines
