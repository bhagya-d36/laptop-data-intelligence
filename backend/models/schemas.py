from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

# Base response model
class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None
    timestamp: Optional[str] = None
    data: Optional[Union[Dict[str, Any], List[Any], Any]] = None

# Health check response
class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: Optional[str] = None
    version: str = "1.0.0"

# API info response
class APIInfoResponse(BaseModel):
    name: str = "Laptop Assistant API"
    version: str = "1.0.0"
    description: str = "AI-powered laptop chat and recommendation API"
    endpoints: Dict[str, str]

# Laptop models
class LaptopResponse(BaseModel):
    laptop_id: int
    brand: str
    model: str
    processor: Optional[str] = None
    memory: Optional[str] = None
    storage: Optional[str] = None
    display: Optional[str] = None
    price_details: Optional[Dict[str, Any]] = None
    review_details: Optional[Dict[str, Any]] = None
    availability: Optional[Dict[str, Any]] = None
    promos: Optional[List[str]] = None

class LaptopListResponse(BaseResponse):
    data: List[LaptopResponse]
    count: int

class LaptopDetailResponse(BaseResponse):
    data: LaptopResponse

# Search models
class SearchRequest(BaseModel):
    query: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None
    processor: Optional[str] = None
    memory: Optional[str] = None
    storage: Optional[str] = None

class AdvancedSearchRequest(BaseModel):
    query: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    sort_by: Optional[str] = "relevance"
    sort_order: Optional[str] = "desc"

class SearchResponse(BaseResponse):
    data: List[LaptopResponse]
    count: int
    query: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

class SearchFiltersResponse(BaseResponse):
    data: Dict[str, List[str]]

class SearchSuggestionsResponse(BaseResponse):
    data: List[str]

# Chat models
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    context: Optional[str] = None

class ChatResponse(BaseResponse):
    data: Dict[str, Any]

class RecommendationRequest(BaseModel):
    constraints: Dict[str, Any] = Field(default_factory=dict)

class RecommendationResponse(BaseResponse):
    data: Dict[str, Any]

class CompareRequest(BaseModel):
    laptop_ids: List[int] = Field(..., min_items=1, max_items=5)

class CompareResponse(BaseResponse):
    data: Dict[str, Any]

# Review models
class ReviewResponse(BaseModel):
    laptop_id: int
    brand: str
    model: str
    overall_rating: Optional[str] = None
    star_breakdown: Optional[str] = None
    ai_summary: Optional[str] = None
    user_feedback: Optional[str] = None
    review_details: Optional[Dict[str, Any]] = None

class ReviewListResponse(BaseResponse):
    data: List[ReviewResponse]
    count: int

class ReviewStatsResponse(BaseResponse):
    data: Dict[str, Any]

class RatingDistributionResponse(BaseResponse):
    data: Dict[str, int]

class ReviewThemesResponse(BaseResponse):
    data: Dict[str, int]

# Offer models
class OfferResponse(BaseModel):
    laptop_id: int
    brand: str
    model: str
    price_details: Optional[Dict[str, Any]] = None
    promos: Optional[List[str]] = None
    availability: Optional[Dict[str, Any]] = None
    current_price: Optional[str] = None
    original_price: Optional[str] = None
    discount: Optional[str] = None

class OfferListResponse(BaseResponse):
    data: List[OfferResponse]
    count: int

class PriceHistoryResponse(BaseResponse):
    data: Dict[str, Any]

# Recommendation models
class RecommendationItem(BaseModel):
    laptop_id: int
    match_score: Optional[float] = None
    similarity_score: Optional[float] = None
    trending_score: Optional[float] = None
    brand: str
    model: str
    processor: Optional[str] = None
    memory: Optional[str] = None
    storage: Optional[str] = None
    display: Optional[str] = None
    price_details: Optional[Dict[str, Any]] = None
    availability: Optional[Dict[str, Any]] = None
    promos: Optional[List[str]] = None
    review_summary: Optional[str] = None
    match_reasons: Optional[List[str]] = None
    value_score: Optional[float] = None

class RecommendationListResponse(BaseResponse):
    data: Dict[str, Any]

class UseCaseRequest(BaseModel):
    use_case: str = Field(..., min_length=1)
    constraints: Optional[Dict[str, Any]] = None

class UseCaseResponse(BaseResponse):
    data: Dict[str, Any]

# Error models
class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: Optional[str] = None
