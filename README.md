# Cross-Marketplace Laptop & Review Intelligence Platform

An AI-powered laptop chat and recommendation assistant featuring natural language queries, intelligent recommendations, advanced filtering, and comprehensive review analytics. Built with **FastAPI** for high performance and automatic API documentation.

## Features

### Core Functionality
- **Chat Interface**: Natural language queries about laptops and specifications using DeepSeek LLM
- **Smart Recommendations**: Personalized laptop suggestions based on budget, specs, and preferences with detailed rationales
- **Explore & Compare**: Advanced filtering by brand/specs/price/rating with price trends and availability tracking
- **Reviews Intelligence**: Volume and rating trends, top themes, attributes, and brand comparison analytics
- **Real-time Data**: Live laptop information from integrated dataset

### AI-Powered Intelligence
- **LLM Integration**: DeepSeek API for natural language processing and chat responses
- **RAG (Retrieval-Augmented Generation)**: Lightweight RAG system (direct data injection) to enrich LLM prompts with context for accurate, data-driven answers
- **Constraint-based Recommendations**: Filter laptops by budget, brand, rating, and use case
- **Intelligent Matching**: AI-powered matching with detailed rationales and scoring
- **Content-based Recommendations**: Similar laptop suggestions using TF-IDF and cosine similarity

### Advanced Analytics
- **Price Trends**: Price change indicators and market trends
- **Availability Monitoring**: Stock status and availability tracking
- **Review Analytics**: Sentiment analysis, theme extraction, and attribute scoring
- **Brand Comparison**: Side-by-side brand performance metrics and insights

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Data Sources  │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (CSV)         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   DeepSeek LLM  │
                    │   (AI Engine)   │
                    └─────────────────┘
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- DeepSeek API Key
- Git

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-engineer-assessment
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your DeepSeek API key
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
echo "REACT_APP_API_URL=http://localhost:5000/api/v1" > .env
```

### 4. Data Setup
Ensure your `data/processed/laptop_info_cleaned.csv` file is in place.

## Running the Application

### Development Mode

1. **Start Backend Server**
```bash
cd backend
python app.py
# OR
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```
Server will run on http://localhost:5000

2. **Start Frontend Development Server**
```bash
cd frontend
npm start
```
Frontend will run on http://localhost:3000

### Production Mode

1. **Build Frontend**
```bash
cd frontend
npm run build
```

2. **Run Backend with Uvicorn**
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 4
```

## Architecture

Schema diagrams illustrating the project structure can be found in the project’s documentation (doc/schema-diagram.md).

## Data Extraction and Integration Process

#### Technical Specifications

* The **technical specifications** of 4 provided laptops were extracted using a PDF extraction method **Docling - Open Source Document Processing for AI** within a Jupyter Notebook.
* These laptops form the core set for detailed analysis.

#### Store Information

* **Store-level details** including *price, availability, promotions, reviews, and Q&A* for the 4 laptops provided were collected using **AI-powered web scraping** from the official HP and Lenovo online stores.

#### Extended Dataset for Coverage

* To make the platform more **dynamic and functional**, additional **basic information on 63 laptops** was extracted from the HP and Lenovo stores.
* This ensured sufficient data points for a broader and more representative dataset.

#### Final Dataset

* All extracted information was combined into **a single coherent dataset** (`laptop_info_cleaned.csv`) containing **67 laptop entries in total**.
* Of these, the **4 core laptops** include both detailed technical specifications and enriched store data.
* The remaining **63 laptops** provide basic information for improved coverage and usability.

The data preparation and modelling was conducted using Jupyter Notebooks (refer data prep).


The integrated dataset `laptop_info_cleaned.csv` (in data/processed) contains the following key fields:

### Core Information
- `Brand`: Laptop brand (HP, Lenovo, etc.)
- `Model`: Specific model name
- `Price Details`: Current price as string (e.g., "$272.00")
- `Availability`: Availability status (e.g., "Available")
- `Promos / Offers`: Promotional offers (e.g., "3% back in HP Rewards")

### Technical Specifications
- `Processor`: CPU specifications
- `Operating System`: OS information
- `Graphics`: GPU details
- `Memory (RAM)`: RAM specifications
- `Storage`: Storage type and capacity
- `Display`: Screen specifications
- `Battery`: Battery information
- `Ports`: Available ports and connectivity

### Reviews & Feedback
- `Review Details`: Review information (often "-" for missing data)
- `Q&A / FAQ`: Common questions and answers (often "-" for missing data)

## 🔌 API Documentation

### Automatic Documentation
FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

### Base URL
```
http://localhost:5000/api/v1
```

### Key Features
- **Automatic Validation**: Request/response validation with Pydantic models
- **Type Safety**: Full type hints and automatic type checking
- **Interactive Docs**: Try API endpoints directly from the browser
- **OpenAPI Schema**: Standard-compliant API specification

### Endpoints

#### Chat
- `POST /api/v1/chat/query` - Send natural language query about laptops
- `POST /api/v1/chat/recommend` - Get AI-powered recommendations
- `POST /api/v1/chat/compare` - Compare multiple laptops

#### Recommendations
- `POST /api/v1/recommendations/constraint-based` - Get recommendations by constraints
- `GET /api/v1/recommendations/similar/{id}` - Get similar laptops
- `GET /api/v1/recommendations/trending` - Get trending laptops
- `GET /api/v1/recommendations/budget/{price}` - Get budget recommendations
- `GET /api/v1/recommendations/brand/{brand}` - Get brand-specific recommendations
- `POST /api/v1/recommendations/use-case` - Get recommendations for specific use cases

#### Explore & Compare
- `GET /api/v1/explore/` - Get all laptops for exploration
- `GET /api/v1/explore/filter-options` - Get available filter options
- `GET /api/v1/explore/price-trends` - Get price trends data
- `GET /api/v1/explore/availability` - Get availability status
- `GET /api/v1/explore/search` - Search and filter laptops
- `GET /api/v1/explore/{id}` - Get detailed laptop information
- `GET /api/v1/explore/{id}/specifications` - Get laptop specifications

#### Reviews Intelligence
- `GET /api/v1/reviews/` - Get all reviews data
- `GET /api/v1/reviews/volume-trends` - Get review volume trends
- `GET /api/v1/reviews/rating-trends` - Get rating trends over time
- `GET /api/v1/reviews/top-themes` - Get top review themes
- `GET /api/v1/reviews/top-attributes` - Get top product attributes
- `GET /api/v1/reviews/rating-distribution` - Get rating distribution
- `GET /api/v1/reviews/brand-comparison` - Get brand performance comparison
- `GET /api/v1/reviews/stats` - Get overall review statistics

## AI Integration

### DeepSeek API Configuration
The application uses DeepSeek API for:
- Natural language processing of user queries
- Generating personalized recommendations
- Analyzing review sentiment and themes
- Providing contextual responses

### Configuration
```bash
# Set your DeepSeek API key
export DEEPSEEK_API_KEY="your_api_key_here"
```

## Frontend Components

The frontend is a single-page React application with tabbed navigation:

### Chat & Recommend Tab
- **Conversational AI**: Natural language chat interface for laptop queries using DeepSeek LLM
- **Constraint-based Recommendations**: Filter laptops by budget, brand, rating, and use case
- **Interactive Suggestions**: Real-time laptop recommendations with detailed rationales
- **Quick Questions**: Pre-defined common queries for easy access

### Explore & Compare Tab
- **Advanced Filtering**: Filter by brand, price range, rating, processor, memory, storage, and display
- **Price Trends**: Visual price change indicators and market trends
- **Availability Tracking**: Stock status with color-coded indicators
- **Product Comparison**: Select multiple laptops for side-by-side comparison
- **Detailed Views**: Drill into row-level details with specifications

### Reviews Intelligence Tab
- **Volume Trends**: Review volume over time with configurable timeframes
- **Rating Distribution**: Visual breakdown of star ratings
- **Theme Analysis**: Top review themes with sentiment scoring
- **Attribute Insights**: Key product attributes with mention counts and ratings
- **Brand Comparison**: Side-by-side brand performance metrics
- **Sentiment Analysis**: Positive, neutral, and negative sentiment breakdowns

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing
```bash
# Test API health
curl http://localhost:5000/api/v1/health

# Test with automatic docs
open http://localhost:5000/docs
```

## Docker Deployment

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Docker Build
```bash
# Build backend
cd backend
docker build -t laptop-assistant-backend .

# Build frontend
cd frontend
docker build -t laptop-assistant-frontend .
```

## Performance Considerations

- **Async Support**: FastAPI provides native async/await support
- **High Performance**: Built on Starlette and Pydantic for speed
- **Automatic Validation**: Request/response validation without performance overhead
- **Type Safety**: Compile-time type checking reduces runtime errors

## Security

- **API Keys**: Store securely in environment variables
- **CORS**: Configured for development, restrict for production
- **Input Validation**: Automatic validation with Pydantic models
- **Rate Limiting**: Implement rate limiting for API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For support and questions:
- Create an issue in the repository
- Check the automatic API documentation at `/docs`
- Review the setup guide

## Further Scope

- [ ] Real-time price monitoring
- [ ] Advanced ML recommendations
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Integration with more marketplaces
- [ ] Advanced analytics dashboard
- [ ] Automated testing suite
- [ ] Performance monitoring

## License

[No License]

This project is provided for demonstration purposes only. All rights are reserved, and no license is granted for commercial or public use.

**Copyright (c) 2025 Bhagya Dissanayake**  
**All rights reserved. This code is proprietary and confidential.**  
**Unauthorized copying, distribution, or use is strictly prohibited.**

---

## Author 
**Bhagya Dissanayake**

* GitHub: **bhagya-d36**