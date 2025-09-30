# API Documentation

## Overview

The Laptop Assistant API provides comprehensive endpoints for accessing laptop data, reviews, recommendations, and AI-powered chat functionality. Built with **FastAPI**, it offers automatic validation, type safety, and interactive documentation. All endpoints return JSON responses and follow RESTful conventions.

## Interactive Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## Key Features

- **Automatic Validation**: Request/response validation with Pydantic models
- **Type Safety**: Full type hints and automatic type checking
- **Interactive Docs**: Try API endpoints directly from the browser
- **OpenAPI Schema**: Standard-compliant API specification
- **Async Support**: Native async/await support for high performance

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API key authentication.

## Response Format

All API responses follow this format:

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Endpoints

### Health Check

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

#### GET /info
Get API information and available endpoints.

**Response:**
```json
{
  "name": "Laptop Assistant API",
  "version": "1.0.0",
  "description": "AI-powered laptop chat and recommendation API",
  "endpoints": {
    "chat": "/api/v1/chat",
    "recommendations": "/api/v1/recommendations",
    "explore": "/api/v1/explore",
    "reviews": "/api/v1/reviews"
  }
}
```

## Explore API

### GET /explore/
Get all laptops for exploration.

**Response:**
```json
{
  "success": true,
  "data": {
    "laptops": [
      {
        "laptop_id": 0,
        "Brand": "HP",
        "Model": "Chromebook Clamshell",
        "Processor": "Intel Core i5",
        "Memory (RAM)": "8GB DDR4",
        "Storage": "256GB SSD",
        "Price Details": "$272.00",
        "Availability": "Available"
      }
    ],
    "count": 1
  }
}
```

### GET /explore/{id}
Get a specific laptop by ID.

**Parameters:**
- `id` (integer): Laptop ID

**Response:**
```json
{
  "success": true,
  "data": {
    "laptop_id": 0,
    "Brand": "HP",
    "Model": "Chromebook Clamshell",
    "Processor": "Intel Core i5",
    "Memory (RAM)": "8GB DDR4",
    "Storage": "256GB SSD",
    "Price Details": "$272.00",
    "Availability": "Available"
  }
}
```

### GET /explore/filter-options
Get available filter options.

**Response:**
```json
{
  "success": true,
  "data": {
    "brands": ["HP", "Lenovo"],
    "processors": ["Intel Core i5", "AMD Ryzen"],
    "memory": ["8GB DDR4", "16GB DDR4"],
    "storage": ["256GB SSD", "512GB SSD"],
    "displays": ["14\" FHD", "15.6\" FHD"]
  }
}
```

### GET /explore/price-trends
Get price trends data.

**Response:**
```json
{
  "success": true,
  "data": {
    "trends": [
      {
        "laptop_id": 0,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "price_change": 5.2,
        "current_price": 272
      }
    ]
  }
}
```

### GET /explore/availability
Get availability status.

**Response:**
```json
{
  "success": true,
  "data": {
    "availability": [
      {
        "laptop_id": 0,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "status": "Available",
        "last_updated": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

### GET /explore/search
Search and filter laptops.

**Query Parameters:**
- `q` (string): Search query
- `brand` (string): Brand filter
- `min_price` (number): Minimum price
- `max_price` (number): Maximum price
- `min_rating` (number): Minimum rating
- `processor` (string): Processor filter
- `memory` (string): Memory filter
- `storage` (string): Storage filter
- `display` (string): Display filter

**Response:**
```json
{
  "success": true,
  "data": {
    "laptops": [
      {
        "laptop_id": 0,
        "Brand": "HP",
        "Model": "Chromebook Clamshell",
        "Processor": "Intel Core i5"
      }
    ],
    "count": 1,
    "filters_applied": {
      "brand": "hp"
    },
    "query": "chromebook"
  }
}
```

### GET /explore/{id}/specifications
Get detailed specifications for a laptop.

**Parameters:**
- `id` (integer): Laptop ID

**Response:**
```json
{
  "success": true,
  "data": {
    "processor": "Intel Core i5",
    "memory": "8GB DDR4",
    "storage": "256GB SSD",
    "display": "14\" FHD",
    "graphics": "Integrated",
    "operating_system": "Windows 11",
    "battery": "Up to 8 hours",
    "ports": "USB-C, USB-A, HDMI",
    "weight": "1.5 kg",
    "dimensions": "323 x 217 x 19 mm"
  }
}
```

## Chat API

### POST /chat/query
Handle chat queries about laptops.

**Request Body:**
```json
{
  "query": "What are the best laptops under $1000?",
  "context": "Optional context"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "What are the best laptops under $1000?",
    "response": "Based on our analysis, here are the best laptops under $1000...",
    "context_used": "Laptop 1: HP Chromebook Clamshell...",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### POST /chat/recommend
Get laptop recommendations based on constraints.

**Request Body:**
```json
{
  "constraints": {
    "brand": "hp",
    "max_price": 1000,
    "min_rating": 4.0
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "constraints": {
      "brand": "hp",
      "max_price": 1000,
      "min_rating": 4.0
    },
    "recommendations": "Based on your criteria, I recommend the HP Chromebook Clamshell...",
    "laptops_considered": 2,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### POST /chat/compare
Compare multiple laptops.

**Request Body:**
```json
{
  "laptop_ids": [0, 1, 2]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "laptops": [
      {
        "Brand": "HP",
        "Model": "Chromebook Clamshell",
        "Processor": "Intel Core i5"
      }
    ],
    "comparison": "Here's a detailed comparison of the selected laptops...",
    "laptop_ids": [0, 1, 2]
  }
}
```

## Reviews API

### GET /reviews/
Get all reviews and ratings.

**Response:**
```json
{
  "success": true,
  "data": {
    "reviews": [
      {
        "laptop_id": 0,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "overall_rating": "4.2",
        "star_breakdown": "",
        "ai_summary": "User rating: 4.2/5 stars based on 48 reviews. This laptop has received positive feedback from users.",
        "user_feedback": "Based on user reviews and ratings."
      }
    ],
    "count": 1
  }
}
```

### GET /reviews/volume-trends
Get review volume trends.

**Query Parameters:**
- `timeframe` (string): Timeframe (7d, 30d, 90d, 1y, all) - default: 30d
- `brand` (string): Brand filter - default: all

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "period": "Week 1",
      "volume": 245,
      "brand": "All Brands"
    },
    {
      "period": "Week 2", 
      "volume": 312,
      "brand": "All Brands"
    }
  ]
}
```

### GET /reviews/stats
Get overall review statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_reviews": 476,
    "average_rating": 4.1,
    "total_laptops": 476,
    "brands_covered": 2
  }
}
```

### GET /reviews/rating-distribution
Get rating distribution.

**Query Parameters:**
- `brand` (string): Brand filter - default: all

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "rating": 5,
      "count": 1226
    },
    {
      "rating": 4,
      "count": 1124
    },
    {
      "rating": 3,
      "count": 648
    }
  ]
}
```

### GET /reviews/top-themes
Get top review themes.

**Query Parameters:**
- `brand` (string): Brand filter - default: all

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "theme": "Performance",
      "count": 245,
      "sentiment": "positive",
      "sentiment_score": 4.2
    },
    {
      "theme": "Battery Life",
      "count": 189,
      "sentiment": "neutral",
      "sentiment_score": 3.8
    }
  ]
}
```

### GET /reviews/top-attributes
Get top product attributes.

**Query Parameters:**
- `brand` (string): Brand filter - default: all

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "attribute": "Performance",
      "mentions": 312,
      "sentiment": "positive",
      "avg_rating": 4.2
    },
    {
      "attribute": "Battery",
      "mentions": 267,
      "sentiment": "neutral",
      "avg_rating": 3.8
    }
  ]
}
```

### GET /reviews/brand-comparison
Get brand performance comparison.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "brand": "HP",
      "avg_rating": 4.2,
      "review_count": 1250,
      "volume": 2500,
      "top_theme": "Performance",
      "positive_percentage": 75,
      "neutral_percentage": 15,
      "negative_percentage": 10
    },
    {
      "brand": "Lenovo",
      "avg_rating": 4.4,
      "review_count": 980,
      "volume": 1950,
      "top_theme": "Build Quality",
      "positive_percentage": 80,
      "neutral_percentage": 12,
      "negative_percentage": 8
    }
  ]
}
```

## Recommendations API

### POST /recommendations/constraint-based
Get recommendations based on user constraints.

**Request Body:**
```json
{
  "constraints": {
    "brand": "hp",
    "max_price": 1000,
    "min_rating": 4.0,
    "processor_type": "intel",
    "min_memory": "8gb",
    "storage_type": "ssd"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "laptop_id": 0,
        "match_score": 8.5,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "processor": "Intel Core i5",
        "memory": "8GB DDR4",
        "storage": "256GB SSD",
        "display": "14\" FHD",
        "price_details": {
          "Current Price": "$272.00"
        },
        "availability": {
          "Status": "Available"
        },
        "match_reasons": [
          "Matches preferred brand: HP",
          "Within budget: $272.00",
          "High rating: 4.2/5"
        ],
        "review_summary": "User rating: 4.2/5 stars based on 48 reviews. This laptop has received positive feedback from users."
      }
    ],
    "constraints": {
      "brand": "hp",
      "max_price": 1000,
      "min_rating": 4.0
    },
    "count": 1
  }
}
```

### GET /recommendations/similar/{id}
Get laptops similar to the specified laptop.

**Parameters:**
- `id` (integer): Laptop ID
- `limit` (integer): Number of recommendations (default: 5)

**Response:**
```json
{
  "success": true,
  "data": {
    "base_laptop_id": 0,
    "recommendations": [
      {
        "laptop_id": 1,
        "similarity_score": 0.85,
        "brand": "HP",
        "model": "Chromebook x360",
        "processor": "Intel Core i5",
        "memory": "8GB DDR4",
        "storage": "256GB SSD",
        "display": "14\" FHD",
        "price_details": "$791.00",
        "review_summary": "User rating: 4.1/5 stars based on 32 reviews. This laptop has received positive feedback from users."
      }
    ],
    "count": 1
  }
}
```

### GET /recommendations/trending
Get trending laptops based on ratings and reviews.

**Query Parameters:**
- `limit` (integer): Number of results (default: 5)

**Response:**
```json
{
  "success": true,
  "data": {
    "trending_laptops": [
      {
        "laptop_id": 0,
        "trending_score": 12.5,
        "rating": 4.2,
        "review_count": 48,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "processor": "Intel Core i5",
        "price_details": "$272.00",
        "review_summary": "User rating: 4.2/5 stars based on 48 reviews. This laptop has received positive feedback from users."
      }
    ],
    "count": 1
  }
}
```

### GET /recommendations/budget/{max_price}
Get recommendations within a specific budget.

**Parameters:**
- `max_price` (float): Maximum price

**Response:**
```json
{
  "success": true,
  "data": {
    "max_price": 1000.0,
    "recommendations": [
      {
        "laptop_id": 0,
        "match_score": 7.5,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "processor": "Intel Core i5",
        "value_score": 0.0154,
        "price_details": {
          "Current Price": "$272.00"
        },
        "review_summary": "User rating: 4.2/5 stars based on 48 reviews. This laptop has received positive feedback from users."
      }
    ],
    "count": 1
  }
}
```

### GET /recommendations/brand/{brand}
Get recommendations for a specific brand.

**Parameters:**
- `brand` (string): Brand name

**Response:**
```json
{
  "success": true,
  "data": {
    "brand": "hp",
    "recommendations": [
      {
        "laptop_id": 0,
        "match_score": 10.0,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "processor": "Intel Core i5",
        "match_reasons": ["Matches preferred brand: HP"]
      }
    ],
    "count": 1
  }
}
```

### POST /recommendations/use-case
Get recommendations for specific use cases.

**Request Body:**
```json
{
  "use_case": "business",
  "constraints": {
    "max_price": 1500
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "use_case": "business",
    "recommendations": [
      {
        "laptop_id": 0,
        "match_score": 8.0,
        "brand": "HP",
        "model": "Chromebook Clamshell",
        "processor": "Intel Core i5",
        "match_reasons": [
          "Matches preferred brand: HP",
          "High rating: 4.2/5"
        ]
      }
    ],
    "constraints_applied": {
      "brand": "hp",
      "min_rating": "4.0",
      "max_price": 1500
    },
    "count": 1
  }
}
```

## Chat API

### POST /chat/query
Handle chat queries about laptops.

**Request Body:**
```json
{
  "query": "What are the best laptops under $1000?",
  "context": "Optional context"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "What are the best laptops under $1000?",
    "response": "Based on our analysis, here are the best laptops under $1000...",
    "context_used": "Laptop 1: HP Chromebook Clamshell...",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### POST /chat/recommend
Get laptop recommendations based on constraints.

**Request Body:**
```json
{
  "constraints": {
    "brand": "hp",
    "max_price": 1000,
    "min_rating": 4.0
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "constraints": {
      "brand": "hp",
      "max_price": 1000,
      "min_rating": 4.0
    },
    "recommendations": "Based on your criteria, I recommend the HP Chromebook Clamshell...",
    "laptops_considered": 2,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### POST /chat/compare
Compare multiple laptops.

**Request Body:**
```json
{
  "laptop_ids": [0, 1, 2]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "laptops": [
      {
        "Brand": "HP",
        "Model": "Chromebook Clamshell",
        "Processor": "Intel Core i5"
      }
    ],
    "comparison": "Here's a detailed comparison of the selected laptops...",
    "laptop_ids": [0, 1, 2]
  }
}
```

## Rate Limiting

Currently, there are no rate limits implemented. In production, consider implementing rate limiting to prevent abuse.

## CORS

The API supports CORS for cross-origin requests from the frontend application.

## Data Formats

### Date Format
All timestamps are in ISO 8601 format: `YYYY-MM-DDTHH:mm:ssZ`

### Price Format
Prices are stored as strings in the format: `"$272.00"` or `"Not Available"`

### Rating Format
Ratings are stored as strings in the format: `"4.2"` or `"N/A"`

### JSON Fields
Some fields contain JSON strings that need to be parsed:
- `Price Details`: Contains price information
- `Review Details`: Contains review and rating information
- `Availability`: Contains availability status
- `Promos / Offers`: Contains promotional offers

## Testing

### Using curl
```bash
# Get all laptops
curl http://localhost:5000/api/v1/explore/

# Search laptops
curl "http://localhost:5000/api/v1/explore/search?q=chromebook&brand=hp"

# Get recommendations
curl -X POST http://localhost:5000/api/v1/recommendations/constraint-based \
  -H "Content-Type: application/json" \
  -d '{"constraints": {"brand": "hp", "max_price": 1000}}'
```

### Using Postman
Import the API collection or manually test endpoints using the examples above.

## Support

For API support and questions:
- Check the error messages in responses
- Verify request format matches examples
- Ensure all required parameters are provided
- Check server logs for detailed error information
