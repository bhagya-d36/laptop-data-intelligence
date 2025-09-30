from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Dict, Any, Optional
from services.data_service import data_service
from models.schemas import BaseResponse

router = APIRouter()

@router.get("/", response_model=BaseResponse)
async def get_all_laptops():
    """Get all laptops for exploration"""
    try:
        laptops = data_service.get_all_laptops()
        
        return BaseResponse(data={
            "laptops": laptops,
            "count": len(laptops)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter-options", response_model=BaseResponse)
async def get_filter_options():
    """Get available filter options"""
    try:
        laptops = data_service.get_all_laptops()
        
        # Extract unique values for each filter
        brands = list(set([laptop.get('Brand', '') for laptop in laptops if laptop.get('Brand')]))
        processors = list(set([laptop.get('Processor', '') for laptop in laptops if laptop.get('Processor')]))
        memory = list(set([laptop.get('Memory (RAM)', '') for laptop in laptops if laptop.get('Memory (RAM)')]))
        storage = list(set([laptop.get('Storage', '') for laptop in laptops if laptop.get('Storage')]))
        displays = list(set([laptop.get('Display', '') for laptop in laptops if laptop.get('Display')]))
        
        return BaseResponse(data={
            "brands": sorted(brands),
            "processors": sorted(processors),
            "memory": sorted(memory),
            "storage": sorted(storage),
            "displays": sorted(displays)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price-trends", response_model=BaseResponse)
async def get_price_trends():
    """Get price trends for laptops"""
    try:
        laptops = data_service.get_all_laptops()
        
        # Generate price trends data
        trends = []
        for i, laptop in enumerate(laptops[:10]):  # Limit to 10 for demo
            import random
            price_change = random.uniform(-15, 15)  # Random price change between -15% and +15%
            
            trends.append({
                "laptop_id": i,
                "brand": laptop.get('brand', laptop.get('Brand', 'Unknown')),
                "model": laptop.get('model', laptop.get('Model', 'Unknown')),
                "price_change": round(price_change, 1),
                "current_price": random.randint(500, 3000)
            })
        
        return BaseResponse(data={"trends": trends})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/availability", response_model=BaseResponse)
async def get_availability():
    """Get availability status for laptops"""
    try:
        laptops = data_service.get_all_laptops()
        
        # Generate availability data
        availability = []
        statuses = ['Available', 'Available Soon']
        
        for i, laptop in enumerate(laptops):
            import random
            status = random.choice(statuses)
            
            availability.append({
                "laptop_id": i,
                "brand": laptop.get('brand', laptop.get('Brand', 'Unknown')),
                "model": laptop.get('model', laptop.get('Model', 'Unknown')),
                "status": status,
                "last_updated": "2024-01-15T10:30:00Z"
            })
        
        return BaseResponse(data={"availability": availability})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=BaseResponse)
async def search_laptops(
    q: Optional[str] = Query(None, description="Search query"),
    brand: Optional[str] = Query(None, description="Brand filter"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    min_rating: Optional[float] = Query(None, description="Minimum rating"),
    processor: Optional[str] = Query(None, description="Processor filter"),
    memory: Optional[str] = Query(None, description="Memory filter"),
    storage: Optional[str] = Query(None, description="Storage filter"),
    display: Optional[str] = Query(None, description="Display filter")
):
    """Search and filter laptops"""
    try:
        filters = {}
        if brand:
            filters['brand'] = brand
        if min_price:
            filters['min_price'] = min_price
        if max_price:
            filters['max_price'] = max_price
        if min_rating:
            filters['min_rating'] = min_rating
        if processor:
            filters['processor'] = processor
        if memory:
            filters['memory'] = memory
        if storage:
            filters['storage'] = storage
        if display:
            filters['display'] = display
        
        results = data_service.search_laptops(q or "", filters)
        
        return BaseResponse(data={
            "laptops": results,
            "count": len(results),
            "filters_applied": filters,
            "query": q
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{laptop_id}", response_model=BaseResponse)
async def get_laptop_details(laptop_id: int = Path(..., description="Laptop ID")):
    """Get detailed information about a specific laptop"""
    try:
        laptop = data_service.get_laptop_by_id(laptop_id)
        
        if not laptop:
            raise HTTPException(status_code=404, detail="Laptop not found")
        
        return BaseResponse(data=laptop)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{laptop_id}/specifications", response_model=BaseResponse)
async def get_laptop_specifications(laptop_id: int = Path(..., description="Laptop ID")):
    """Get detailed specifications for a laptop"""
    try:
        laptop = data_service.get_laptop_by_id(laptop_id)
        
        if not laptop:
            raise HTTPException(status_code=404, detail="Laptop not found")
        
        specifications = {
            "processor": laptop.get('Processor', 'N/A'),
            "memory": laptop.get('Memory (RAM)', 'N/A'),
            "storage": laptop.get('Storage', 'N/A'),
            "display": laptop.get('Display', 'N/A'),
            "graphics": laptop.get('Graphics', 'N/A'),
            "operating_system": laptop.get('Operating System', 'N/A'),
            "battery": laptop.get('Battery', 'N/A'),
            "ports": laptop.get('Ports', 'N/A'),
            "weight": laptop.get('Weight', 'N/A'),
            "dimensions": laptop.get('Dimensions', 'N/A')
        }
        
        return BaseResponse(data=specifications)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
