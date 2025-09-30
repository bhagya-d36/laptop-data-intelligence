# Setup Guide

This guide will walk you through setting up the Laptop Assistant platform from scratch.

## Prerequisites

Before starting, ensure you have the following installed:

### Required Software
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **DeepSeek API Key**: [Get API Key](https://platform.deepseek.com/)

### Optional Software
- **Docker**: [Download Docker](https://www.docker.com/get-started) (for containerized deployment)
- **Postman**: [Download Postman](https://www.postman.com/downloads/) (for API testing)
- **VS Code**: [Download VS Code](https://code.visualstudio.com/) (recommended editor)

## Quick Start (5 minutes)

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repository-url>
cd ai-engineer-assessment

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### 2. Configure Environment
```bash
# Copy environment template
cd ../backend
cp env.example .env

# Edit .env file with your DeepSeek API key
# DEEPSEEK_API_KEY=your_actual_api_key_here
```

### 3. Run the Application
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Start frontend
cd frontend
npm start
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Health: http://localhost:5000/api/v1/health

## Detailed Setup Instructions

### Step 1: Environment Setup

#### Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.8+
```

#### Node.js Environment
```bash
# Verify Node.js installation
node --version  # Should be 16+
npm --version   # Should be 8+
```

### Step 2: Backend Installation

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(FastAPI|pandas|requests)"
```

#### Backend Dependencies
The backend uses the following key packages:
- **FastAPI**: Web framework
- **uvicorn**: ASGI server
- **pandas**: Data manipulation
- **requests**: HTTP client
- **openai**: DeepSeek API client
- **scikit-learn**: Machine learning
- **pydantic**: Data validation

### Step 3: Frontend Installation

```bash
cd frontend

# Install Node.js dependencies
npm install

# Verify installation
npm list --depth=0
```

#### Frontend Dependencies
The frontend uses the following key packages:
- **React**: UI framework
- **Axios**: HTTP client
- **React Scripts**: Build tools

### Step 4: Data Setup

#### Verify Data File
```bash
# Check if data file exists
ls -la data/processed/laptop_info_cleaned.csv

# Verify data structure
head -5 data/processed/laptop_info_cleaned.csv
```

#### Data File Requirements
The `laptop_info_cleaned.csv` file should contain:
- Integrated data from HP and other laptop brands
- Canonical specifications from PDFs
- Scraped marketplace data
- Review and pricing information

### Step 5: API Configuration

#### DeepSeek API Setup
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account or sign in
3. Generate an API key
4. Add the key to your `.env` file:

```bash
# backend/.env
DEEPSEEK_API_KEY=sk-your-actual-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

#### API Testing
```bash
# Test API health
curl http://localhost:5000/api/v1/health

# Test API info
curl http://localhost:5000/api/v1/info
```

### Step 6: Frontend Configuration

#### Environment Variables
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:5000/api/v1
```

#### Proxy Configuration
The frontend is configured to proxy API requests to the backend during development.

### Step 7: Running the Application

#### Development Mode

**Backend Server:**
```bash
cd backend
python app.py
```
- Server runs on http://localhost:5000
- Debug mode enabled
- Auto-reload on code changes

**Frontend Server:**
```bash
cd frontend
npm start
```
- Server runs on http://localhost:3000
- Hot reload enabled
- Proxy to backend configured

#### Production Mode

**Build Frontend:**
```bash
cd frontend
npm run build
```

**Run Backend with Gunicorn:**
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Docker Setup (Alternative)

### Using Docker Compose
```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build
```bash
# Build backend image
cd backend
docker build -t laptop-intelligence-backend .

# Build frontend image
cd ../frontend
docker build -t laptop-intelligence-frontend .

# Run containers
docker run -d -p 5000:5000 laptop-intelligence-backend
docker run -d -p 3000:3000 laptop-intelligence-frontend
```

## Verification Steps

### 1. Backend Verification
```bash
# Check if backend is running
curl http://localhost:5000/api/v1/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### 2. Frontend Verification
- Open http://localhost:3000 in your browser
- You should see the Laptop Intelligence dashboard
- Check browser console for any errors

### 3. API Integration Verification
```bash
# Test catalog endpoint
curl http://localhost:5000/api/v1/catalog/

# Test search endpoint
curl "http://localhost:5000/api/v1/search/?q=thinkpad"

# Test recommendations endpoint
curl -X POST http://localhost:5000/api/v1/recommendations/constraint-based \
  -H "Content-Type: application/json" \
  -d '{"constraints": {"brand": "lenovo"}}'
```

### 4. AI Integration Verification
```bash
# Test chat endpoint
curl -X POST http://localhost:5000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best laptops under $1000?"}'
```

## Troubleshooting

### Common Issues

#### 1. Python Virtual Environment Issues
```bash
# If virtual environment activation fails
python -m venv --clear venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Node.js Dependency Issues
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 3. API Connection Issues
```bash
# Check if backend is running
ps aux | grep python

# Check port availability
netstat -tulpn | grep :5000

# Test API directly
curl -v http://localhost:5000/api/v1/health
```

#### 4. DeepSeek API Issues
```bash
# Verify API key in .env file
cat backend/.env | grep DEEPSEEK_API_KEY

# Test API key validity
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  https://api.deepseek.com/v1/models
```

#### 5. Data File Issues
```bash
# Check data file permissions
ls -la data/processed/laptop_info.csv

# Verify data file content
head -10 data/processed/laptop_info.csv

# Check file encoding
file data/processed/laptop_info.csv
```

### Error Messages and Solutions

#### "ModuleNotFoundError: No module named 'flask'"
```bash
# Solution: Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

#### "Cannot find module 'react'"
```bash
# Solution: Install frontend dependencies
cd frontend
npm install
```

#### "Connection refused" errors
```bash
# Solution: Check if backend is running
cd backend
python app.py
```

#### "API key not configured" warnings
```bash
# Solution: Set DeepSeek API key
echo "DEEPSEEK_API_KEY=your_key_here" >> backend/.env
```

### Performance Optimization

#### Backend Optimization
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Enable caching (optional)
pip install redis
# Configure Redis for caching
```

#### Frontend Optimization
```bash
# Build optimized production bundle
npm run build

# Serve static files with nginx
# Configure nginx to serve build/ directory
```

### Security Considerations

#### Environment Variables
```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use strong API keys
# Rotate API keys regularly
```

#### CORS Configuration
```python
# In backend/app.py, configure CORS for production
CORS(app, origins=["https://yourdomain.com"])
```

## Development Workflow

### 1. Making Changes
```bash
# Backend changes
cd backend
# Edit Python files
# Test with: python app.py

# Frontend changes
cd frontend
# Edit React components
# Test with: npm start
```

### 2. Testing Changes
```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### 3. Deployment
```bash
# Build frontend
cd frontend
npm run build

# Deploy backend
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [DeepSeek API Documentation](https://platform.deepseek.com/api-docs/)

### Support
- Check the main README.md for project overview
- Review API documentation in docs/api.md
- Examine schema documentation in docs/schema.md

### Community
- Create issues for bugs or feature requests
- Submit pull requests for improvements
- Join discussions in project forums

This setup guide should get you up and running with the Laptop Intelligence platform. If you encounter any issues not covered here, please create an issue in the repository.
