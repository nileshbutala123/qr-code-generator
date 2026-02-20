# QR Code Generator

A simple Python application to generate QR codes for any URL.  

This project was built by a **non-Python developer** using **GitHub Copilot Agent Mode** (“vibe coding”), deployed on **Render.com**, and is planned for **AWS ECS/EC2 deployment**.  

GitHub repo: [https://github.com/nileshbutala123/qr-code-generator](https://github.com/nileshbutala123/qr-code-generator)

---

## Features

- Generate QR codes for any URL
- Each QR code is stored in a **unique subfolder** with metadata
- Metadata includes: creation timestamp, expiration date, original URL
- Automatic **cleanup of old QR codes**
- Works locally and on cloud deployments
- Simple **FastAPI integration** for web apps
- Built-in **interactive API docs** (Swagger/OpenAPI)
- Designed for **future AI-assisted enhancements** (automated PRs)

---

## Tech Stack

| Layer                | Tools / Frameworks                              |
|----------------------|------------------------------------------------|
| Programming Language  | Python 3.x                                     |
| QR Generation         | `qrcode` Python library                        |
| File Handling         | `pathlib`, `os`, `shutil`                     |
| Web API / Deployment  | FastAPI, Render.com (currently), planned AWS ECS/EC2 |
| API Docs              | Swagger / OpenAPI (built-in)                  |
| AI Assistance         | GitHub Copilot Agent Mode (“vibe coding”)     |
| IDE                   | Visual Studio Code (Python & FastAPI extensions)|

---

## Architecture

```text
+----------------+       +-----------------+
|   User / Web   | <---> | FastAPI Layer   |
+----------------+       +-----------------+
                               |
                               v
                      +-------------------+
                      | QRCodeGenerator   |
                      | (Python Class)    |
                      +-------------------+
                               |
                 +------------------------------+
                 | File Storage / Metadata      |
                 | (Local / Cloud S3 in future)|
                 +------------------------------+




Installation & Local Setup
  1. Clone the repository:
      > git clone https://github.com/nileshbutala123/qr-code-generator.git
      > cd qr-code-generator

2. Install dependencies:
    > pip install -r requirements.txt

3. Open the project in VS Code with recommended Python extensions.

4. Run the FastAPI app locally:
    > uvicorn app:app --reload

5. Access locally via:

    > API: http://127.0.0.1:8000
    > Interactive Swagger UI: http://127.0.0.1:8000/docs

Usage
    Python API from qrcode_generator import QRCodeGenerator
      > generator = QRCodeGenerator()
      > result = generator.generate("https://example.com")
        > print(result['message'])

FastAPI Web API
    > POST /api/generate-qr
      {
        "url": "https://example.com"
      }

    > GET /api/qr-image?path=<qr_image_path> to retrieve the QR code image
    > Swagger UI: Visit http://127.0.0.1:8000/docs for interactive API testing

Deployment
    => Render.com
        Deploy as a Python web service
        Supports automatic rebuilds from GitHub pushes

    => AWS ECS / EC2 (Planned)
        Dockerize the app for ECS Fargate or EC2
        Use S3 for QR code storage and CloudFront for delivery
        Auto-scale API requests with ECS or EC2

AI-Assisted Development Workflow
  Entire app built in <2 days using GitHub Copilot Agent Mode
  “Vibe coding”: AI generates functions, boilerplate, and suggestions while the developer reviews
  Plan: AI agent will automatically propose PRs for feature updates; the developer only reviews and merges

  Benefits:
    Rapid prototype delivery
    Minimal Python knowledge needed
    Easy integration with web and cloud platforms

Future Enhancements
  Add QR code analytics (scan count, location, device)
  Auto-generate QR codes for dynamic URLs
  Provide Base64 output for frontend embedding
  Fully automated AI PR agent for continuous enhancements


Output with screenshots - 
1. Swagger - https://github.com/nileshbutala123/qr-code-generator/blob/main/QR%20Code%20Generator%20API%20-%20Swagger%20UI.pdf
2. Form to enter URL - https://github.com/nileshbutala123/qr-code-generator/blob/main/Output%20with%20Form%20to%20enter%20URL%20-%20Screen%201.pdf
3. https://github.com/nileshbutala123/qr-code-generator/blob/main/Output%20with%20generated%20QR%20Code%20-%20Screen%202.pdf
