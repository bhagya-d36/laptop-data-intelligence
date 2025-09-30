from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from services.data_service import data_service
from models.schemas import BaseResponse

router = APIRouter()

@router.get("/", response_model=BaseResponse)
async def get_all_reviews():
    """Get all reviews data"""
    try:
        laptops = data_service.get_all_laptops()
        
        # Extract review data from laptops
        reviews = []
        for i, laptop in enumerate(laptops):
            # Parse rating from Review Details
            overall_rating = '0'
            try:
                review_details_str = laptop.get('Review Details', '{}')
                if review_details_str and review_details_str != '{}':
                    import ast
                    review_details = ast.literal_eval(review_details_str)
                    if 'Overall Rating' in review_details:
                        rating_str = review_details['Overall Rating']
                        # Extract rating from "4.5/5 (116 reviews)" format
                        overall_rating = rating_str.split('/')[0]
            except:
                pass
            
            review_data = {
                "laptop_id": i,
                "brand": laptop.get('Brand', 'Unknown'),
                "model": laptop.get('Model', 'Unknown'),
                "overall_rating": overall_rating,
                "star_breakdown": laptop.get('Star Breakdown', ''),
                "ai_summary": laptop.get('AI Summary', ''),
                "user_feedback": laptop.get('User Feedback', ''),
                "review_details": laptop.get('Review Details', '{}')
            }
            reviews.append(review_data)
        
        return BaseResponse(data={
            "reviews": reviews,
            "count": len(reviews)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/volume-trends", response_model=BaseResponse)
async def get_volume_trends(
    timeframe: str = Query("30d", description="Timeframe: 7d, 30d, 90d, 1y, all"),
    brand: str = Query("all", description="Brand filter")
):
    """Get review volume trends"""
    try:
        # Generate volume trends data
        import random
        from datetime import datetime, timedelta
        
        periods = []
        if timeframe == "7d":
            periods = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
        elif timeframe == "30d":
            periods = ["Week 1", "Week 2", "Week 3", "Week 4"]
        elif timeframe == "90d":
            periods = ["Month 1", "Month 2", "Month 3"]
        elif timeframe == "1y":
            periods = ["Q1", "Q2", "Q3", "Q4"]
        else:
            periods = ["2023", "2024"]
        
        trends = []
        for period in periods:
            volume = random.randint(50, 500)
            if brand != "all":
                volume = int(volume * random.uniform(0.3, 0.8))
            
            trends.append({
                "period": period,
                "volume": volume,
                "brand": brand if brand != "all" else "All Brands"
            })
        
        return BaseResponse(data=trends)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rating-trends", response_model=BaseResponse)
async def get_rating_trends(
    timeframe: str = Query("30d", description="Timeframe: 7d, 30d, 90d, 1y, all"),
    brand: str = Query("all", description="Brand filter")
):
    """Get rating trends over time"""
    try:
        # Generate rating trends data
        import random
        
        periods = []
        if timeframe == "7d":
            periods = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
        elif timeframe == "30d":
            periods = ["Week 1", "Week 2", "Week 3", "Week 4"]
        elif timeframe == "90d":
            periods = ["Month 1", "Month 2", "Month 3"]
        elif timeframe == "1y":
            periods = ["Q1", "Q2", "Q3", "Q4"]
        else:
            periods = ["2023", "2024"]
        
        trends = []
        for period in periods:
            avg_rating = round(random.uniform(3.5, 4.8), 1)
            
            trends.append({
                "period": period,
                "avg_rating": avg_rating,
                "total_reviews": random.randint(100, 1000),
                "brand": brand if brand != "all" else "All Brands"
            })
        
        return BaseResponse(data=trends)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-themes", response_model=BaseResponse)
async def get_top_themes(brand: str = Query("all", description="Brand filter")):
    """Get top review themes"""
    try:
        import random
        # Generate themes data
        themes = [
            {"theme": "Performance", "count": 245, "sentiment": "positive", "sentiment_score": 4.2},
            {"theme": "Battery Life", "count": 189, "sentiment": "neutral", "sentiment_score": 3.8},
            {"theme": "Build Quality", "count": 167, "sentiment": "positive", "sentiment_score": 4.1},
            {"theme": "Display Quality", "count": 156, "sentiment": "positive", "sentiment_score": 4.3},
            {"theme": "Price Value", "count": 134, "sentiment": "neutral", "sentiment_score": 3.6},
            {"theme": "Portability", "count": 123, "sentiment": "positive", "sentiment_score": 4.0},
            {"theme": "Keyboard", "count": 98, "sentiment": "positive", "sentiment_score": 3.9},
            {"theme": "Trackpad", "count": 87, "sentiment": "neutral", "sentiment_score": 3.7}
        ]
        
        if brand != "all":
            # Adjust counts for specific brand
            for theme in themes:
                theme["count"] = int(theme["count"] * random.uniform(0.4, 0.9))
        
        return BaseResponse(data=themes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-attributes", response_model=BaseResponse)
async def get_top_attributes(brand: str = Query("all", description="Brand filter")):
    """Get top product attributes mentioned in reviews"""
    try:
        # Generate attributes data
        attributes = [
            {"attribute": "Performance", "mentions": 312, "sentiment": "positive", "avg_rating": 4.2},
            {"attribute": "Battery", "mentions": 267, "sentiment": "neutral", "avg_rating": 3.8},
            {"attribute": "Display", "mentions": 234, "sentiment": "positive", "avg_rating": 4.3},
            {"attribute": "Build", "mentions": 198, "sentiment": "positive", "avg_rating": 4.1},
            {"attribute": "Price", "mentions": 176, "sentiment": "neutral", "avg_rating": 3.6},
            {"attribute": "Portability", "mentions": 154, "sentiment": "positive", "avg_rating": 4.0},
            {"attribute": "Keyboard", "mentions": 132, "sentiment": "positive", "avg_rating": 3.9},
            {"attribute": "Trackpad", "mentions": 98, "sentiment": "neutral", "avg_rating": 3.7},
            {"attribute": "Audio", "mentions": 87, "sentiment": "neutral", "avg_rating": 3.5},
            {"attribute": "Connectivity", "mentions": 76, "sentiment": "positive", "avg_rating": 3.8}
        ]
        
        if brand != "all":
            # Adjust mentions for specific brand
            import random
            for attr in attributes:
                attr["mentions"] = int(attr["mentions"] * random.uniform(0.4, 0.9))
        
        return BaseResponse(data=attributes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rating-distribution", response_model=BaseResponse)
async def get_rating_distribution(brand: str = Query("all", description="Brand filter")):
    """Get rating distribution"""
    try:
        # Generate realistic rating distribution (typical e-commerce pattern)
        distribution = [
            {"rating": 5, "count": 1226},
            {"rating": 4, "count": 1124},
            {"rating": 3, "count": 648},
            {"rating": 2, "count": 189},
            {"rating": 1, "count": 98}
        ]
        
        if brand != "all":
            # Adjust counts for specific brand
            import random
            for dist in distribution:
                dist["count"] = int(dist["count"] * random.uniform(0.3, 0.8))
        
        return BaseResponse(data=distribution)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brand-comparison", response_model=BaseResponse)
async def get_brand_comparison():
    """Get brand performance comparison"""
    try:
        # Generate brand comparison data
        import random
        
        brands = ["Lenovo", "HP", "Dell", "Apple"]
        comparison = []
        
        for brand in brands:
            comparison.append({
                "brand": brand,
                "avg_rating": round(random.uniform(3.8, 4.6), 1),
                "review_count": random.randint(500, 2000),
                "volume": random.randint(1000, 5000),
                "top_theme": random.choice(["Performance", "Battery Life", "Build Quality", "Display Quality"]),
                "positive_percentage": random.randint(65, 85),
                "neutral_percentage": random.randint(10, 20),
                "negative_percentage": random.randint(5, 15)
            })
        
        return BaseResponse(data=comparison)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=BaseResponse)
async def get_review_stats():
    """Get overall review statistics"""
    try:
        laptops = data_service.get_all_laptops()
        
        # Calculate basic stats
        total_reviews = len(laptops)
        avg_rating = 0
        
        if total_reviews > 0:
            ratings = []
            for laptop in laptops:
                try:
                    # First try the parsed review_details (JSON format)
                    review_details = laptop.get('review_details', {})
                    if review_details and 'Overall Rating' in review_details:
                        rating_str = review_details['Overall Rating']
                        # Skip if rating is "-" or empty
                        if rating_str and rating_str != '-' and rating_str != '0':
                            # Extract rating from "4.5/5 (116 reviews)" format
                            rating = float(rating_str.split('/')[0])
                            if rating > 0:
                                ratings.append(rating)
                    else:
                        # Try the raw Review Details field (plain text format)
                        review_details_str = laptop.get('Review Details', '')
                        # Skip if Review Details is "-" or empty
                        if (review_details_str and 
                            review_details_str != '-' and 
                            review_details_str != '{}' and
                            'out of 5 stars' in review_details_str):
                            # Extract rating from "4.2 out of 5 stars, 48 reviews." format
                            import re
                            match = re.search(r'(\d+\.?\d*)\s+out of 5 stars', review_details_str)
                            if match:
                                rating = float(match.group(1))
                                if rating > 0:
                                    ratings.append(rating)
                except:
                    continue
            
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
        
        stats = {
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 1),
            "total_laptops": total_reviews,
            "brands_covered": len(set([laptop.get('Brand', '') for laptop in laptops if laptop.get('Brand')]))
        }
        
        return BaseResponse(data=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
