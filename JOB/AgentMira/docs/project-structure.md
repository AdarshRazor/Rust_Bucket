# Agent Mira - Project Repository Structure

## 📁 Root Directory Structure

```
agent-mira/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
├── package.json
│
├── backend/                          # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                       # FastAPI application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile
│   ├── alembic.ini                   # Database migration config
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── core/                     # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # Application settings
│   │   │   ├── database.py           # Database connection
│   │   │   ├── redis.py              # Redis connection
│   │   │   └── security.py           # Security utilities
│   │   │
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── property.py           # Property data model
│   │   │   └── preferences.py        # User preferences model
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── property.py           # Property schemas
│   │   │   ├── preferences.py        # Preferences schemas
│   │   │   └── recommendations.py    # Recommendation schemas
│   │   │
│   │   ├── api/                      # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # Dependencies
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── properties.py     # Property endpoints
│   │   │   │   ├── preferences.py    # Preference endpoints
│   │   │   │   ├── recommendations.py # Recommendation endpoints
│   │   │   │   └── health.py         # Health check endpoints
│   │   │   └── api.py                # API router
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── property_service.py   # Property management
│   │   │   ├── ml_service.py         # ML model service
│   │   │   ├── recommendation_engine.py # Recommendation logic
│   │   │   └── scoring_service.py    # Scoring algorithms
│   │   │
│   │   ├── ml/                       # ML related code
│   │   │   ├── __init__.py
│   │   │   ├── model_wrapper.py      # ML model wrapper
│   │   │   ├── price_predictor.py    # Price prediction logic
│   │   │   └── model_monitor.py      # Model performance monitoring
│   │   │
│   │   └── utils/                    # Utility functions
│   │       ├── __init__.py
│   │       ├── logging.py            # Logging configuration
│   │       ├── validators.py         # Input validation
│   │       └── exceptions.py         # Custom exceptions
│   │
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── README
│   │
│   └── tests/                        # Backend tests
│       ├── __init__.py
│       ├── conftest.py               # Test configuration
│       ├── test_api/
│       │   ├── __init__.py
│       │   ├── test_properties.py
│       │   ├── test_preferences.py
│       │   └── test_recommendations.py
│       ├── test_services/
│       │   ├── __init__.py
│       │   ├── test_ml_service.py
│       │   ├── test_recommendation_engine.py
│       │   └── test_scoring_service.py
│       └── test_utils/
│           ├── __init__.py
│           └── test_validators.py
│
├── frontend/                         # React/Next.js Frontend
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── .env.local.example
│   │
│   ├── public/                       # Static assets
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   └── images/
│   │       └── properties/           # Property images
│   │
│   ├── src/
│   │   ├── app/                      # Next.js 13+ app directory
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── globals.css           # Global styles
│   │   │   └── recommendations/
│   │   │       └── page.tsx          # Recommendations page
│   │   │
│   │   ├── components/               # Reusable components
│   │   │   ├── ui/                   # UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   │
│   │   │   ├── forms/                # Form components
│   │   │   │   ├── PreferenceForm.tsx
│   │   │   │   ├── PropertyFilters.tsx
│   │   │   │   └── FormValidation.tsx
│   │   │   │
│   │   │   ├── property/             # Property components
│   │   │   │   ├── PropertyCard.tsx
│   │   │   │   ├── PropertyList.tsx
│   │   │   │   ├── PropertyDetails.tsx
│   │   │   │   └── PropertyGallery.tsx
│   │   │   │
│   │   │   └── layout/               # Layout components
│   │   │       ├── Header.tsx
│   │   │       ├── Footer.tsx
│   │   │       └── Navigation.tsx
│   │   │
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useApi.ts
│   │   │   ├── useProperties.ts
│   │   │   ├── useRecommendations.ts
│   │   │   └── useLocalStorage.ts
│   │   │
│   │   ├── services/                 # API services
│   │   │   ├── api.ts                # API client configuration
│   │   │   ├── propertyService.ts    # Property API calls
│   │   │   ├── preferenceService.ts  # Preference API calls
│   │   │   └── recommendationService.ts # Recommendation API calls
│   │   │
│   │   ├── types/                    # TypeScript types
│   │   │   ├── property.ts
│   │   │   ├── preferences.ts
│   │   │   ├── recommendations.ts
│   │   │   └── api.ts
│   │   │
│   │   ├── utils/                    # Utility functions
│   │   │   ├── formatting.ts
│   │   │   ├── validation.ts
│   │   │   └── constants.ts
│   │   │
│   │   └── styles/                   # Additional styles
│   │       ├── components.css
│   │       └── utilities.css
│   │
│   └── __tests__/                    # Frontend tests
│       ├── components/
│       │   ├── PropertyCard.test.tsx
│       │   ├── PreferenceForm.test.tsx
│       │   └── PropertyList.test.tsx
│       ├── services/
│       │   ├── api.test.ts
│       │   └── propertyService.test.ts
│       └── utils/
│           ├── formatting.test.ts
│           └── validation.test.ts
│
├── models/                           # ML Models
│   ├── complex_price_model_v2.pkl    # Provided ML model
│   ├── model_metadata.json           # Model information
│   └── model_validation.py           # Model validation script
│
├── data/                            # Data files
│   ├── mock_properties.json         # Mock property data
│   ├── seed_data.sql                # Database seed script
│   └── sample_preferences.json      # Sample user preferences
│
├── scripts/                         # Utility scripts
│   ├── setup.sh                     # Project setup script
│   ├── seed_database.py             # Database seeding
│   ├── test_ml_model.py             # ML model testing
│   └── deploy.sh                    # Deployment script
│
├── docs/                            # Documentation
│   ├── api/                         # API documentation
│   │   ├── openapi.json
│   │   └── endpoints.md
│   ├── deployment/                  # Deployment guides
│   │   ├── local.md
│   │   ├── staging.md
│   │   └── production.md
│   ├── development/                 # Development guides
│   │   ├── setup.md
│   │   ├── contributing.md
│   │   └── testing.md
│   └── architecture/                # Architecture documentation
│       ├── system-design.md
│       ├── database-schema.md
│       └── ml-pipeline.md
│
├── infrastructure/                  # Infrastructure as Code
│   ├── docker/                      # Docker configurations
│   │   ├── backend.Dockerfile
│   │   ├── frontend.Dockerfile
│   │   └── nginx.conf
│   ├── k8s/                         # Kubernetes manifests
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── database-deployment.yaml
│   │   └── redis-deployment.yaml
│   └── terraform/                   # Terraform configurations
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
└── monitoring/                      # Monitoring and logging
    ├── prometheus/
    │   └── prometheus.yml
    ├── grafana/
    │   └── dashboards/
    └── logs/
        └── .gitkeep
```

## 📋 Key Features of This Structure

### Backend Organization
- **Modular Design**: Clear separation of concerns with dedicated directories for models, schemas, API endpoints, and services
- **FastAPI Best Practices**: Following FastAPI recommended project structure
- **ML Integration**: Dedicated ML module for model serving and monitoring
- **Testing**: Comprehensive test structure matching the application structure

### Frontend Organization
- **Next.js 13+ App Directory**: Using the latest Next.js app directory structure
- **Component Organization**: Logical grouping of UI components, forms, and property-specific components
- **TypeScript Support**: Strong typing with dedicated types directory
- **Service Layer**: Clean API integration with dedicated service files

### Development Support
- **Docker Support**: Multi-stage Dockerfiles for both development and production
- **Database Migrations**: Alembic setup for database schema management
- **Mock Data**: Sample data for development and testing
- **Scripts**: Automation scripts for common tasks

### Production Ready
- **Infrastructure as Code**: Terraform and Kubernetes configurations
- **Monitoring**: Prometheus and Grafana setup
- **Security**: Environment variable examples and security configurations
- **Documentation**: Comprehensive documentation structure

## 🚀 Next Steps

After creating this structure, the next tasks would be:
1. Set up Python backend environment (T002)
2. Set up React/Next.js frontend environment (T003)
3. Configure development database (T004)
4. Set up Redis for caching (T005)
5. Create Docker configuration (T006)

This structure provides a solid foundation for the Agent Mira property recommendation system, following industry best practices and supporting the full development lifecycle from local development to production deployment.