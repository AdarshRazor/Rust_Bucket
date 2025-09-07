# 🏗️ Agent Mira - AI-Powered Property Recommendation System

A full-stack application that provides intelligent property recommendations using machine learning and multi-factor scoring algorithms.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AgentMira
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment files
   cp backend/env.example backend/.env
   cp client/.env.example client/.env.local
   
   # Edit the environment files with your settings
   ```

3. **Start with Docker Compose (Recommended)**
   ```bash
   # Start all services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend (FastAPI)
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

#### Frontend (Next.js)
```bash
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🏗️ Project Structure

```
AgentMira/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic
│   ├── models/             # ML model files
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI app entry point
├── client/                 # Next.js frontend
│   ├── src/
│   │   └── app/           # Next.js app directory
│   └── package.json       # Node.js dependencies
├── docs/                  # Documentation and case study
├── docker-compose.yml     # Docker services configuration
└── README.md             # This file
```

## 🔧 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Primary database
- **Redis**: Caching layer
- **SQLAlchemy**: ORM for database operations
- **scikit-learn**: Machine learning model serving

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📊 Core Features

### 1. Property Recommendation Engine
- **Multi-factor Scoring**: 6-component weighted algorithm
  - Price Match (30%)
  - Bedrooms (20%)
  - School Rating (15%)
  - Commute Time (15%)
  - Property Age (10%)
  - Amenities (10%)

### 2. ML-Powered Price Prediction
- Integration with provided `complex_price_model_v2.pkl`
- Real-time property price estimation
- Fallback strategies for model failures

### 3. User Experience
- Intuitive preference input form
- Top 3 property recommendations with reasoning
- Responsive design for all devices
- Real-time loading states

## 🚀 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `POST /api/preferences` - Submit user preferences
- `GET /api/recommendations` - Get property recommendations
- `GET /api/properties` - List properties with filtering
- `GET /api/properties/{id}` - Get property details

### ML Endpoints
- `POST /api/ml/predict-price` - Predict property price
- `GET /api/ml/model-info` - Get model information

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd client
npm test
```

### End-to-End Tests
```bash
# Run with Docker Compose
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📈 Monitoring

### Health Checks
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

## 🔧 Development Commands

### Docker Commands
```bash
# Start services
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Database Commands
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d agentmira_dev

# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## 🚦 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/agentmira_dev
REDIS_URL=redis://localhost:6379
ML_MODEL_PATH=./models/complex_price_model_v2.pkl
DEBUG=true
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📋 Development Workflow

1. **Feature Development**
   - Create feature branch from main
   - Implement changes with tests
   - Update documentation
   - Submit pull request

2. **Code Quality**
   - Run linting: `black`, `isort`, `flake8`
   - Run tests: `pytest`
   - Type checking: `mypy`

3. **Database Changes**
   - Create migration: `alembic revision --autogenerate`
   - Apply migration: `alembic upgrade head`
   - Test migration: `alembic downgrade -1`

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**
   - Change ports in docker-compose.yml
   - Kill processes using ports: `lsof -ti:8000 | xargs kill -9`

2. **Database connection issues**
   - Check PostgreSQL is running: `docker-compose ps postgres`
   - Verify connection string in .env

3. **ML model not found**
   - Ensure model file is in `docs/backend/`
   - Check ML_MODEL_PATH in .env

4. **Frontend build issues**
   - Clear node_modules: `rm -rf client/node_modules`
   - Reinstall: `cd client && npm install`

## 📚 Documentation

- [Product Requirements (PRD.md)](./PRD.md)
- [System Architecture (ARCHITECTURE.md)](./ARCHITECTURE.md)
- [Project TODO & Tasks (PROJECT_TODO.md)](./PROJECT_TODO.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the Agent Mira case study.
