# Copyright (c) 2025 Bhagya Dissanayake
# All rights reserved. This code is proprietary and confidential.
# Unauthorized copying, distribution, or use is strictly prohibited.

from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Dict, Any
import json
import math
from services.recommendation_service import recommendation_service
from models.schemas import (
    RecommendationRequest, RecommendationListResponse, UseCaseRequest, UseCaseResponse, BaseResponse
)

class SafeJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return 'null'
        return super().encode(obj)

router = APIRouter()

@router.post("/constraint-based", response_model=RecommendationListResponse)
async def get_constraint_recommendations(request: RecommendationRequest):
    """Get recommendations based on user constraints"""
    try:
        print(f"Received constraints: {request.constraints}")
        recommendations = recommendation_service.get_constraint_based_recommendations(request.constraints)
        print(f"Generated {len(recommendations)} recommendations")
        
        # Clean recommendations for JSON serialization
        def clean_for_json(obj):
            if isinstance(obj, dict):
                return {k: clean_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_for_json(item) for item in obj]
            elif isinstance(obj, float):
                if math.isnan(obj) or math.isinf(obj):
                    return None
            return obj
        
        cleaned_recommendations = clean_for_json(recommendations)
        
        return RecommendationListResponse(data={
            "recommendations": cleaned_recommendations,
            "constraints": request.constraints,
            "count": len(cleaned_recommendations)
        })
    except Exception as e:
        print(f"Error in get_constraint_recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar/{laptop_id}", response_model=BaseResponse)
async def get_similar_laptops(
    laptop_id: int = Path(..., description="Laptop ID"),
    limit: int = Query(5, description="Number of recommendations")
):
    """Get laptops similar to the specified laptop"""
    try:
        recommendations = recommendation_service.get_content_based_recommendations(
            laptop_id, limit
        )
        
        return BaseResponse(data={
            "base_laptop_id": laptop_id,
            "recommendations": recommendations,
            "count": len(recommendations)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending", response_model=BaseResponse)
async def get_trending_laptops(limit: int = Query(5, description="Number of results")):
    """Get trending laptops based on ratings and reviews"""
    try:
        trending = recommendation_service.get_trending_laptops(limit)
        
        return BaseResponse(data={
            "trending_laptops": trending,
            "count": len(trending)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/budget/{max_price}", response_model=BaseResponse)
async def get_budget_recommendations(max_price: float = Path(..., description="Maximum price")):
    """Get recommendations within a specific budget"""
    try:
        constraints = {
            'max_price': max_price
        }
        
        recommendations = recommendation_service.get_constraint_based_recommendations(constraints)
        
        # Sort by value (rating/price ratio)
        for rec in recommendations:
            try:
                price_detail = rec['price_details']
                if isinstance(price_detail, str):
                    import ast
                    price_dict = ast.literal_eval(price_detail)
                    current_price = price_dict.get('Current Price', 'Not Available')
                    if current_price != 'Not Available':
                        price_str = str(current_price).replace('$', '').replace(',', '')
                        if price_str.replace('.', '').isdigit():
                            price = float(price_str)
                            rec['value_score'] = rec['match_score'] / price if price > 0 else 0
            except:
                rec['value_score'] = 0
        
        recommendations.sort(key=lambda x: x.get('value_score', 0), reverse=True)
        
        return BaseResponse(data={
            "max_price": max_price,
            "recommendations": recommendations[:10],  # Top 10 by value
            "count": len(recommendations)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brand/{brand}", response_model=BaseResponse)
async def get_brand_recommendations(brand: str = Path(..., description="Brand name")):
    """Get recommendations for a specific brand"""
    try:
        constraints = {
            'brand': brand
        }
        
        recommendations = recommendation_service.get_constraint_based_recommendations(constraints)
        
        return BaseResponse(data={
            "brand": brand,
            "recommendations": recommendations,
            "count": len(recommendations)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/use-case", response_model=UseCaseResponse)
async def get_use_case_recommendations(request: UseCaseRequest):
    """Get recommendations for specific use cases"""
    try:
        use_case = request.use_case.lower()
        constraints = request.constraints or {}
        
        # Map use cases to constraints
        use_case_mapping = {
            'gaming': {'processor_type': 'intel', 'min_memory': '16gb'},
            'business': {'brand': 'lenovo', 'min_rating': '4.0'},
            'student': {'max_price': '1000', 'min_rating': '3.5'},
            'creative': {'min_memory': '16gb', 'storage_type': 'ssd'},
            'portable': {'brand': 'lenovo'}  # ThinkPads are known for portability
        }
        
        if use_case in use_case_mapping:
            constraints.update(use_case_mapping[use_case])
        
        recommendations = recommendation_service.get_constraint_based_recommendations(constraints)
        
        return UseCaseResponse(data={
            "use_case": use_case,
            "recommendations": recommendations,
            "constraints_applied": constraints,
            "count": len(recommendations)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
