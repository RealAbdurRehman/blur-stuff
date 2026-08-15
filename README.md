<h1 align="center">
  <img
    src="https://raw.githubusercontent.com/RealAbdurRehman/blur-stuff/main/app/frontend/templates/components/icons/logo-white.svg"
    width="35"
    height="35"
    alt="Blur Stuff logo"
    style="vertical-align: bottom;"
  />
  Blur Stuff
</h1>

<p align="center">
  <i>Automatically detect and anonymize sensitive information in images, videos, and documents.</i>
</p>

<p align="center">
  <a href="https://github.com/RealAbdurRehman/blur-stuff" style="text-decoration: none;">
    <img src="https://img.shields.io/github/stars/RealAbdurRehman/blur-stuff?style=flat&logo=github" alt="GitHub Stars">
  </a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.1.3-000000?style=flat&logo=flask&logoColor=white" alt="Flask Version">
  <a href="https://github.com/RealAbdurRehman/blur-stuff/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT">
  </a>
</p>

<p align="center">
  <img src="https://github.com/RealAbdurRehman/blur-stuff/blob/main/screenshots/hero.png" alt="Blur Stuff homepage">
</p>

<p align="center">
  <a href="https://blurstuff.up.railway.app">Website</a>
  &nbsp;&bull;&nbsp;
  <a href="https://blurstuff.up.railway.app/api">API</a>
  &nbsp;&bull;&nbsp;
  <a href="https://blurstuff.up.railway.app/docs">Documentation</a>
</p>

---

## What is Blur Stuff?

**Blur Stuff** is an open-source privacy-focused tool for detecting and anonymizing sensitive information in **images, videos, and documents**.

Instead of manually searching through a file for information that should not be shared, Blur Stuff can automatically detect sensitive regions and apply an anonymization effect to them.

It can detect:

- Faces
- License plates
- Text
- Personally identifiable information (PII)

You can anonymize everything automatically or review detections and choose exactly which regions should be processed.

---

## Why Blur Stuff?

Sharing media can unintentionally expose information that was never meant to be public.

Blur Stuff is designed to make protecting that information simple:

- 🔒 **Privacy-focused** — built around minimizing unnecessary handling of user media
- 🎯 **Selective anonymization** — choose individual detections instead of processing everything
- 🧠 **Automatic detection** — detect faces, plates, text, and PII
- 🎥 **Multi-media support** — images, videos, and documents
- 🎨 **Multiple anonymization effects** — choose how detected information is hidden
- 🔌 **API-first** — use the processing engine from your own applications
- 🚫 **No account required** — core functionality does not require registration
- 🧩 **Open source** — inspect, modify, self-host, and contribute

---

## Features

### Detection

| Target             | Description                                         | Technology     |
| ------------------ | --------------------------------------------------- | -------------- |
| **Faces**          | Detect human faces                                  | YOLO           |
| **License Plates** | Detect vehicle license plates                       | YOLO           |
| **Text**           | Detect visible text                                 | PaddleOCR      |
| **PII**            | Identify potentially sensitive personal information | OCR + Presidio |

### Media Processing

- **Images** — Detect and anonymize sensitive regions in images
- **Videos** — Track detections across video frames
- **Documents** — Process supported documents and PDFs
- **Audio preservation** — Preserve the original audio when processing videos
- **EXIF removal** — Remove image metadata from processed images

### Anonymization

Choose how detected information should be hidden:

- **Pixelate**
- **Blur**
- **Solid**
- **Noise**
- **Emoji**
- **Inpaint**

### Workflow

- Automatic detection
- Selective anonymization
- Adjustable detection padding
- Detection-only API endpoints
- Anonymization API endpoints
- No account required for core functionality

---

## How It Works

Blur Stuff separates **detection** from **anonymization**, allowing applications to inspect detections before deciding what to process.

```text
                    ┌─────────────────┐
                    │      Upload     │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Detect sensitive   │
                  │     information     │
                  └──────────┬──────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
          Faces           Plates        Text / PII
             │               │               │
             └───────────────┼───────────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Review / Select     │
                  │    detections       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Anonymization     │
                  │                     │
                  │ Blur                │
                  │ Pixelate            │
                  │ Solid               │
                  │ Noise               │
                  │ Emoji               │
                  │ Inpaint             │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Anonymized Output  │
                  └─────────────────────┘
```

The API can also be used as a detection service independently of the frontend.

---

## Demo

### Image anonymization

<p align="center">
  <img src="YOUR_IMAGE_DEMO_URL_HERE" alt="Blur Stuff image anonymization">
</p>

### Selective anonymization

<p align="center">
  <img src="YOUR_SELECTIVE_DEMO_URL_HERE" alt="Blur Stuff selective anonymization">
</p>

### Video anonymization

<p align="center">
  <img src="YOUR_VIDEO_DEMO_URL_HERE" alt="Blur Stuff video anonymization">
</p>

> Replace the placeholders above with screenshots or GIFs from the application.

---

## Use Cases

Blur Stuff can be useful anywhere sensitive information needs to be removed before media is shared.

### Journalism

Anonymize faces, license plates, and identifying information before publishing photographs or footage.

### Research

De-identify images, videos, or documents before using them in research or datasets.

### Content Creation

Automatically hide faces, plates, or other sensitive information in photos and video.

### Document Sharing

Detect and anonymize potentially identifying information before sharing documents.

### Development & Testing

Sanitize media before using it in demos, documentation, or development environments.

### Privacy-conscious workflows

Reduce the amount of sensitive information exposed when sharing media with others.

---

## Supported Detection Targets

Use the `targets` parameter to control what Blur Stuff detects.

| Target               | Value    | Description                          |
| -------------------- | -------- | ------------------------------------ |
| Faces                | `faces`  | Human faces                          |
| License plates       | `plates` | Vehicle license plates               |
| Text                 | `text`   | Detected text regions                |
| Personal information | `pii`    | Potentially identifiable information |

Multiple targets can be provided as a comma-separated list:

```text
?targets=faces
?targets=faces,plates
?targets=text
?targets=pii
```

If `targets` is omitted, the API defaults to `faces`.

> `text` and `pii` cannot be used together in the same request.

---

## Anonymization Modes

Blur Stuff supports multiple ways to hide detected information.

| Mode       | Description                                 |
| ---------- | ------------------------------------------- |
| `pixelate` | Pixelates the detected region               |
| `blur`     | Applies a blur effect                       |
| `solid`    | Covers the region with a solid color        |
| `noise`    | Replaces the region with visual noise       |
| `emoji`    | Covers the region with an emoji             |
| `inpaint`  | Attempts to reconstruct the detected region |

Pixelation is the default mode.

```text
?mode=pixelate
?mode=blur
?mode=solid
?mode=noise
?mode=emoji
?mode=inpaint
```

---

## Selective Anonymization

Blur Stuff does not require you to anonymize every detection.

The detection endpoints can first return the regions found in a file. You can then send only the detections you want anonymized to the `anonymize-selected` endpoints.

```text
                ┌──────────────┐
                │     File     │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │    Detect    │
                └──────┬───────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Detection results│
              └────────┬─────────┘
                       │
                 Select regions
                       │
                       ▼
             ┌────────────────────┐
             │ Anonymize selected │
             └──────────┬─────────┘
                        │
                        ▼
                 Anonymized file
```

This is useful when a file contains both information that should remain visible and information that should be hidden.

---

# Quick Start

## Requirements

- Python 3.11+
- `pip`
- Git

## Clone the repository

```bash
git clone https://github.com/RealAbdurRehman/blur-stuff.git
cd blur-stuff
```

## Create a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run Blur Stuff

```bash
python run.py
```

The application will then be available locally.

---

# API

Blur Stuff exposes a reusable REST API for detection and anonymization.

The API is versioned under:

```text
/api/v1/
```

The hosted API base URL is:

```text
https://blurstuff.com/api/v1
```

No API key is currently required.

> For complete request parameters, response schemas, validation rules, and endpoint details, see the [API documentation](https://blurstuff.com/docs).

---

## API Quick Start

### Anonymize an image

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize?targets=faces&mode=pixelate" \
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

### Detect without anonymizing

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/detect?targets=faces,plates" \
  -F "file=@image.jpg"
```

### Anonymize a video

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/videos/anonymize?targets=faces&mode=blur" \
  -F "file=@video.mp4" \
  --output anonymized.mp4
```

### Anonymize a document

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/documents/anonymize?targets=pii&mode=blur" \
  -F "file=@document.pdf" \
  --output anonymized.pdf
```

---

## API Endpoints

### Images

| Method | Endpoint                     | Description                                |
| ------ | ---------------------------- | ------------------------------------------ |
| `POST` | `/images/detect`             | Detect sensitive information               |
| `POST` | `/images/anonymize`          | Detect and anonymize sensitive information |
| `POST` | `/images/anonymize-selected` | Anonymize only supplied detections         |

### Videos

| Method | Endpoint            | Description                                                   |
| ------ | ------------------- | ------------------------------------------------------------- |
| `POST` | `/videos/detect`    | Detect sensitive information across video frames              |
| `POST` | `/videos/anonymize` | Detect and anonymize sensitive information throughout a video |

Video processing tracks detections across frames so that detected objects can continue to be anonymized as they move.

Original audio is preserved during processing.

### Documents

| Method | Endpoint                        | Description                                       |
| ------ | ------------------------------- | ------------------------------------------------- |
| `POST` | `/documents/detect`             | Detect text and potentially sensitive information |
| `POST` | `/documents/anonymize`          | Detect and anonymize sensitive information        |
| `POST` | `/documents/anonymize-selected` | Anonymize only supplied detections                |

### Health

| Method | Endpoint        | Description                                         |
| ------ | --------------- | --------------------------------------------------- |
| `GET`  | `/health`       | Check whether the API is running                    |
| `GET`  | `/health/ready` | Check whether the API and required models are ready |

---

## Detection Response

Detection endpoints return information about detected regions.

An image detection response can look like:

```json
{
  "faces": [
    {
      "x1": 120,
      "y1": 80,
      "x2": 260,
      "y2": 240,
      "confidence": 0.94,
      "id": "face_1"
    }
  ],
  "plates": [
    {
      "x1": 420,
      "y1": 310,
      "x2": 580,
      "y2": 360,
      "confidence": 0.88,
      "id": "plate_1"
    }
  ]
}
```

Video detections additionally include the frame and timestamp where the detection occurred.

Document detections are grouped by page.

---

## Selective Anonymization API

The `anonymize-selected` endpoints accept detection information supplied by the client.

### Image

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize-selected?mode=blur&padding=0.2" \
  -F "file=@image.jpg" \
  -F 'detections=[{"target":"faces","x1":0.25,"y1":0.15,"x2":0.45,"y2":0.50}]' \
  --output anonymized.jpg
```

A detection can contain:

```json
[
  {
    "target": "faces",
    "x1": 0.25,
    "y1": 0.15,
    "x2": 0.45,
    "y2": 0.5,
    "confidence": 0.94,
    "id": "face_1"
  }
]
```

Coordinates used by selective anonymization are normalized between `0` and `1`.

### Documents

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/documents/anonymize-selected?mode=blur" \
  -F "file=@document.pdf" \
  -F 'detections=[{"target":"pii","x1":0.10,"y1":0.30,"x2":0.80,"y2":0.40}]' \
  --output anonymized.pdf
```

### Videos

Video selections additionally identify the frame where a detection was selected.

```json
[
  {
    "target": "faces",
    "x1": 0.25,
    "y1": 0.15,
    "x2": 0.45,
    "y2": 0.5,
    "frame": 0,
    "confidence": 0.94,
    "id": "face_1"
  }
]
```

The selected detection is used as the starting point for tracking through subsequent video frames.

---

## Padding

Padding controls how much additional area around a detection is included in the anonymization.

Default:

```text
0.2
```

Accepted range:

```text
0.0 - 1.0
```

Example:

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize?targets=faces&mode=blur&padding=0.3" \
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

---

# Supported Formats

## Images

Common supported image formats include:

```text
JPG
JPEG
PNG
WEBP
GIF
TIFF
HEIC
HEIF
```

## Videos

Supported video formats include:

```text
MP4
MOV
AVI
MKV
WEBM
```

## Documents

Supported document formats are processed through the document pipeline and converted to PDF when required.

---

# Privacy

Privacy is a core design goal of Blur Stuff.

The application is designed around processing uploaded content for the requested detection and anonymization operation rather than building a permanent collection of user media.

### No account required

The core application does not require users to create an account or provide personal information.

### Minimal data handling

Blur Stuff is designed to process files for the requested operation rather than intentionally maintain a permanent collection of uploaded media.

### Browser-side result handling

The frontend keeps original and processed files available in the browser so they can be previewed and downloaded without requiring the application to permanently store them.

### EXIF removal

Image metadata can contain additional information such as:

- Device information
- Capture dates
- GPS coordinates
- Software information

Processed images have EXIF metadata removed to reduce the risk of unintentionally exposing this information.

> Privacy guarantees can depend on how Blur Stuff is deployed. Review the project's privacy documentation and deployment configuration before using it for highly sensitive workloads.

---

# Architecture

Blur Stuff is structured as a Flask application with a reusable API and a frontend built on top of it.

```text
                         ┌─────────────────────┐
                         │      Frontend       │
                         │ Flask + Jinja       │
                         │ Tailwind + Alpine   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      REST API       │
                         │      /api/v1        │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
              ┌──────────┐   ┌──────────┐   ┌──────────────┐
              │  Images  │   │  Videos  │   │  Documents   │
              └────┬─────┘   └────┬─────┘   └──────┬───────┘
                   │              │                 │
                   └──────────────┼─────────────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │      Detection      │
                       ├─────────────────────┤
                       │ YOLO                │
                       │ PaddleOCR           │
                       │ Presidio             │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │   Anonymization     │
                       ├─────────────────────┤
                       │ Blur                │
                       │ Pixelate            │
                       │ Solid               │
                       │ Noise               │
                       │ Emoji               │
                       │ Inpaint             │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │   Processed Output  │
                       └─────────────────────┘
```

The frontend and API are intentionally separated so that the processing functionality can be consumed independently by other applications.

---

# Technology Stack

### Backend

- **Python**
- **Flask**
- **OpenCV**

### Computer Vision

- **YOLO** — object detection
- **PaddleOCR** — text detection and OCR
- **Microsoft Presidio** — PII recognition

### Frontend

- **Flask / Jinja**
- **Tailwind CSS**
- **Alpine.js**

### API

- REST
- JSON detection responses
- Multipart file uploads
- Versioned API under `/api/v1`

---

# Project Structure

```text
blur-stuff/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── frontend/
│   │   ├── routes/
│   │   ├── static/
│   │   └── templates/
│   ├── media/
│   └── services/
├── models/
├── tests/
├── run.py
├── requirements.txt
├── LICENSE
└── README.md
```

The application is separated into API routes, frontend routes, media processing, detection, anonymization, and supporting services.

---

# Development

Run the application locally:

```bash
python run.py
```

The frontend is served by Flask alongside the API.

The API can also be used independently of the frontend, allowing other applications to integrate Blur Stuff's detection and anonymization functionality.

### Running tests

```bash
pytest
```

---

# Project Status

Blur Stuff is actively under development.

### Implemented

- [x] Face detection
- [x] Face anonymization
- [x] License plate detection
- [x] License plate anonymization
- [x] OCR text detection
- [x] PII detection
- [x] Image anonymization
- [x] Video anonymization
- [x] Audio preservation
- [x] Document processing
- [x] Selective anonymization
- [x] Multiple anonymization modes
- [x] Adjustable padding
- [x] Detection API
- [x] Anonymization API
- [x] Health and readiness endpoints
- [x] EXIF removal

### Future

Planned improvements may include additional detection models, supported formats, anonymization techniques, and processing capabilities.

---

# Documentation

The project includes documentation covering:

- API endpoints
- Detection targets
- Detection responses
- Anonymization modes
- Padding
- Selective anonymization
- Supported formats
- Request and response formats
- Privacy considerations

**Documentation:**

https://blurstuff.com/docs

**API:**

https://blurstuff.com/api

---

# Contributing

Contributions, ideas, bug reports, and improvements are welcome.

If you find a bug or have an idea for improving Blur Stuff:

1. Open an issue
2. Describe the problem or proposed change
3. Include reproduction steps where applicable
4. Submit a pull request for implementation changes

Before contributing, please review the project's existing structure and development conventions.

---

# License

Blur Stuff is open-source software licensed under the **MIT License**.

See [LICENSE](LICENSE) for the full license text.

---

<p align="center">
  Built with Python, Flask, OpenCV, YOLO, PaddleOCR, and ❤️
</p>

<p align="center">
  <a href="https://blurstuff.com">blurstuff.com</a>
</p>
