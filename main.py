#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from qr_code_generator import QRCodeGenerator

# Initialize FastAPI app
app = FastAPI(
    title="QR Code Generator API",
    description="Generate QR codes for URLs and manage them with cleanup functionality",
    version="1.0.0"
)

# CORS middleware - adjust origins for your AWS deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins like ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class QRGenerateRequest(BaseModel):
    url: str
    cleanup_on_generate: bool = True

class QRGenerateResponse(BaseModel):
    success: bool
    path: str | None
    folder: str | None
    message: str

class CleanupResponse(BaseModel):
    success: bool
    deleted_count: int
    message: str

# Initialize QR Code Generator
generator = QRCodeGenerator()

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for AWS load balancer"""
    return {"status": "healthy", "service": "QR Code Generator"}

# Generate QR Code endpoint
@app.post("/generate", response_model=QRGenerateResponse)
async def generate_qr(request: QRGenerateRequest):
    """
    Generate a QR code for the provided URL
    
    Args:
        request: Contains URL and optional cleanup_on_generate flag
        
    Returns:
        QRGenerateResponse with success status and path
    """
    try:
        result = generator.generate(
            url=request.url,
            cleanup_on_generate=request.cleanup_on_generate
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['message'])
        
        return QRGenerateResponse(
            success=result['success'],
            path=result['path'],
            folder=result['folder'],
            message=result['message']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Retrieve QR Code Image endpoint
@app.get("/qr/{folder_name}")
async def get_qr_image(folder_name: str):
    """
    Retrieve the QR code image by folder name
    
    Args:
        folder_name: The folder name containing the QR code (e.g., qr_20260212_105235_58e0421c)
        
    Returns:
        The PNG image file
    """
    try:
        qr_path = os.path.join(generator.qr_folder, folder_name, "qrcode.png")
        
        if not os.path.exists(qr_path):
            raise HTTPException(status_code=404, detail="QR code not found")
        
        return FileResponse(qr_path, media_type="image/png")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Retrieve Metadata endpoint
@app.get("/metadata/{folder_name}")
async def get_metadata(folder_name: str):
    """
    Retrieve the metadata for a specific QR code
    
    Args:
        folder_name: The folder name containing the QR code
        
    Returns:
        Metadata as JSON
    """
    try:
        metadata_path = os.path.join(generator.qr_folder, folder_name, "metadata.txt")
        
        if not os.path.exists(metadata_path):
            raise HTTPException(status_code=404, detail="Metadata not found")
        
        metadata = {}
        with open(metadata_path, 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        return metadata
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Cleanup endpoint
@app.post("/cleanup", response_model=CleanupResponse)
async def cleanup_qrcodes(days: int = 1):
    """
    Cleanup old QR code folders
    
    Args:
        days: Number of days after which to delete QR codes (default: 1)
        
    Returns:
        CleanupResponse with statistics
    """
    try:
        result = generator.cleanup_old_qrcodes(days=days)
        
        return CleanupResponse(
            success=result['success'],
            deleted_count=result['deleted_count'],
            message=result['message']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Serve static QR codes if needed (optional - for direct file storage)
# Uncomment and adjust path if you want to serve files directly
# app.mount("/static", StaticFiles(directory="QR code"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
