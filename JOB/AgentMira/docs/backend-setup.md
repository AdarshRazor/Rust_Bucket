# Agent Mira - Backend Requirements & Configuration

## requirements.txt
```
# FastAPI Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Redis
redis==5.0.1
hiredis==2.2.3

# ML & Data Processing
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.24.4
joblib==1.3.2

# Validation & Serialization
pydantic==2.5.0
pydantic-settings==2.0.3

# HTTP Client
httpx==0.25.2
requests==2.31.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Utilities
python-dotenv==1.0.0
structlog==23.2.0
rich==13.7.0

# Development & Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
faker==20.1.0

# Monitoring & Logging
sentry-sdk[fastapi]==1.38.0
prometheus-client==0.19.0

# Performance
python-json-logger==2.0.7
aiofiles==23.2.1
```

## Backend Dockerfile
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

## alembic.ini
```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version number format.  This value should be a string
# that is a Python string format template for the version
# number
version_num_format = 1_%%(year)04d%%(month)02d%%(day)02d_%%(hour)02d%%(minute)02d

# path to the .env file
# (defaults to the root of the script location)
# dotenv_path = /path/to/.env

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = postgresql://username:password@localhost:5432/agent_mira_dev

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## Backend main.py
```python
"""
Agent Mira - FastAPI Application Entry Point
"""
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import structlog

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.api.api import api_router
from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.utils.logging import configure_logging
from app.utils.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    """
    # Startup
    configure_logging()
    logger = structlog.get_logger()
    logger.info("Starting Agent Mira API", version=settings.API_VERSION)
    
    # Load ML model on startup
    try:
        from app.ml.model_wrapper import ModelWrapper
        model_wrapper = ModelWrapper()
        model_wrapper.load_model()
        app.state.ml_model = model_wrapper
        logger.info("ML model loaded successfully")
    except Exception as e:
        logger.error("Failed to load ML model", error=str(e))
        app.state.ml_model = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Mira API")


# Create FastAPI application
app = FastAPI(
    title="Agent Mira API",
    description="AI-Powered Property Recommendation System",
    version=settings.API_VERSION,
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle custom application exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "code": exc.code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger = structlog.get_logger()
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR"}
    )


# Include API routes
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agent Mira API",
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "ml_model_loaded": hasattr(app.state, 'ml_model') and app.state.ml_model is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
```