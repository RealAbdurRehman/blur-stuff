<h1 align="center">Blur Stuff</h1>

<p align="center">
  <i>Privacy-first anonymization for images, videos, and documents</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white" alt="Flask Version">
  <a href="https://github.com/RealAbdurRehman/blur-stuff/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT">
  </a>
</p>

<p align="center">
  <img src="YOUR_SCREENSHOT_URL_HERE" alt="Blur Stuff">
</p>

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Supported Targets](#supported-targets)
- [Anonymization Modes](#anonymization-modes)
- [Quick Start](#quick-start)
- [API](#api)
  - [Health](#health)
  - [Image Anonymization](#image-anonymization)
  - [Video Anonymization](#video-anonymization)
  - [Document Anonymization](#document-anonymization)
  - [Detection](#detection)
  - [Selected Detections](#selected-detections)
- [Privacy](#privacy)
- [Supported Formats](#supported-formats)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- **Face Detection** - Detect and anonymize faces in images and videos
- **License Plate Detection** - Detect and anonymize vehicle license plates
- **Text Detection** - Detect and anonymize visible text using OCR
- **PII Detection** - Identify and anonymize potentially sensitive personal information
- **Video Support** - Anonymize sensitive information across video frames
- **Audio Preservation** - Preserve the original audio when processing videos
- **Document Support** - Process documents and PDFs using OCR and PII detection
- **Selective Anonymization** - Choose individual detections instead of anonymizing everything
- **Multiple Effects** - Pixelate, blur, replace with a solid color, add noise, use emojis, or inpaint
- **Adjustable Padding** - Control how much additional area around a detection is anonymized
- **EXIF Removal** - Remove image metadata that could contain additional information
- **API** - Use Blur Stuff programmatically through HTTP endpoints
- **No Account Required** - The application does not require user accounts for its core functionality

## How It Works

Blur Stuff detects potentially sensitive information and applies an anonymization effect to the detected regions.

```text
Upload
  │
  ▼
Detect sensitive information
  │
  ├── Faces
  ├── License plates
  ├── Text
  └── PII
  │
  ▼
Select detections (optional)
  │
  ▼
Apply anonymization
  │
  ├── Pixelate
  ├── Blur
  ├── Solid
  ├── Noise
  ├── Emoji
  └── Inpaint
  │
  ▼
Download anonymized file
```

## Supported Targets

Blur Stuff currently supports four detection targets:

| Target   | Description                                  |
| -------- | -------------------------------------------- |
| `faces`  | Human faces                                  |
| `plates` | Vehicle license plates                       |
| `text`   | Detected text regions                        |
| `pii`    | Detected personally identifiable information |

`faces` is the default target when no target is specified.

```text
?targets=faces
?targets=faces,plates
?targets=text
?targets=pii
```

`text` and `pii` cannot be used together in the same request.

## Anonymization Modes

The following anonymization modes are available:

| Mode       | Description                           |
| ---------- | ------------------------------------- |
| `pixelate` | Pixelates the detected region         |
| `blur`     | Applies a blur effect                 |
| `solid`    | Covers the region with a solid color  |
| `noise`    | Replaces the region with visual noise |
| `emoji`    | Covers the region with an emoji       |
| `inpaint`  | Attempts to reconstruct the region    |

Pixelation is used by default.

```text
?mode=pixelate
?mode=blur
?mode=solid
?mode=noise
?mode=emoji
?mode=inpaint
```

## Quick Start

### Clone the repository

```bash
git clone https://github.com/RealAbdurRehman/blur-stuff.git
cd blur-stuff
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python run.py
```

The application will then be available locally.

## API

Blur Stuff exposes a reusable HTTP API for detection and anonymization.

The API is versioned under:

```text
/api/v1/
```

### Health

Check whether the API is running:

```bash
curl https://blurstuff.com/api/v1/health
```

### Image Anonymization

Automatically detect and anonymize sensitive information in an image.

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize?targets=faces,plates&mode=blur&padding=0.2" \
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

By default, the API detects faces.

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize" \
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

### Video Anonymization

Anonymize sensitive information in a video:

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/videos/anonymize?targets=faces&mode=blur&padding=0.2" \
  -F "file=@video.mp4" \
  --output anonymized.mp4
```

Video processing tracks detections across frames so that detected objects can continue to be anonymized as they move.

Original audio is preserved during processing.

### Document Anonymization

Documents can be anonymized through the document endpoint:

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/documents/anonymize?targets=pii&mode=blur" \
  -F "file=@document.pdf" \
  --output anonymized.pdf
```

Documents are processed page by page and can use OCR and PII detection to identify sensitive information.

### Detection

Detection endpoints allow applications to inspect what Blur Stuff finds before anonymizing anything.

#### Image Detection

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/detect?targets=faces,plates" \
  -F "file=@image.jpg"
```

Example response:

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

#### Video Detection

Video detections include the frame number and timestamp:

```json
[
  {
    "frame": 0,
    "timestamp": 0.0,
    "detections": {
      "faces": [
        {
          "x1": 120,
          "y1": 80,
          "x2": 260,
          "y2": 240,
          "confidence": 0.94,
          "id": "face_1"
        }
      ]
    }
  }
]
```

#### Document Detection

Document detections are grouped by page:

```json
[
  {
    "text": [
      {
        "x1": 120,
        "y1": 180,
        "x2": 520,
        "y2": 220,
        "confidence": 0.97,
        "id": "token_1"
      }
    ],
    "page": 1
  }
]
```

### Selected Detections

The `anonymize-selected` endpoints allow applications to anonymize only specific detections returned by a detection endpoint.

#### Images

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize-selected?mode=blur&padding=0.2" \
  -F "file=@image.jpg" \
  -F 'detections=[{"target":"faces","x1":0.25,"y1":0.15,"x2":0.45,"y2":0.50}]' \
  --output anonymized.jpg
```

A selected detection contains:

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

Coordinates are normalized between `0` and `1`.

#### Videos

Video selections additionally include the frame where the detection was selected:

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

Blur Stuff uses the selected detection as the starting point and tracks it across subsequent video frames.

#### Documents

Document selections include the page containing the detection:

```json
[
  {
    "target": "pii",
    "x1": 0.1,
    "y1": 0.3,
    "x2": 0.8,
    "y2": 0.4,
    "page": 1,
    "confidence": 0.97,
    "id": "pii_1"
  }
]
```

This allows a specific detection on a specific document page to be anonymized.

## Padding

Padding controls how much additional area around each detected region is included in the anonymization.

The default is:

```text
0.2
```

The accepted range is:

```text
0.0 - 1.0
```

Example:

```bash
curl -X POST \
  "https://blurstuff.com/api/v1/images/anonymize?mode=blur&padding=0.3" \
  -F "file=@image.jpg" \
  --output anonymized.jpg
```

## Supported Formats

Blur Stuff supports a range of image, video, and document formats.

### Images

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

### Videos

Supported video formats include:

```text
MP4
MOV
AVI
MKV
WEBM
```

### Documents

Documents can be processed through the document pipeline and converted to PDF when necessary.

## Privacy

Privacy is a core part of Blur Stuff's design.

The application is designed around processing uploaded content only for the purpose of detection and anonymization.

### No account required

The core application does not require users to create an account or provide personal information.

### No intentional permanent storage

Uploaded files are processed for the requested operation rather than being intended for permanent storage.

### Browser-side result handling

The frontend keeps the original and processed files available in the browser so they can be previewed and downloaded without requiring the application to permanently store them.

### EXIF removal

Image metadata can contain information such as:

- Device information
- Capture dates
- GPS coordinates
- Software information

Blur Stuff removes EXIF metadata from processed images to reduce the risk of unintentionally exposing this information.

For complete details, see the project's privacy documentation.

## Project Structure

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
└── LICENSE
```

The application is separated into API, frontend, media processing, detection, and anonymization services.

## Development

Run the application locally:

```bash
python run.py
```

The frontend is served by Flask alongside the API.

The API can also be used independently of the frontend, allowing other applications to integrate Blur Stuff's detection and anonymization functionality.

## Documentation

Full documentation is available through the project's documentation pages, covering:

- API endpoints
- Detection targets
- Detection responses
- Anonymization modes
- Padding
- Selective anonymization
- Privacy
- Request and response formats

## License

Blur Stuff is open source software licensed under the MIT License.

See [LICENSE](LICENSE) for the full license text.

<p align="center">
  Built with Python, Flask, OpenCV, YOLO, PaddleOCR, and ❤️
</p>
