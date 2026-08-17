from .ocr import OcrDetector

from app.services.pii.graph import TokenGraph
from app.services.pii.manager import DetectorManager
from app.services.pii.mapper import map_matches

ocr = OcrDetector()
manager = DetectorManager()


def detect_pii(image):
    tokens = ocr.detect(image)
    graph = TokenGraph(tokens).build()
    matches = manager.detect(graph)

    return map_matches(matches)


def unload_pii():
    ocr.unload()
