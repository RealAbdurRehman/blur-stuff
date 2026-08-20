<p align="center">
  <img
    src="https://github.com/RealAbdurRehman/blur-stuff/blob/main/screenshots/logo.svg"
    width="300"
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

## What is Blur Stuff?

I made Blur Stuff because when sharing files you might not want others to see some information and hiding it manually might be difficult and time consuming. To make things easier when sharing files, I made this application.

## Features

- You can detect faces, license plates, text and pii
- You can anonymize detected regions using a wide range of anonymization modes
- Blur Stuff supports a wide range of file formats making it easier to use
- It also has an API so you can integrate it in your app if you want

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

## Quick Start

```bash
git clone https://github.com/RealAbdurRehman/blur-stuff.git
cd blur-stuff
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Documentation

You can learn more about the API in the [API documentation](https://blurstuff.up.railway.app/docs).

## Technology Stack

- Python
- Flask
- OpenCV
- YOLO
- PaddleOCR
- Microsoft Presidio
- Jinja
- Tailwind CSS
- Alpine.js

## Current Status

### Working

- Face, license plate, text, and PII detection and anonymization
- Support for images (including GIFs), videos, and documents (PDFs and also Word documents)
- Selective anonymization (to some extent)

### In Progress

- Selective video anonymization currently has bugs but I am working on fixing them
- Selective anonymization in general doesn't have that good of a design and isn't consistent with the rest of the apploication's detection format so I want to improve that

### Planned

- In the future I want to add more anonymization modes and improve some of the current ones like emoji anonymization so the emoji changes based on the person's facial expression
- I also want to improve the accuracy of the entire application
- Performance is currently the weakest part of Blur Stuff so I plan to do a lot of work optimizing it

## License

Blur Stuff is open source software licensed under the MIT License.

See [LICENSE](LICENSE) for the full license text.
