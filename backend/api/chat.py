# Copyright (c) 2025 Bhagya Dissanayake
# All rights reserved. This code is proprietary and confidential.
# Unauthorized copying, distribution, or use is strictly prohibited.

from fastapi import APIRouter, HTTPException, Depends
from services.llm_service import llm_service
from models.schemas import ChatRequest, ChatResponse, RecommendationRequest, RecommendationResponse, CompareRequest, CompareResponse
from services.data_service import data_service

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """Handle chat queries about laptops"""
    try:
        response = llm_service.chat_query(request.query, request.context or "")
        
        return ChatResponse(
            data={
                "query": request.query,
                "response": response["response"],
                "context_used": response["context_used"],
                "timestamp": response["timestamp"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get laptop recommendations based on constraints"""
    try:
        response = llm_service.get_recommendations(request.constraints)
        
        return RecommendationResponse(
            data={
                "constraints": request.constraints,
                "recommendations": response["recommendations"],
                "laptops_considered": response["laptops_considered"],
                "timestamp": response["timestamp"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare", response_model=CompareResponse)
async def compare_laptops(request: CompareRequest):
    """Compare multiple laptops"""
    try:
        # Get laptop details
        laptops = []
        for laptop_id in request.laptop_ids:
            laptop = data_service.get_laptop_by_id(laptop_id)
            if laptop:
                # Convert all values to strings to avoid JSON serialization issues
                safe_laptop = {}
                for key, value in laptop.items():
                    if value is not None:
                        if isinstance(value, (int, float)):
                            # Handle special float values that aren't JSON compliant
                            if str(value) in ['inf', '-inf', 'nan']:
                                safe_laptop[key] = str(value)
                            else:
                                safe_laptop[key] = value
                        else:
                            safe_laptop[key] = str(value)
                    else:
                        safe_laptop[key] = None
                laptops.append(safe_laptop)
        
        if len(laptops) < 2:
            raise HTTPException(status_code=404, detail="Could not find enough laptops for comparison")
        
        # Create comparison context
        comparison_context = "Compare these laptops:\n"
        for i, laptop in enumerate(laptops):
            comparison_context += f"Laptop {i+1}: {laptop.get('Brand', '')} {laptop.get('Model', '')}\n"
            comparison_context += f"Processor: {laptop.get('Processor', '')}\n"
            comparison_context += f"Memory: {laptop.get('Memory (RAM)', '')}\n"
            comparison_context += f"Storage: {laptop.get('Storage', '')}\n"
            comparison_context += f"Display: {laptop.get('Display', '')}\n"
            comparison_context += f"Price: {laptop.get('Price Details', '')}\n"
            comparison_context += "---\n"
        
        # Use LLM to generate comparison
        comparison_query = f"Please provide a detailed comparison of these laptops, highlighting key differences, pros and cons, and which would be best for different use cases: {comparison_context}"
        
        response = llm_service.chat_query(comparison_query)
        
        return CompareResponse(
            data={
                "laptops": laptops,
                "comparison": response["response"],
                "laptop_ids": request.laptop_ids
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
