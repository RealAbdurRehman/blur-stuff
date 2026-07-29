from .ocr import OcrDetector
from app.services.pii.graph import TokenGraph
from app.services.pii.detector import detect_pii as detect_pii_words
from app.services.pii.mapper import map_matches

model = OcrDetector()


def detect_pii(image):
    tokens = model.detect(image)
    graph = TokenGraph(tokens)
    tokens = graph.build()
    for token in tokens:
        print(
            token.text,
            "LEFT:",
            token.previous.text if token.previous else None,
            "RIGHT:",
            token.next.text if token.next else None,
            "DIST:",
            token.distance_to_next,
        )

    return map_matches(detect_pii_words(tokens))
