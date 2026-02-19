# FastAPI QR Code Generator - API Documentation

## Base URL
- Local: `http://localhost:8000`
- AWS (example): `http://your-domain.com`

## API Endpoints

### 1. Health Check
**Endpoint:** `GET /health`

**Purpose:** Check if the API is running (useful for AWS load balancer health checks)

**Response:**
```json
{
  "status": "healthy",
  "service": "QR Code Generator"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 2. Root/Welcome
**Endpoint:** `GET /`

**Purpose:** Get API information and available endpoints

**Response:**
```json
{
  "message": "QR Code Generator API",
  "version": "1.0.0",
  "endpoints": {
    "generate": "/generate (POST)",
    "retrieve_qr": "/qr/{folder_name} (GET)",
    "retrieve_metadata": "/metadata/{folder_name} (GET)",
    "cleanup": "/cleanup (POST)",
    "health": "/health (GET)"
  }
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

### 3. Generate QR Code
**Endpoint:** `POST /generate`

**Purpose:** Generate a new QR code for a given URL

**Request Body:**
```json
{
  "url": "https://example.com",
  "cleanup_on_generate": true
}
```

**Parameters:**
- `url` (required, string): The URL to encode in the QR code
  - Automatically adds `https://` if no protocol specified
- `cleanup_on_generate` (optional, boolean): Whether to cleanup QR codes older than 1 day (default: true)

**Response (Success):**
```json
{
  "success": true,
  "path": "/app/QR code/qr_20260219_143522_a1b2c3d4/qrcode.png",
  "folder": "/app/QR code/qr_20260219_143522_a1b2c3d4",
  "message": "QR code generated successfully for URL: https://example.com"
}
```

**Response (Error):**
```json
{
  "detail": "URL cannot be empty"
}
```

**HTTP Status Codes:**
- `200 OK`: QR code successfully generated
- `400 Bad Request`: Invalid URL or other validation error
- `500 Internal Server Error`: Server error during generation

**Examples:**

```bash
# With full URL
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# With domain only (https:// added automatically)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "google.com"}'

# Without cleanup
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com", "cleanup_on_generate": false}'
```

---

### 4. Retrieve QR Code Image
**Endpoint:** `GET /qr/{folder_name}`

**Purpose:** Download the generated QR code as a PNG image

**Parameters:**
- `folder_name` (required, path parameter): The folder name from generation response (e.g., `qr_20260219_143522_a1b2c3d4`)

**Response:**
- PNG image file

**HTTP Status Codes:**
- `200 OK`: Image found and returned
- `404 Not Found`: QR code folder doesn't exist
- `500 Internal Server Error`: Server error

**Examples:**

```bash
# Download QR code image
curl http://localhost:8000/qr/qr_20260219_143522_a1b2c3d4 -o qrcode.png

# View in browser
# http://localhost:8000/qr/qr_20260219_143522_a1b2c3d4
```

---

### 5. Retrieve Metadata
**Endpoint:** `GET /metadata/{folder_name}`

**Purpose:** Get metadata about a generated QR code (URL, creation time, expiration)

**Parameters:**
- `folder_name` (required, path parameter): The folder name from generation response

**Response:**
```json
{
  "url": "https://example.com",
  "created": "2026-02-19T14:35:22.123456",
  "expires": "2026-02-20T14:35:22.123456",
  "filename": "qrcode.png"
}
```

**HTTP Status Codes:**
- `200 OK`: Metadata found
- `404 Not Found`: QR code folder doesn't exist
- `500 Internal Server Error`: Server error

**Examples:**

```bash
curl http://localhost:8000/metadata/qr_20260219_143522_a1b2c3d4

# Pretty print with jq
curl http://localhost:8000/metadata/qr_20260219_143522_a1b2c3d4 | jq .
```

---

### 6. Cleanup Old QR Codes
**Endpoint:** `POST /cleanup`

**Purpose:** Delete QR codes older than specified number of days

**Query Parameters:**
- `days` (optional, integer): Number of days as cutoff (default: 1)

**Response:**
```json
{
  "success": true,
  "deleted_count": 5,
  "message": "Cleanup complete. Deleted 5 old QR code folder(s)."
}
```

**HTTP Status Codes:**
- `200 OK`: Cleanup completed
- `500 Internal Server Error`: Server error

**Examples:**

```bash
# Delete QR codes older than 1 day
curl -X POST http://localhost:8000/cleanup

# Delete QR codes older than 7 days
curl -X POST http://localhost:8000/cleanup?days=7

# Delete QR codes older than 30 days
curl -X POST http://localhost:8000/cleanup?days=30
```

---

## Complete Workflow Example

```bash
#!/bin/bash

# 1. Health check
echo "Checking health..."
curl http://localhost:8000/health

# 2. Generate QR code
echo "Generating QR code..."
response=$(curl -s -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}')

echo "Response: $response"

# Extract folder name from response (requires jq)
folder_name=$(echo $response | jq -r '.folder | split("/") | .[-1]')
echo "Folder: $folder_name"

# 3. Get metadata
echo "Getting metadata..."
curl -s http://localhost:8000/metadata/$folder_name | jq .

# 4. Download QR code
echo "Downloading QR code..."
curl -s http://localhost:8000/qr/$folder_name -o qrcode.png
echo "QR code saved to qrcode.png"

# 5. Cleanup
echo "Cleaning up old QR codes..."
curl -s -X POST http://localhost:8000/cleanup | jq .
```

---

## HTTP Status Codes Reference

| Code | Meaning |
|------|---------|
| 200  | Success |
| 400  | Bad Request (invalid input) |
| 404  | Not Found |
| 500  | Internal Server Error |

---

## Error Handling

### Example Error Responses

**Empty URL:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": ""}'
```
Response: `{"detail": "URL cannot be empty"}`

**QR Code Not Found:**
```bash
curl http://localhost:8000/qr/nonexistent_folder
```
Response: `{"detail": "QR code not found"}`

---

## Rate Limiting (Recommended for Production)

For AWS deployment, consider adding rate limiting:
- Use AWS API Gateway rate limiting
- Or add FastAPI middleware like `slowapi`

---

## Authentication (Optional)

For production, add API key authentication:

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/generate")
async def generate_qr(api_key: str = Security(api_key_header)):
    # Validate API key
    if api_key != valid_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
```

---

## OpenAPI/Swagger UI

Access interactive API documentation (when running locally):
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Performance Tips

1. **Batch requests:** Use task queues (Celery, RQ) for bulk QR code generation
2. **Caching:** Use Redis to cache frequently generated QR codes
3. **CDN:** Serve generated QR codes through CloudFront (AWS)
4. **Database:** Consider storing metadata in DynamoDB instead of files

---

## Client Libraries

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:8000/generate',
    json={'url': 'https://example.com'}
)
data = response.json()
print(f"QR Code Path: {data['path']}")
```

### JavaScript (fetch)
```javascript
const response = await fetch('http://localhost:8000/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url: 'https://example.com'})
});
const data = await response.json();
console.log(data);
```

### cURL (command line)
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## Troubleshooting

### API returns 500 error
- Check server logs: `docker logs qr-code-generator`
- Verify Python dependencies are installed: `pip install -r requirements.txt`

### QR codes not saving
- Check write permissions for QR code directory
- Verify storage is mounted correctly in Docker

### Slow response time
- Consider upgrading container resources
- Enable response caching
- Use task queue for async processing

---

## Support
For issues, check the [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) or the main [README.md](README.md).
