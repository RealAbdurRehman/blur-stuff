from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

from .base import BaseDetector
from app.services.pii.detection import Detection
from app.services.pii.types import DetectionType

ENTITY_MAP = {
    "PERSON": DetectionType.PERSON,
    "ORGANIZATION": DetectionType.ORGANIZATION,
    "LOCATION": DetectionType.LOCATION,
    "ADDRESS": DetectionType.ADDRESS,
    "DATE_TIME": DetectionType.DATE,
    "URL": DetectionType.URL,
    "EMAIL_ADDRESS": DetectionType.EMAIL,
    "PHONE_NUMBER": DetectionType.PHONE,
    "CREDIT_CARD": DetectionType.CARD,
    "IPV4": DetectionType.IPV4,
    "IPV6": DetectionType.IPV6,
    "MAC_ADDRESS": DetectionType.MAC,
    "UUID": DetectionType.UUID,
    "IBAN_CODE": DetectionType.IBAN,
    "US_SSN": DetectionType.SSN,
    "PASSPORT": DetectionType.PASSPORT,
    "DRIVER_LICENSE": DetectionType.DRIVER_LICENSE,
    "MEDICAL_LICENSE": DetectionType.MEDICAL_LICENSE,
    "NRP": DetectionType.NRP,
}


MIN_SCORES = {
    "PERSON": 0.35,
    "ORGANIZATION": 0.35,
    "LOCATION": 0.35,
    "ADDRESS": 0.30,
    "DATE_TIME": 0.30,
    "URL": 0.30,
}


class PresidioDetector(BaseDetector):
    def __init__(self):
        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()

        nlp_configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
        }

        provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
        nlp_engine = provider.create_engine()

        self.engine = AnalyzerEngine(nlp_engine=nlp_engine, registry=registry)

    def detect(self, graph):
        detections = []
        for line in graph.lines:
            results = self.engine.analyze(
                text=line.text,
                language="en",
            )

            for result in results:
                detection_type = ENTITY_MAP.get(result.entity_type)
                if detection_type is None:
                    continue

                minimum = MIN_SCORES.get(result.entity_type, 0.5)
                if result.score < minimum:
                    continue

                tokens = [
                    token
                    for token in line.tokens
                    if token.start < result.end and token.end > result.start
                ]

                if not tokens:
                    continue

                detections.append(
                    Detection(
                        type=detection_type,
                        text=line.text[result.start : result.end],
                        tokens=tokens,
                    )
                )

        return detections
