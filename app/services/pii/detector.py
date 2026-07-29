from .reconstruct import reconstruct
from .regex import detect
from .email import detect_emails
from .phone import detect_phones


def detect_pii(tokens):
    lines = reconstruct(tokens)

    results = []
    results.extend(detect(lines))
    results.extend(detect_emails(tokens))
    results.extend(detect_phones(tokens))

    return results
