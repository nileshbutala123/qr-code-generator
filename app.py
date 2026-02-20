from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qr_code_generator import QRCodeGenerator

app = FastAPI(title="QR Code Generator API")

generator = QRCodeGenerator()

class QRRequest(BaseModel):
    url: str
    cleanup: bool = True

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate_qr(req: QRRequest):
    result = generator.generate(
        req.url,
        cleanup_on_generate=req.cleanup
    )

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return result