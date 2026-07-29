import re

PUNCTUATION = r"[.,;:!?\[\]{}]"


def normalize_text(text):
    text = text.strip()
    text = text.lower()

    text = re.sub(rf"^{PUNCTUATION}+|{PUNCTUATION}+$", "", text)
    text = re.sub(r"\s+", " ", text)

    return text
