from app.services.pii.token import Token


class TokenGraph:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

    def build(self):
        lines = self._group_lines()
        for line_id, line in enumerate(lines):
            self._connect_line(
                line,
                line_id,
            )

        return self.tokens

    def _group_lines(
        self,
        y_threshold=15,
    ):
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

    def _connect_line(
        self,
        tokens,
        line_id,
    ):
        tokens.sort(key=lambda t: t.x1)

        for index, token in enumerate(tokens):
            token.line_id = line_id

            if index > 0:
                token.previous = tokens[index - 1]

            if index < len(tokens) - 1:
                token.next = tokens[index + 1]
