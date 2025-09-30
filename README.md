# SnapChef 🍳

A real-time recipe search and recommendation system that searches across multiple Indian recipe websites using AI-powered semantic search and Pathway for real-time data processing.

## Features

- 🔍 **Real-time Recipe Search**: Search across Hebbar's Kitchen, Archana's Kitchen, and Indian Healthy Recipes
- 🤖 **AI-Powered**: Uses Hugging Face transformers and sentence embeddings for semantic search
- ⚡ **Real-time Processing**: Pathway pipeline for live data processing and indexing
- 🐳 **Dockerized**: Complete containerized setup for easy deployment
- 📊 **Data Indexing**: Elasticsearch for fast search and Redis for caching
- 🎨 **Modern UI**: Beautiful React frontend with responsive design
- 📈 **Analytics**: Popular recipes tracking and search analytics

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │  Pathway Pipeline│
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Real-time)   │
│   Port: 3000    │    │   Port: 8000    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │     Redis       │    │  Elasticsearch  │
                       │   (Caching)     │    │   (Search DB)   │
                       │   Port: 6379    │    │   Port: 9200    │
                       └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd snapchef
   ```

2. **Set up environment**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit .env file and add your Hugging Face API key
   # Get your API key from: https://huggingface.co/settings/tokens
   ```

3. **Start the application**
   
   **On Linux/Mac:**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
   
   **On Windows:**
   ```cmd
   start.bat
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

### Searching for Recipes

1. Open the frontend at http://localhost:3000
2. Enter a dish name in the search box (e.g., "biryani", "dal", "curry")
3. Click "Search Recipes" to find recipes across all sources
4. View the top 2 most accurate results with similarity scores

### API Endpoints

- `POST /search` - Search for recipes
- `GET /recipes/popular` - Get popular recipes
- `POST /recipes/refresh` - Refresh recipe data
- `GET /stats` - Get system statistics
- `GET /health` - Health check

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HUGGINGFACE_API_KEY` | Hugging Face API key for embeddings | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `ELASTICSEARCH_URL` | Elasticsearch connection URL | `http://localhost:9200` |
| `MAX_SEARCH_RESULTS` | Maximum search results | `2` |
| `SIMILARITY_THRESHOLD` | Minimum similarity score | `0.3` |

### Recipe Sources

The system searches across these websites:
- https://hebbarskitchen.com/
- https://www.archanaskitchen.com/
- https://www.indianhealthyrecipes.com/

## Development

### Project Structure

```
snapchef/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main API application
│   ├── models.py           # Pydantic models
│   ├── services.py         # Business logic
│   ├── scrapers/           # Web scrapers
│   └── config.py           # Configuration
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   └── services/       # API services
│   └── public/
├── pathway_pipeline/       # Pathway real-time processing
│   ├── main.py            # Pipeline entry point
│   ├── data_processor.py  # Data processing logic
│   ├── indexer.py         # Elasticsearch indexing
│   └── monitor.py         # Pipeline monitoring
├── docker-compose.yml      # Docker services
├── Dockerfile.*           # Docker configurations
└── requirements.txt       # Python dependencies
```

### Running in Development

1. **Backend only:**
   ```bash
   cd backend
   pip install -r ../requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend only:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Pathway pipeline:**
   ```bash
   cd pathway_pipeline
   python main.py
   ```

## Troubleshooting

### Common Issues

1. **"localhost refused to connect"**
   - Ensure Docker containers are running: `docker-compose ps`
   - Check if ports 3000, 8000, 6379, 9200 are available
   - Wait for services to fully start (may take 2-3 minutes)

2. **Search not working**
   - Check if Elasticsearch is running: `curl http://localhost:9200`
   - Verify Redis is running: `docker-compose exec redis redis-cli ping`
   - Check backend logs: `docker-compose logs snapchef-backend`

3. **No search results**
   - Verify your Hugging Face API key in `.env`
   - Check if recipe websites are accessible
   - Review scraper logs for errors

### Logs

View logs for specific services:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f snapchef-backend
docker-compose logs -f snapchef-frontend
docker-compose logs -f pathway-pipeline
```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down --volumes --remove-orphans

# Remove all images
docker-compose down --rmi all

# Start fresh
./start.sh
```

## Performance

- **Search Speed**: Typically < 2 seconds for cached results
- **Real-time Processing**: Pathway processes data in real-time
- **Caching**: Redis caches search results for 1 hour
- **Indexing**: Elasticsearch provides fast full-text search

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation at http://localhost:8000/docs

---

**SnapChef** - Find your perfect recipe with AI-powered search! 🍳✨
