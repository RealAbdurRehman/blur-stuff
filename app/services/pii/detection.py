from dataclasses import dataclass

from .token import Token
from .types import DetectionType


@dataclass(slots=True)
class Detection:
    type: DetectionType
    text: str
    tokens: list[Token]
