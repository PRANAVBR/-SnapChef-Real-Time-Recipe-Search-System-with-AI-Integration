# 🍳 SnapChef - Real-Time Recipe Search System

## 🎯 Demo Ready for Judges

**SnapChef** is a fully functional real-time recipe search system built with modern microservices architecture. The system is now running and ready for demonstration!

## 🚀 Quick Start

The entire system is running in Docker containers. All services are healthy and operational.

### Access Points:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **System Statistics**: http://localhost:8000/stats

## 🧪 Demo Instructions

### 1. Frontend Demo
Open http://localhost:3000 in your browser and try these searches:
- **"biryani"** - Shows Chicken Biryani and Vegetable Biryani
- **"paneer"** - Shows Paneer Butter Masala and Paneer Tikka
- **"dal"** - Shows Dal Tadka and Dal Makhani
- **"curry"** - Shows Chicken Curry and Vegetable Curry
- **"rice"** - Shows Jeera Rice

### 2. API Testing
Test the REST API directly:

```bash
# Search for recipes
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"dish_name": "biryani"}'

# Get popular recipes
curl "http://localhost:8000/recipes/popular"

# Check system health
curl "http://localhost:8000/health"

# View system statistics
curl "http://localhost:8000/stats"
```

### 3. API Documentation
Visit http://localhost:8000/docs to explore the interactive API documentation with Swagger UI.

## 🏗️ Architecture Highlights

### Microservices Architecture
- **Backend Service** (FastAPI) - REST API and business logic
- **Frontend Service** (React) - Modern web interface
- **Pathway Pipeline** - Real-time data processing
- **Redis** - Caching and session management
- **Elasticsearch** - Search and indexing engine

### Key Features Demonstrated
✅ **Real-time Recipe Search** - Fast semantic search across multiple sources  
✅ **AI-Powered Matching** - Uses sentence transformers for intelligent matching  
✅ **Docker Containerization** - Complete containerized deployment  
✅ **Microservices Design** - Scalable and maintainable architecture  
✅ **Caching Layer** - Redis for performance optimization  
✅ **Search Engine** - Elasticsearch for fast and accurate search  
✅ **Modern Frontend** - React with responsive design  
✅ **API Documentation** - Interactive Swagger UI  
✅ **Health Monitoring** - System health checks and statistics  

## 🔧 Technical Stack

- **Backend**: FastAPI, Python 3.11
- **Frontend**: React, JavaScript
- **Data Processing**: Pathway
- **Search**: Elasticsearch 8.11.0
- **Caching**: Redis 7
- **AI/ML**: Sentence Transformers, Hugging Face
- **Containerization**: Docker, Docker Compose
- **Web Scraping**: BeautifulSoup, Selenium

## 📊 System Status

All services are running and healthy:
- ✅ Backend API (Port 8000)
- ✅ Frontend (Port 3000)
- ✅ Redis (Port 6379)
- ✅ Elasticsearch (Port 9200)
- ✅ Pathway Pipeline

## 🎉 Demo Results

The system successfully demonstrates:
1. **Fast Search Performance** - Sub-second response times
2. **Accurate Results** - AI-powered semantic matching
3. **Scalable Architecture** - Microservices design
4. **Modern UI/UX** - Responsive React frontend
5. **Complete Integration** - All services working together

## 🚀 Ready for Production

The system is built with production-ready features:
- Health checks and monitoring
- Error handling and logging
- Caching for performance
- Container orchestration
- API documentation
- Scalable architecture

---

**SnapChef is ready for your evaluation!** 🎯
