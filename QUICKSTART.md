# Quick Start Guide - Local Development

## 1. Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerized setup)
- Git

## 2. Local Setup (Without Docker)

### Step 1: Install Dependencies
```bash
cd qr-code-generator
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: Access the API
- **API docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health
- **Generate QR code:**
  ```bash
  curl -X POST http://localhost:8000/generate \
    -H "Content-Type: application/json" \
    -d '{"url": "https://github.com"}'
  ```

---

## 3. Docker Setup (Recommended)

### Step 1: Build Docker Image
```bash
docker build -t qr-code-generator .
```

### Step 2: Run Container
```bash
docker run -p 8000:8000 -v $(pwd)/QR\ code:/app/QR\ code qr-code-generator
```

**Windows PowerShell:**
```powershell
docker run -p 8000:8000 -v "${PWD}/QR code:/app/QR code" qr-code-generator
```

### Step 3: Access API
Same as above (http://localhost:8000/docs)

---

## 4. Docker Compose Setup (Best for Testing)

### Step 1: Start Services
```bash
docker-compose up -d
```

### Step 2: View Logs
```bash
docker-compose logs -f qr-generator
```

### Step 3: Access Services
- **API:** http://localhost:8000
- **Nginx reverse proxy:** http://localhost (optional)
- **API docs:** http://localhost:8000/docs

### Step 4: Stop Services
```bash
docker-compose down
```

---

## 5. Testing the API

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Generate QR Code
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Response:**
```json
{
  "success": true,
  "path": "/app/QR code/qr_20260219_143522_a1b2c3d4/qrcode.png",
  "folder": "/app/QR code/qr_20260219_143522_a1b2c3d4",
  "message": "QR code generated successfully for URL: https://www.google.com"
}
```

### Test 3: Retrieve QR Image
```bash
# Extract folder name from previous response
curl http://localhost:8000/qr/qr_20260219_143522_a1b2c3d4 -o qrcode.png
# Image saved to qrcode.png
```

### Test 4: Get Metadata
```bash
curl http://localhost:8000/metadata/qr_20260219_143522_a1b2c3d4
```

### Test 5: Cleanup Old QR Codes
```bash
curl -X POST http://localhost:8000/cleanup?days=1
```

---

## 6. Interactive API Testing

Open your browser to: **http://localhost:8000/docs**

You'll see Swagger UI where you can:
- Try out endpoints
- See request/response schemas
- Check error examples

---

## 7. Debugging

### View Application Logs
```bash
# Docker container
docker logs qr-code-generator

# Docker compose
docker-compose logs qr-generator -f

# Local run
# Logs appear in terminal
```

### Check Generated QR Codes
```bash
# List all QR code folders
ls -la "QR code/"

# Check metadata
cat "QR code/qr_20260219_143522_a1b2c3d4/metadata.txt"

# View image (on Mac/Linux)
open "QR code/qr_20260219_143522_a1b2c3d4/qrcode.png"
```

### Common Issues

**Issue: Port 8000 already in use**
```bash
# Find process using port 8000
lsof -i :8000

# Use different port
docker run -p 8001:8000 qr-code-generator
```

**Issue: Permission denied for QR code folder**
```bash
# Fix permissions (Linux/Mac)
chmod -R 755 "QR code"
```

**Issue: Module not found errors**
```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt
```

---

## 8. Performance Testing

### Load Test with Apache Bench
```bash
# Generate 100 requests, 10 concurrent
ab -n 100 -c 10 -p test.json -T application/json http://localhost:8000/generate
```

### Load Test with ApacheBench (POST)
```bash
# Create test JSON
echo '{"url": "https://example.com"}' > test.json

# Run test
ab -n 100 -c 10 -p test.json -T application/json http://localhost:8000/generate
```

### Load Test with wrk
```bash
# Install wrk: https://github.com/wg/wrk
wrk -t4 -c100 -d30s http://localhost:8000/health
```

---

## 9. Development Workflow

### 1. Make Changes
Edit `main.py` or `qr_code_generator.py`

### 2. Reload Application
**For Docker:** Restart container
```bash
docker-compose restart qr-generator
```

**For Local:** Stop (Ctrl+C) and restart
```bash
python main.py
```

### 3. Test Changes
```bash
curl http://localhost:8000/docs
```

---

## 10. Next Steps

1. ✅ Test locally
2. 📦 [Build Docker image](AWS_DEPLOYMENT.md#option-2-ecsfargate-deployment-recommended-for-scalability)
3. 🚀 [Deploy to AWS](AWS_DEPLOYMENT.md)
4. 📊 [Monitor with CloudWatch](AWS_DEPLOYMENT.md#monitoring--logging)
5. 🔒 [Secure with HTTPS](AWS_DEPLOYMENT.md#security-best-practices)

---

## 11. Useful Commands

```bash
# View Python version
python --version

# Install packages
pip install -r requirements.txt

# Generate requirements from environment
pip freeze > requirements.txt

# Run with verbose logging
python main.py --log-level debug

# Run on different port
uvicorn main:app --port 8001

# Run with auto-reload (development)
uvicorn main:app --reload

# Format code with black
pip install black
black main.py qr_code_generator.py

# Type checking with mypy
pip install mypy
mypy main.py
```

---

## 12. Documentation Links

- [API Documentation](API_DOCUMENTATION.md) - Detailed API endpoints
- [AWS Deployment](AWS_DEPLOYMENT.md) - Deploy to AWS
- [QR Code Generator](README.md) - Original project README
- [FastAPI Docs](https://fastapi.tiangolo.com/) - FastAPI documentation
- [Uvicorn Docs](https://www.uvicorn.org/) - Uvicorn server documentation

---

## Need Help?

1. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for endpoint details
2. Review [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for deployment issues
3. Check Docker logs: `docker logs qr-code-generator`
4. Access interactive docs: http://localhost:8000/docs
