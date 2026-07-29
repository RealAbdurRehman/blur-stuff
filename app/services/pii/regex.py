import re


def luhn_check(number):
    digits = [int(d) for d in re.sub(r"\D", "", number)]

    if not (13 <= len(digits) <= 19):
        return False

    checksum = 0
    parity = len(digits) % 2
    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


PATTERNS = {
    "EMAIL": {
        "pattern": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    },
    "PHONE": {
        "pattern": re.compile(
            r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{2,4}(?!\w)"
        ),
    },
    "URL": {
        "pattern": re.compile(r"(?:https?://|www\.)[^\s<>\"']+"),
    },
    "CARD": {
        "pattern": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
        "validator": luhn_check,
    },
    "IPV4": {
        "pattern": re.compile(
            r"\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
            r"(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}\b"
        ),
    },
    "IPV6": {
        "pattern": re.compile(r"\b(?:[0-9A-Fa-f]{1,4}:){2,7}[0-9A-Fa-f]{1,4}\b"),
    },
    "MAC": {
        "pattern": re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b"),
    },
    "UUID": {
        "pattern": re.compile(
            r"\b[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[1-5][0-9a-fA-F]{3}-"
            r"[89abAB][0-9a-fA-F]{3}-"
            r"[0-9a-fA-F]{12}\b"
        ),
    },
    "IBAN": {
        "pattern": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"),
    },
    "SSN": {
        "pattern": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    },
}


def detect(lines):
    results = []

    for line in lines:
        text = line["text"]

        for pii_type, config in PATTERNS.items():
            pattern = config["pattern"]
            validator = config.get("validator")

            for match in pattern.finditer(text):
                if validator and not validator(match.group()):
                    continue

                results.append(
                    {
                        "type": pii_type,
                        "text": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "line": line,
                    }
                )

    return results
