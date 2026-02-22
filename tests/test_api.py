#!/usr/bin/env python3

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "service": "QR Code Generator"
        }


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "QR Code Generator API"
        assert "endpoints" in data


class TestGenerateEndpoint:
    """Test QR code generation endpoint"""
    
    def test_generate_valid_url(self):
        """Test generating QR code with valid URL"""
        response = client.post(
            "/generate",
            json={"url": "https://example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["path"] is not None
        assert data["folder"] is not None
        assert "example.com" in data["message"]
    
    def test_generate_url_without_protocol(self):
        """Test generating QR code with URL without protocol"""
        response = client.post(
            "/generate",
            json={"url": "github.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "https://" in data["message"]
    
    def test_generate_empty_url(self):
        """Test generating QR code with empty URL"""
        response = client.post(
            "/generate",
            json={"url": ""}
        )
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_generate_no_cleanup(self):
        """Test generating QR code without cleanup"""
        response = client.post(
            "/generate",
            json={"url": "https://test.com", "cleanup_on_generate": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_generate_missing_url(self):
        """Test generating QR code without URL parameter"""
        response = client.post(
            "/generate",
            json={}
        )
        assert response.status_code == 422  # Validation error


class TestQRRetrievalEndpoint:
    """Test QR code retrieval endpoint"""
    
    @pytest.fixture
    def qr_folder(self):
        """Generate a QR code for testing"""
        response = client.post(
            "/generate",
            json={"url": "https://example.com"}
        )
        return response.json()["folder"].split("/")[-1]
    
    def test_get_qr_image(self, qr_folder):
        """Test retrieving QR code image"""
        response = client.get(f"/qr/{qr_folder}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    
    def test_get_qr_image_not_found(self):
        """Test retrieving non-existent QR code"""
        response = client.get("/qr/nonexistent_folder")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestMetadataEndpoint:
    """Test metadata retrieval endpoint"""
    
    @pytest.fixture
    def qr_folder(self):
        """Generate a QR code for testing"""
        response = client.post(
            "/generate",
            json={"url": "https://example.com"}
        )
        return response.json()["folder"].split("/")[-1]
    
    def test_get_metadata(self, qr_folder):
        """Test retrieving metadata"""
        response = client.get(f"/metadata/{qr_folder}")
        assert response.status_code == 200
        data = response.json()
        assert "url" in data
        assert "created" in data
        assert "expires" in data
        assert "filename" in data
        assert data["url"] == "https://example.com"
    
    def test_get_metadata_not_found(self):
        """Test retrieving non-existent metadata"""
        response = client.get("/metadata/nonexistent_folder")
        assert response.status_code == 404


class TestCleanupEndpoint:
    """Test cleanup endpoint"""
    
    def test_cleanup_default(self):
        """Test cleanup with default days parameter"""
        response = client.post("/cleanup")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "deleted_count" in data
        assert isinstance(data["deleted_count"], int)
    
    def test_cleanup_custom_days(self):
        """Test cleanup with custom days parameter"""
        response = client.post("/cleanup?days=7")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_cleanup_response_structure(self):
        """Test cleanup response has correct structure"""
        response = client.post("/cleanup")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "deleted_count" in data
        assert "message" in data


class TestEndToEndWorkflow:
    """Test complete workflow"""
    
    def test_complete_workflow(self):
        """Test complete workflow: generate -> retrieve -> cleanup"""
        
        # 1. Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # 2. Generate QR code
        generate_response = client.post(
            "/generate",
            json={"url": "https://workflow-test.com"}
        )
        assert generate_response.status_code == 200
        qr_data = generate_response.json()
        assert qr_data["success"] is True
        folder_name = qr_data["folder"].split("/")[-1]
        
        # 3. Get metadata
        metadata_response = client.get(f"/metadata/{folder_name}")
        assert metadata_response.status_code == 200
        metadata = metadata_response.json()
        assert metadata["url"] == "https://workflow-test.com"
        
        # 4. Get QR image
        image_response = client.get(f"/qr/{folder_name}")
        assert image_response.status_code == 200
        assert image_response.headers["content-type"] == "image/png"
        
        # 5. Cleanup
        cleanup_response = client.post("/cleanup?days=7")
        assert cleanup_response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_method(self):
        """Test invalid HTTP method"""
        response = client.put("/generate")
        assert response.status_code == 405
    
    def test_invalid_json(self):
        """Test invalid JSON request"""
        response = client.post(
            "/generate",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        response = client.post(
            "/generate",
            json={"cleanup_on_generate": True}
        )
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
