# Agent Mira - Root Configuration Files

## .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
*.env
.env

# FastAPI
instance/
.webassets-cache

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Next.js
.next/
out/
build/

# Database
*.db
*.sqlite3

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# ML Models (if large)
# *.pkl
# models/

# Environment files
.env
.env.local
.env.production
.env.staging

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml

# Docker
.docker/

# Cache
.cache/
```

## .env.example
```
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/agent_mira_dev
DATABASE_TEST_URL=postgresql://username:password@localhost:5432/agent_mira_test

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_TEST_URL=redis://localhost:6379/1

# Application Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
LOG_LEVEL=INFO
API_VERSION=v1

# ML Model Configuration
ML_MODEL_PATH=./models/complex_price_model_v2.pkl
ML_MODEL_CACHE_TTL=3600

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Agent Mira

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Performance
CACHE_TTL=300
MAX_WORKERS=4
```

## README.md
```markdown
# Agent Mira - AI-Powered Property Recommendation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

## 🏠 Overview

Agent Mira is an intelligent property recommendation system that uses machine learning to match users with their ideal properties based on their preferences and requirements.

## ✨ Features

- **Smart Recommendations**: ML-powered property matching with 6-factor scoring
- **Real-time Price Prediction**: Uses advanced ML model for accurate pricing
- **Intelligent Scoring**: Multi-criteria decision making with weighted algorithms
- **Modern UI**: Clean, responsive React/Next.js interface
- **Fast Performance**: Redis caching and optimized database queries
- **Scalable Architecture**: Designed for high-traffic production use

## 🛠️ Technology Stack

- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL
- **Cache**: Redis
- **ML**: scikit-learn, pandas, numpy
- **DevOps**: Docker, Docker Compose

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- Redis 6+
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/agent-mira.git
cd agent-mira
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database Setup**
```bash
cd backend
alembic upgrade head
python scripts/seed_database.py
```

6. **Start Development Servers**
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000` to access the application.

### Docker Setup (Alternative)

```bash
docker-compose up -d
```

## 📖 Documentation

- [API Documentation](docs/api/endpoints.md)
- [Development Setup](docs/development/setup.md)
- [Architecture Overview](docs/architecture/system-design.md)
- [Deployment Guide](docs/deployment/production.md)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Project Structure

```
agent-mira/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── models/           # ML models
├── data/             # Sample data
├── docs/             # Documentation
├── scripts/          # Utility scripts
└── infrastructure/   # Deployment configs
```

## 🚦 API Endpoints

- `POST /api/preferences` - Submit user preferences
- `GET /api/recommendations` - Get property recommendations
- `GET /api/properties` - List properties with filtering
- `GET /api/health` - Health check

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ML model provided by the development team
- Built with modern web technologies
- Inspired by real estate recommendation systems

## 📞 Support

For support and questions, please contact the development team or create an issue in the repository.
```

## docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/agent_mira
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=True
    volumes:
      - ./backend:/app
      - ./models:/app/models
    depends_on:
      - db
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    command: npm run dev

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: agent_mira
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./data/seed_data.sql:/docker-entrypoint-initdb.d/seed_data.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## package.json (Root)
```json
{
  "name": "agent-mira",
  "version": "1.0.0",
  "description": "AI-Powered Property Recommendation System",
  "main": "index.js",
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd backend && uvicorn main:app --reload --port 8000",
    "dev:frontend": "cd frontend && npm run dev",
    "build": "npm run build:backend && npm run build:frontend",
    "build:backend": "cd backend && python -m build",
    "build:frontend": "cd frontend && npm run build",
    "test": "npm run test:backend && npm run test:frontend",
    "test:backend": "cd backend && pytest",
    "test:frontend": "cd frontend && npm test",
    "setup": "npm run setup:backend && npm run setup:frontend",
    "setup:backend": "cd backend && pip install -r requirements.txt",
    "setup:frontend": "cd frontend && npm install",
    "docker:up": "docker-compose up -d",
    "docker:down": "docker-compose down",
    "docker:logs": "docker-compose logs -f"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/your-username/agent-mira.git"
  },
  "keywords": [
    "real-estate",
    "recommendation-system",
    "machine-learning",
    "fastapi",
    "nextjs",
    "property-search"
  ],
  "author": "Your Name",
  "license": "MIT",
  "devDependencies": {
    "concurrently": "^8.2.0"
  }
}
```