# Agent Mira - System Architecture

## 🏗️ High-Level Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Service    │
│   (React/Next)  │◄──►│   (FastAPI)     │◄──►│   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (PostgreSQL)  │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Cache Layer   │
                       │   (Redis)       │
                       └─────────────────┘
```

### Data Flow

1. **User Input**: User submits preferences through React frontend
2. **API Processing**: FastAPI backend receives and validates preferences
3. **Property Retrieval**: Backend queries PostgreSQL for available properties
4. **ML Prediction**: ML service predicts property prices using provided model
5. **Scoring**: Recommendation engine calculates match scores for each property
6. **Ranking**: Properties are ranked and top 3 are selected
7. **Response**: Results are returned to frontend with reasoning

## 🔧 Technology Stack

### Frontend
- **Framework**: React with Next.js
- **Styling**: Tailwind CSS or Material-UI
- **State Management**: React Context or Redux
- **HTTP Client**: Axios or Fetch API

### Backend
- **Framework**: FastAPI (Python)
- **Database ORM**: SQLAlchemy
- **Authentication**: JWT (if needed)
- **Validation**: Pydantic models
- **Documentation**: OpenAPI/Swagger

### Database
- **Primary**: PostgreSQL
- **Cache**: Redis
- **Migrations**: Alembic

### ML/AI
- **Model**: Provided `complex_price_model_v2.pkl`
- **Framework**: scikit-learn
- **Serving**: FastAPI endpoints

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose (dev), Kubernetes (prod)
- **Cloud**: AWS/GCP/Azure
- **Monitoring**: DataDog/New Relic + Sentry

## 📊 Database Schema

### Properties Table
```sql
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    location VARCHAR(255) NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    size_sqft INTEGER NOT NULL,
    year_built INTEGER,
    amenities TEXT[], -- Array of amenities
    image_urls TEXT[], -- Array of image URLs
    school_rating DECIMAL(3,1),
    commute_time INTEGER, -- Minutes to city center
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### User Preferences Table (Session-based)
```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    budget DECIMAL(12,2) NOT NULL,
    location VARCHAR(255),
    min_bedrooms INTEGER,
    max_commute_time INTEGER,
    min_school_rating DECIMAL(3,1),
    preferred_amenities TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔄 API Endpoints

### Core Endpoints
- `POST /api/preferences` - Submit user preferences
- `GET /api/recommendations` - Get property recommendations
- `GET /api/properties` - List all properties (with filtering)
- `GET /api/properties/{id}` - Get property details
- `GET /api/health` - Health check

### ML Endpoints
- `POST /api/ml/predict-price` - Predict property price
- `GET /api/ml/model-info` - Get model information

## 🚀 Scaling Architecture

### Scenario A: 1,000 users/day
- **Frontend**: Single Next.js instance
- **Backend**: 2-3 FastAPI instances behind load balancer
- **Database**: Single PostgreSQL instance with read replicas
- **Cache**: Single Redis instance
- **ML**: In-process model loading

### Scenario B: 20,000 users/day
- **Frontend**: CDN + multiple Next.js instances
- **Backend**: 10+ FastAPI instances with auto-scaling
- **Database**: PostgreSQL cluster with read replicas
- **Cache**: Redis cluster
- **ML**: Dedicated ML service with model caching
- **Load Balancer**: Application Load Balancer
- **Monitoring**: Comprehensive APM and logging

## 🔒 Security Considerations

### API Security
- Rate limiting per IP/user
- Input validation and sanitization
- CORS configuration
- HTTPS enforcement

### Data Security
- Database encryption at rest
- Secure connection strings
- Environment variable management
- Regular security audits

## 📈 Performance Optimization

### Caching Strategy
- **Redis**: Cache recommendation results
- **CDN**: Static assets and images
- **Database**: Query result caching
- **ML**: Model prediction caching

### Database Optimization
- Proper indexing on search fields
- Query optimization
- Connection pooling
- Read replicas for scaling

## 🔍 Monitoring & Observability

### Application Monitoring
- Response time tracking
- Error rate monitoring
- Throughput metrics
- Resource utilization

### ML Model Monitoring
- Prediction accuracy tracking
- Model performance metrics
- Data drift detection
- A/B testing framework

### Alerting
- Error rate thresholds
- Response time degradation
- Resource utilization alerts
- Model performance alerts

## 🚦 Deployment Strategy

### Development
- Docker Compose for local development
- Hot reloading for frontend and backend
- Local PostgreSQL and Redis instances

### Staging
- Production-like environment
- Automated testing
- Performance testing
- Security scanning

### Production
- Blue-green deployment
- Automated rollback capability
- Database migration strategy
- Zero-downtime deployments

## 📋 Environment Configuration

### Development
```yaml
DATABASE_URL: postgresql://localhost:5432/agentmira_dev
REDIS_URL: redis://localhost:6379
ML_MODEL_PATH: ./models/complex_price_model_v2.pkl
DEBUG: true
```

### Production
```yaml
DATABASE_URL: postgresql://prod-cluster:5432/agentmira
REDIS_URL: redis://prod-cluster:6379
ML_MODEL_PATH: /app/models/complex_price_model_v2.pkl
DEBUG: false
LOG_LEVEL: INFO
```

## 🔄 CI/CD Pipeline

### Build Stage
- Code quality checks (linting, formatting)
- Unit test execution
- Security scanning
- Docker image building

### Test Stage
- Integration tests
- API tests
- End-to-end tests
- Performance tests

### Deploy Stage
- Staging deployment
- Production deployment
- Database migrations
- Health checks
- Rollback capability
