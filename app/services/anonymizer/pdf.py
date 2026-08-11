from app.services.processor import process_frame
from app.services.video_state import VideoState
from app.services.selected_detections import parse_selected_detections


def anonymize_pdf(document, targets, mode, padding):
    for page in document:
        state = VideoState()
        process_frame(page.image, state, targets, mode, padding)

    return document


def anonymize_selected_pdf(document, detections, mode, padding):
    detections_by_page = {}
    for detection in detections:
        page = detection.get("page")
        if page is None:
            continue

        detections_by_page.setdefault(int(page), []).append(detection)

    for page_number, page_detections in detections_by_page.items():
        if page_number < 1 or page_number > len(document):
            continue

        page = document.page(page_number - 1)
        parsed = parse_selected_detections(page_detections)
        state = VideoState()

        process_frame(
            page.image,
            state,
            set(parsed.keys()),
            mode,
            padding,
            initial_detections=parsed,
            allow_detection=False,
        )

    return document
