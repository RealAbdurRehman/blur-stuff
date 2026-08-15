<p align="center">
  <img
    src="https://github.com/RealAbdurRehman/blur-stuff/blob/main/screenshots/logo.svg"
    width="70"
    alt="Blur Stuff"
  />
</p>

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

## Table of Contents

- [What is Blur Stuff?](#what-is-blur-stuff)
- [Why Blur Stuff?](#why-blur-stuff)
- [Features](#features)
- [Demo](#demo)
- [Use Cases](#use-cases)
- [Quick Start](#quick-start)
- [API](#api)
- [API Quick Start](#api-quick-start)
- [API Endpoints](#api-endpoints)
- [Supported Detection Targets](#supported-detection-targets)
- [Anonymization Modes](#anonymization-modes)
- [Detection Response](#detection-response)
- [Selective Anonymization](#selective-anonymization)
- [Padding](#padding)
- [Supported Formats](#supported-formats)
- [Privacy](#privacy)
- [Technology Stack](#technology-stack)
- [Development](#development)
- [Project Status](#project-status)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## What is Blur Stuff?

**Blur Stuff** is an open-source tool for automatically detecting and anonymizing sensitive information in images, videos, and documents.

Instead of manually searching through a file for information that should not be shared, Blur Stuff can automatically detect sensitive regions and apply an anonymization effect to them.

It can detect:

- Faces
- License plates
- Text
- Personally identifiable information (PII)

You can anonymize everything automatically or review detections and choose exactly which regions should be processed.

## Why Blur Stuff?

Sharing media can unintentionally expose information that was never meant to be public. Blur Stuff is designed to make protecting that information simple:

- 🔒 **Privacy-focused** — Minimize unnecessary media handling
- 🎯 **Selective** — Anonymize only what you choose
- ⚡ **Automatic** — Detect sensitive information quickly
- 🔌 **API-first** — Integrate with your own applications
- 🚫 **No account required** — Use the core functionality without registration
- 🧩 **Open source** — Inspect, modify, and self-host

## Features

- **Detection:** Faces, license plates, text, and PII
- **Processing:** Images, videos, and documents
- **Anonymization:** Pixelate, blur, solid, noise, emoji, and inpaint
- **Selective anonymization:** Choose specific detections to process
- **Video:** Detection tracking with audio preservation
- **Privacy:** EXIF removal and no account required
- **API:** Integrate detection and anonymization into your own applications

## Demo

### Image anonymization

<p align="center">
  <img src="https://github.com/RealAbdurRehman/blur-stuff/blob/main/screenshots/anonymize-all.jpg" alt="Blur Stuff image anonymization">
</p>

### Selective anonymization

<p align="center">
  <img src="https://github.com/RealAbdurRehman/blur-stuff/blob/main/screenshots/anonymize-selected.jpg" alt="Blur Stuff selective anonymization">
</p>

### Video anonymization

<p align="center">
  <img src="https://github.com/RealAbdurRehman/blur-stuff/blob/main/screenshots/anonymize-video.gif" alt="Blur Stuff video anonymization">
</p>

## Use Cases

### Content Creation

Hide faces, license plates, and other sensitive information in photos and videos.

### Document Sharing

Anonymize personal and identifying information before sharing documents.

## Quick Start

**Requirements:** Python 3.12, `pip`, and Git.

### Clone

```bash
git clone https://github.com/RealAbdurRehman/blur-stuff.git
cd blur-stuff
```

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> On Windows, use `.venv\Scripts\activate` after creating the virtual environment.

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
python run.py
```

The application will be available locally.

## API

Blur Stuff exposes a reusable REST API for detection and anonymization.

The API is versioned under:

```text
/api/v1/
```

The hosted API base URL is:

```text
https://blurstuff.up.railway.app/api/v1
```

No API key is currently required.

> See the [API documentation](https://blurstuff.up.railway.app/docs) for details.

## API Quick Start

### Image

```bash
curl -X POST \
  "https://blurstuff.up.railway.app/api/v1/images/anonymize?targets=plates" /
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

### Video

```bash
curl -X POST \
  "https://blurstuff.up.railway.app/api/v1/videos/anonymize?targets=faces" /
  -F "file=@video.mp4" \
  --output anonymized.mp4
```

### Document

```bash
curl -X POST \
  "https://blurstuff.up.railway.app/api/v1/documents/anonymize?targets=pii" /
  -F "file=@document.pdf" \
  --output anonymized.pdf
```

See the [API documentation](https://blurstuff.up.railway.app/docs) for details.

## API Endpoints

### Images

| Method | Endpoint                     | Description                      |
| ------ | ---------------------------- | -------------------------------- |
| `POST` | `/images/detect`             | Detect sensitive information     |
| `POST` | `/images/anonymize`          | Detect and anonymize information |
| `POST` | `/images/anonymize-selected` | Anonymize selected detections    |

### Videos

| Method | Endpoint            | Description                      |
| ------ | ------------------- | -------------------------------- |
| `POST` | `/videos/detect`    | Detect sensitive information     |
| `POST` | `/videos/anonymize` | Detect and anonymize information |

> Video processing tracks detections across frames and preserves audio.

### Documents

| Method | Endpoint                        | Description                      |
| ------ | ------------------------------- | -------------------------------- |
| `POST` | `/documents/detect`             | Detect text and PII              |
| `POST` | `/documents/anonymize`          | Detect and anonymize information |
| `POST` | `/documents/anonymize-selected` | Anonymize selected detections    |

### Health

| Method | Endpoint        | Description                   |
| ------ | --------------- | ----------------------------- |
| `GET`  | `/health`       | Check API status              |
| `GET`  | `/health/ready` | Check API and model readiness |

## Supported Detection Targets

Use `targets` to select what Blur Stuff detects.

| Target | Value    | Description                          |
| ------ | -------- | ------------------------------------ |
| Faces  | `faces`  | Human faces                          |
| Plates | `plates` | Vehicle license plates               |
| Text   | `text`   | Text regions                         |
| PII    | `pii`    | Potentially identifiable information |

Multiple targets can be comma-separated, e.g. `?targets=faces,plates`.

> Defaults to `faces`. `text` and `pii` cannot be used together.

## Anonymization Modes

Choose how detected information is anonymized.

| Mode       | Description                        |
| ---------- | ---------------------------------- |
| `pixelate` | Pixelates the region               |
| `blur`     | Blurs the region                   |
| `solid`    | Covers the region                  |
| `noise`    | Adds visual noise                  |
| `emoji`    | Covers the region with an emoji    |
| `inpaint`  | Attempts to reconstruct the region |

> Defaults to `pixelate`.

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

Video detections additionally include the frame and timestamp associated with each detection.

Document detections are grouped by page.

## Selective Anonymization

The `anonymize-selected` endpoints let you anonymize only specific detections instead of processing everything automatically.

Provide the selected detections as normalized bounding boxes (`0`–`1`) through the `detections` field.

```json
[
  {
    "target": "faces",
    "x1": 0.25,
    "y1": 0.15,
    "x2": 0.45,
    "y2": 0.5
  }
]
```

See the [API documentation](https://blurstuff.up.railway.app/docs) for details.

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
  "https://blurstuff.up.railway.app/api/v1/images/anonymize?targets=faces&mode=solid&padding=0.5" \
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

## Supported Formats

**Images:** JPG, JPEG, PNG, WEBP, TIFF, HEIC, HEIF, GIF

**Videos:** MP4, MOV, AVI, MKV, WEBM

**Documents:** PDF, DOCX, PPTX, XLSX

> HEIC/HEIF inputs are returned as PNG. DOCX/PPTX/XLSX inputs are returned as PDF.

## Privacy

Privacy is a core design goal of Blur Stuff.

- **No account required** — No registration or personal information needed.
- **Minimal data handling** — Files are processed and not permanently stored.
- **Browser-side results** — Files can be previewed and downloaded in the browser.
- **EXIF removal** — Image metadata is removed from processed images.

You can check the [Privacy Policy](https://blurstuff.up.railway.app/privacy) for more details.

## Technology Stack

### Backend

- **Python**
- **Flask**
- **OpenCV**

### Computer Vision

- **YOLO**
- **PaddleOCR**
- **Microsoft Presidio**

### Frontend

- **Jinja**
- **Tailwind CSS**
- **Alpine.js**

## Development

Run the application locally:

```bash
python run.py
```

The frontend is served by Flask alongside the API.

The API can also be used independently of the frontend, allowing other applications to integrate Blur Stuff's detection and anonymization functionality.

## Project Status

Blur Stuff is actively under development.

### Implemented

- Face & license plate detection and anonymization
- Text & PII detection and anonymization
- Image, video & document processing
- Selective anonymization
- Multiple anonymization modes
- Adjustable configuration & EXIF removal
- Detection & anonymization API

### In Progress

- **Selective video anonymization** — currently being refined and may contain bugs
- **Selective anonymization** — improving usability and simplifying the required detection format

### Future

- More anonymization modes
- Improved accuracy and reliability
- Improved performance

## Documentation

Explore the API endpoints, detection targets, anonymization modes, supported formats, and more.

**API:** https://blurstuff.up.railway.app/api

**Documentation:** https://blurstuff.up.railway.app/docs

## Contributing

Contributions, ideas, and bug reports are welcome. Open an issue for bugs or feature requests, or submit a pull request for code changes.

## License

Blur Stuff is open-source software licensed under the MIT License.

See [LICENSE](LICENSE) for the full license text.

---

<p align="center">
  <i>Protect what you share.</i>
</p>
