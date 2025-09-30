# Copyright (c) 2025 Bhagya Dissanayake
# All rights reserved. This code is proprietary and confidential.
# Unauthorized copying, distribution, or use is strictly prohibited.

import os
from fastapi import FastAPI, HTTPException, Depends, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import pandas as pd
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

# Load environment variables
load_dotenv()

# Import API modules
from api.chat import router as chat_router
from api.recommendations import router as recommendations_router
from api.explore import router as explore_router
from api.reviews import router as reviews_router

# Import models
from models.schemas import HealthResponse, APIInfoResponse, ErrorResponse

# Create FastAPI app
app = FastAPI(
    title="Laptop Assistant API",
    description="AI-powered laptop chat and recommendation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(recommendations_router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(explore_router, prefix="/api/v1/explore", tags=["explore"])
app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["reviews"])

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(timestamp=datetime.now().isoformat())

@app.get("/api/v1/info", response_model=APIInfoResponse)
async def api_info():
    """API information endpoint"""
    return APIInfoResponse(
        endpoints={
            "chat": "/api/v1/chat",
            "recommendations": "/api/v1/recommendations",
            "explore": "/api/v1/explore",
            "reviews": "/api/v1/reviews"
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=f"HTTP {exc.status_code} error",
            timestamp=datetime.now().isoformat()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )