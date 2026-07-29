from dataclasses import dataclass

from app.services.pii.token import Token
from dataclasses import dataclass


@dataclass
class TokenLine:
    tokens: list
    text: str


class TokenGraph:
    def __init__(self, tokens):
        self.tokens = tokens
        self.lines = []

    def build(self):
        self.lines = []
        grouped = self._group_lines()
        for line_id, line in enumerate(grouped):
            text = self._connect_line(line, line_id)
            self.lines.append(TokenLine(tokens=line, text=text))

        return self

    def _group_lines(self, y_threshold=15):
        tokens = sorted(
            self.tokens,
            key=lambda t: (
                t.y1,
                t.x1,
            ),
        )

        lines = []
        current = []
        current_y = None

        for token in tokens:
            center = token.center_y

            if current_y is None:
                current.append(token)
                current_y = center
                continue

            if abs(center - current_y) <= y_threshold:
                current.append(token)

                current_y = (current_y * (len(current) - 1) + center) / len(current)

            else:
                lines.append(current)

                current = [token]
                current_y = center

        if current:
            lines.append(current)

        return lines

    def _connect_line(self, tokens, line_id):
        tokens.sort(key=lambda t: t.x1)

        parts = []
        position = 0
        for index, token in enumerate(tokens):
            token.start = position
            token.line_id = line_id
            parts.append(token.normalized)

            position += len(token.normalized)
            token.end = position

            if index != len(tokens) - 1:
                position += 1

            token.previous = tokens[index - 1] if index > 0 else None
            token.next = tokens[index + 1] if index < len(tokens) - 1 else None

        return " ".join(parts)
