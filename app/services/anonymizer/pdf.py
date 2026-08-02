from app.services.processor import process_frame
from app.services.video_state import VideoState


def anonymize_pdf(document, targets, mode):
    for page in document:
        state = VideoState()
        process_frame(page.image, state, targets, mode)

        return document
