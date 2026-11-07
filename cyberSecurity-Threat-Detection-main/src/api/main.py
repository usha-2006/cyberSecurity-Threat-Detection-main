"""
Main API for the Cybersecurity Threat Detection System.
Provides REST endpoints for threat detection and system management.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from ..detection.detection_engine import DetectionEngine
from ..alerting.alert_manager import AlertManager
from ..utils.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="Cybersecurity Threat Detection API",
    description="Next-generation threat detection system with AI-powered analysis",
    version="1.0.0"
)

# Add CORS middleware to allow requests from local HTML files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
detection_engine = DetectionEngine()
alert_manager = AlertManager()

class DetectionRequest(BaseModel):
    data: Dict
    request_id: str = None

class ThreatResponse(BaseModel):
    threats: List[Dict]
    request_id: str
    timestamp: str
    total_threats: int = 0

class HealthResponse(BaseModel):
    status: str
    components: Dict

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Cybersecurity Threat Detection System API",
        "version": "1.0.0",
        "endpoints": {
            "/detect": "POST - Detect threats in provided data",
            "/health": "GET - System health check",
            "/docs": "API documentation"
        }
    }

@app.post("/detect", response_model=ThreatResponse)
async def detect_threats(request: DetectionRequest):
    """Detect threats in the provided data."""
    try:
        logger.info(f"Received detection request: {request.request_id}")
        
        # Detect threats
        threats = detection_engine.detect_threats(request.data)
        
        # Send alerts for detected threats
        if threats:
            alert_manager.process_alerts(threats)
        
        response = ThreatResponse(
            threats=threats,
            request_id=request.request_id or "unknown",
            timestamp="2024-01-01T00:00:00Z",  # Would use actual timestamp
            total_threats=len(threats)
        )
        
        logger.info(f"Detection completed: {len(threats)} threats found")
        return response
        
    except Exception as e:
        logger.error(f"Detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check endpoint."""
    try:
        # Check component status (simplified)
        components = {
            "detection_engine": "healthy",
            "alert_manager": "healthy",
            "database": "connected"  # Would check actual DB connection
        }
        
        return HealthResponse(
            status="healthy",
            components=components
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="System unhealthy")

@app.post("/train")
async def train_models(training_data: List[Dict]):
    """Train the machine learning models."""
    try:
        detection_engine.train_models(training_data)
        return {"message": "Models trained successfully"}
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signatures")
async def update_signatures(signatures: List[Dict]):
    """Update threat signatures."""
    try:
        detection_engine.update_signatures(signatures)
        return {"message": "Signatures updated successfully"}
    except Exception as e:
        logger.error(f"Signature update error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# For serverless deployment, do not run uvicorn here
# The app will be imported and wrapped by the serverless handler
