# Phase 1: Foundation & Local AI Setup - Complete Beginner's Guide

*This guide assumes you're starting from scratch and explains every concept, command, and decision along the way.*

## Before We Begin: Understanding the Big Picture

Think of building ARIA like constructing a house. Phase 1 is laying the foundation and installing the basic utilities. We're not building the beautiful rooms yet, but without this solid foundation, nothing else will work properly.

### What You'll Learn
By the end of Phase 1, you'll understand how to set up a complete development environment, work with local AI models, create a memory system, and build basic AI agents. More importantly, you'll understand *why* each piece is necessary and how they work together.

### Prerequisites
- A computer with at least 16GB RAM (32GB recommended for running AI models)
- Basic familiarity with using a terminal/command line
- Willingness to learn and experiment
- About 40-60 hours of dedicated time over 6 weeks

---

## Week 1-2: Development Environment & Core Infrastructure

### Understanding Development Environments

Before diving into code, let's understand what a development environment is. Think of it as your workshop where you build software. Just like a carpenter needs a well-organized workshop with the right tools, you need a properly configured development environment.

**Why Docker?** Docker is like having a magical box that contains everything your application needs to run, regardless of what computer it's on. This means your ARIA will work the same way on your development machine, your friend's computer, or a server in the cloud.

### Day 1: Setting Up Your Foundation

#### Step 1: Install Required Tools

**Installing Docker Desktop**
Docker Desktop is your gateway to containerized development. Here's why we use it and how to set it up:

1. **Download Docker Desktop** from docker.com
   - Choose your operating system (Windows, Mac, or Linux)
   - The installer will guide you through the process

2. **Verify Installation**
   ```bash
   # Open your terminal and run:
   docker --version
   docker compose --version
   
   # You should see version numbers, not error messages
   ```

**Why This Matters:** Docker ensures that when you say "it works on my machine," it will actually work on any machine. This eliminates the frustrating "dependency hell" where different versions of software conflict with each other.

**Installing Git**
Git is your time machine for code. It tracks every change you make and lets you go back to any previous version.

1. **Download Git** from git-scm.com
2. **Configure Git** with your identity:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

**Installing a Code Editor**
I recommend Visual Studio Code because it's free, powerful, and has excellent extensions for our project:

1. **Download VS Code** from code.visualstudio.com
2. **Install Essential Extensions:**
   - Python (by Microsoft)
   - Docker (by Microsoft)
   - GitLens (for better Git integration)
   - REST Client (for testing APIs)

#### Step 2: Understanding Project Structure

Let's create your project directory and understand why each folder exists:

```bash
# Create your main project directory
mkdir aria
cd aria

# Create the complete directory structure
mkdir -p backend/{api,core,agents,memory,tests}
mkdir -p frontend/{components,pages,public,styles}
mkdir -p docker/{backend,frontend,db}
mkdir -p docs
mkdir -p scripts
```

**Understanding Each Directory:**

- **backend/**: Contains all server-side code that processes requests and runs AI models
  - **api/**: Web endpoints that your frontend will call (like asking questions to ARIA)
  - **core/**: Essential services like the AI model manager and logging
  - **agents/**: Different AI personalities and specialized functions
  - **memory/**: Systems for storing and retrieving conversations and learned information
  - **tests/**: Code that verifies everything works correctly

- **frontend/**: The user interface that you'll interact with
  - **components/**: Reusable UI pieces (like chat bubbles, buttons)
  - **pages/**: Complete screens (like the main chat page, settings page)
  - **public/**: Static files like images and icons
  - **styles/**: Visual styling for the interface

- **docker/**: Configuration files for containerizing each part of the system
- **docs/**: Documentation for your project
- **scripts/**: Helpful automation scripts

#### Step 3: Initialize Git Repository

Think of Git as creating a detailed journal of your project's development:

```bash
# Initialize Git in your project
git init

# Create a .gitignore file to exclude sensitive or unnecessary files
cat << EOF > .gitignore
# Python
__pycache__/
*.py[cod]
*.so
.env
.venv/
env/
venv/

# Node.js
node_modules/
npm-debug.log*
.npm

# Docker
.docker/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite

# Logs
*.log

# AI Models (these are large files)
models/
*.bin
*.gguf
EOF

# Make your first commit
git add .
git commit -m "Initial project structure"
```

**Why .gitignore?** Some files shouldn't be tracked by Git because they're either generated automatically, contain sensitive information, or are too large. The .gitignore file tells Git to ignore these files.

### Day 2: Creating Docker Configuration

Docker Compose is like a recipe that tells Docker how to set up multiple containers that work together. Let's create this recipe for ARIA:

#### Understanding the Docker Compose File

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Backend service - runs our Python API server
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"  # Maps port 8000 on your computer to port 8000 in the container
    volumes:
      - ./backend:/app  # Connects your local code to the container
      - ./models:/app/models  # Shared folder for AI models
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://aria_user:aria_password@db:5432/aria_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    networks:
      - aria-network

  # Database service - stores structured data
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: aria_db
      POSTGRES_USER: aria_user
      POSTGRES_PASSWORD: aria_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    networks:
      - aria-network

  # Redis service - fast caching and session storage
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - aria-network

  # ChromaDB service - vector database for AI memory
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chromadb_data:/chroma/chroma
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
    networks:
      - aria-network

# Named volumes for persistent data storage
volumes:
  postgres_data:
  redis_data:
  chromadb_data:

# Custom network for service communication
networks:
  aria-network:
    driver: bridge
```

**Understanding Each Service:**

- **Backend**: Your Python application that handles all the AI processing
- **Database (PostgreSQL)**: Stores structured data like user preferences, conversation metadata
- **Redis**: Ultra-fast storage for temporary data like active conversations
- **ChromaDB**: Specialized database for storing and searching AI-generated embeddings (vector representations of text)

#### Creating the Backend Dockerfile

The Dockerfile is like a recipe for creating your backend container:

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker layer caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Key Concepts Explained:**

- **Layer Caching**: By copying requirements.txt first, Docker can reuse the dependency installation layer when only your code changes
- **Non-root User**: Running as a non-root user improves security
- **Health Check**: Allows Docker to verify your application is working correctly

#### Creating Initial Requirements

```text
# backend/requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.0
asyncpg==0.29.0
redis==5.0.1
chromadb==0.4.18
langchain==0.0.350
langchain-community==0.0.1
langgraph==0.0.20
requests==2.31.0
httpx==0.25.2
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==7.4.3
pytest-asyncio==0.21.1
```

### Day 3-4: Setting Up Ollama for Local AI

Ollama is your local AI model server. Think of it as having ChatGPT running on your own computer, completely private and under your control.

#### Understanding Local vs Cloud AI

**Why Local AI?**
- **Privacy**: Your conversations never leave your computer
- **Cost**: No API fees or usage limits
- **Speed**: No internet latency for processing
- **Control**: You choose exactly which models to use
- **Availability**: Works offline

**The Trade-off**: Local models require significant computer resources and may not be as capable as the largest cloud models, but they're perfect for a personal assistant that respects your privacy.

#### Installing Ollama

**On macOS:**
```bash
# Install using Homebrew (recommended)
brew install ollama

# Or download from ollama.ai
```

**On Windows:**
1. Download the installer from ollama.ai
2. Run the installer and follow the prompts

**On Linux:**
```bash
# Install script
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Starting Ollama and Downloading Models

```bash
# Start Ollama service
ollama serve

# In a new terminal, download models (this will take time!)
# Llama 3.1 8B - General purpose, good balance of capability and speed
ollama pull llama3.1:8b

# Mistral 7B - Faster responses, good for quick interactions
ollama pull mistral:7b

# CodeLlama 7B - Specialized for code assistance
ollama pull codellama:7b

# Test that models work
ollama run llama3.1:8b "Hello, how are you?"
```

**Understanding Model Sizes:**
- **7B**: 7 billion parameters, faster but less capable
- **8B**: 8 billion parameters, good balance
- **13B**: 13 billion parameters, more capable but slower
- **70B**: 70 billion parameters, very capable but requires lots of memory

#### Creating the LLM Manager

Now let's create the code that manages these AI models:

```python
# backend/core/llm_manager.py
import asyncio
import httpx
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Set up logging to track what's happening
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for an AI model"""
    name: str
    endpoint: str
    description: str
    max_tokens: int
    temperature_range: tuple[float, float]

class LLMManager:
    """
    Manages communication with local AI models through Ollama.
    
    Think of this as a translator between ARIA and the AI models.
    It handles sending questions to models and getting responses back.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.models = {
            "general": ModelConfig(
                name="llama3.1:8b",
                endpoint=f"{base_url}/api/generate",
                description="General conversation and reasoning",
                max_tokens=4000,
                temperature_range=(0.1, 1.0)
            ),
            "fast": ModelConfig(
                name="mistral:7b", 
                endpoint=f"{base_url}/api/generate",
                description="Quick responses for simple queries",
                max_tokens=2000,
                temperature_range=(0.1, 0.8)
            ),
            "coding": ModelConfig(
                name="codellama:7b",
                endpoint=f"{base_url}/api/generate", 
                description="Code assistance and technical queries",
                max_tokens=3000,
                temperature_range=(0.0, 0.6)
            )
        }
        
        # HTTP client for making requests to Ollama
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate_response(
        self,
        prompt: str,
        model_type: str = "general",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a response from the AI model.
        
        Args:
            prompt: The question or input for the AI
            model_type: Which model to use ("general", "fast", "coding")
            temperature: How creative the response should be (0.0-1.0)
            max_tokens: Maximum length of response
            system_prompt: Instructions for how the AI should behave
            
        Returns:
            The AI's response as a string, or None if there was an error
        """
        
        if model_type not in self.models:
            logger.error(f"Unknown model type: {model_type}")
            return None
            
        config = self.models[model_type]
        
        # Validate temperature is within acceptable range
        min_temp, max_temp = config.temperature_range
        temperature = max(min_temp, min(max_temp, temperature))
        
        # Build the complete prompt with system instructions
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        
        request_data = {
            "model": config.name,
            "prompt": full_prompt,
            "options": {
                "temperature": temperature,
                "num_predict": min(max_tokens, config.max_tokens)
            },
            "stream": False  # Get complete response at once
        }
        
        try:
            logger.info(f"Sending request to {config.name} model")
            response = await self.client.post(
                config.endpoint,
                json=request_data
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract the response text
            if "response" in result:
                generated_text = result["response"].strip()
                logger.info(f"Successfully generated {len(generated_text)} characters")
                return generated_text
            else:
                logger.error(f"Unexpected response format: {result}")
                return None
                
        except httpx.TimeoutException:
            logger.error("Request timed out - model might be slow or overloaded")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error generating response: {e}")
            return None
    
    async def list_available_models(self) -> List[Dict[str, str]]:
        """
        Get a list of all models available in Ollama.
        
        This is useful for checking which models are installed
        and available for use.
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            
            data = response.json()
            models = []
            
            for model in data.get("models", []):
                models.append({
                    "name": model.get("name", "Unknown"),
                    "size": self._format_size(model.get("size", 0)),
                    "modified": model.get("modified_at", "Unknown")
                })
            
            return models
            
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def _format_size(self, size_bytes: int) -> str:
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    async def health_check(self) -> bool:
        """
        Check if Ollama is running and responding.
        
        Returns True if healthy, False otherwise.
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Clean up resources when shutting down"""
        await self.client.aclose()

# Example usage and testing
async def test_llm_manager():
    """Test function to verify the LLM manager works correctly"""
    manager = LLMManager()
    
    # Check if Ollama is running
    if not await manager.health_check():
        print("❌ Ollama is not running. Please start it with 'ollama serve'")
        return
    
    print("✅ Ollama is running")
    
    # List available models
    models = await manager.list_available_models()
    print(f"📋 Available models: {len(models)}")
    for model in models:
        print(f"  - {model['name']} ({model['size']})")
    
    # Test generating a response
    print("\n🤖 Testing response generation...")
    response = await manager.generate_response(
        prompt="What is artificial intelligence?",
        model_type="general",
        temperature=0.7,
        max_tokens=200
    )
    
    if response:
        print(f"✅ Response generated successfully:")
        print(f"📝 {response[:100]}..." if len(response) > 100 else response)
    else:
        print("❌ Failed to generate response")
    
    await manager.close()

# Run the test if this file is executed directly
if __name__ == "__main__":
    asyncio.run(test_llm_manager())
```

#### Testing Your Setup

Create a simple test script to verify everything works:

```python
# backend/test_setup.py
import asyncio
from core.llm_manager import LLMManager

async def main():
    print("🚀 Testing ARIA Foundation Setup")
    print("=" * 40)
    
    # Test LLM Manager
    llm = LLMManager()
    
    # Check Ollama health
    if await llm.health_check():
        print("✅ Ollama is running and healthy")
        
        # List models
        models = await llm.list_available_models()
        print(f"📋 Found {len(models)} available models")
        
        # Test generation
        response = await llm.generate_response(
            "Hello! Please introduce yourself as ARIA.",
            model_type="general"
        )
        
        if response:
            print("✅ AI response generation successful")
            print(f"🤖 ARIA says: {response}")
        else:
            print("❌ AI response generation failed")
    else:
        print("❌ Ollama is not accessible")
        print("💡 Make sure to run 'ollama serve' in another terminal")
    
    await llm.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Day 5: Logging and Monitoring Foundation

Good logging is like having a detailed diary of everything your application does. When something goes wrong, logs help you understand what happened and why.

#### Understanding Structured Logging

Traditional logging just writes text messages. Structured logging writes data in a consistent format (JSON) that can be easily searched and analyzed.

```python
# backend/core/logging.py
import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """
    Custom formatter that converts log records to JSON.
    
    This makes logs machine-readable and easier to search through.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        # Start with basic log information
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread
        }
        
        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add any extra fields passed to the log call
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data, ensure_ascii=False)

class ContextFilter(logging.Filter):
    """
    Filter that adds contextual information to log records.
    
    This helps track requests and user sessions across multiple log entries.
    """
    
    def filter(self, record):
        # Add default context if not present
        if not hasattr(record, 'request_id'):
            record.request_id = 'unknown'
        if not hasattr(record, 'user_id'):
            record.user_id = 'anonymous'
        return True

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True
) -> logging.Logger:
    """
    Set up application logging with both console and file output.
    
    Args:
        log_level: Minimum level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        enable_console: Whether to also log to console
        
    Returns:
        Configured logger instance
    """
    
    # Create main logger
    logger = logging.getLogger("aria")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = JSONFormatter()
    
    # Add console handler if requested
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(ContextFilter())
        logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(ContextFilter())
        logger.addHandler(file_handler)
    
    # Prevent duplicate logs from parent loggers
    logger.propagate = False
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module or component"""
    return logging.getLogger(f"aria.{name}")

# Convenience functions for common logging patterns
def log_api_call(logger: logging.Logger, endpoint: str, method: str, 
                status_code: int, duration_ms: float, **kwargs):
    """Log an API call with standard fields"""
    logger.info(
        f"API call completed",
        extra={
            'extra_fields': {
                'endpoint': endpoint,
                'method': method,
                'status_code': status_code,
                'duration_ms': duration_ms,
                **kwargs
            }
        }
    )

def log_ai_generation(logger: logging.Logger, model: str, prompt_length: int,
                     response_length: int, duration_ms: float, **kwargs):
    """Log an AI generation request with standard fields"""
    logger.info(
        f"AI generation completed",
        extra={
            'extra_fields': {
                'model': model,
                'prompt_length': prompt_length,
                'response_length': response_length,
                'duration_ms': duration_ms,
                **kwargs
            }
        }
    )

def log_memory_operation(logger: logging.Logger, operation: str, 
                        collection: str, count: int, **kwargs):
    """Log a memory/database operation with standard fields"""
    logger.info(
        f"Memory operation completed",
        extra={
            'extra_fields': {
                'operation': operation,
                'collection': collection,
                'count': count,
                **kwargs
            }
        }
    )

# Example usage
if __name__ == "__main__":
    # Set up logging
    logger = setup_logging(
        log_level="INFO",
        log_file="logs/aria.log",
        enable_console=True
    )
    
    # Test different log levels and patterns
    logger.info("ARIA logging system initialized")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    
    # Test structured logging
    api_logger = get_logger("api")
    log_api_call(
        api_logger,
        endpoint="/chat",
        method="POST",
        status_code=200,
        duration_ms=150.5,
        user_id="user123"
    )
    
    # Test AI logging
    ai_logger = get_logger("ai")
    log_ai_generation(
        ai_logger,
        model="llama3.1:8b",
        prompt_length=50,
        response_length=200,
        duration_ms=1200.0,
        temperature=0.7
    )
```

#### Creating Health Check Endpoints

Health checks tell you and external systems whether your application is working correctly:

```python
# backend/api/health.py
from fastapi import APIRouter, Response, status, Depends
from typing import Dict, Any
import asyncio
from datetime import datetime, timezone

from core.llm_manager import LLMManager
from core.logging import get_logger

router = APIRouter()
logger = get_logger("health")

# Dependency to get LLM manager
async def get_llm_manager():
    return LLMManager()

@router.get("/health")
async def basic_health_check() -> Dict[str, Any]:
    """
    Basic health check - just confirms the API is responding.
    
    This is the simplest check - if you get a response, the basic
    web server is working.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "aria-api"
    }

@router.get("/health/ready")
async def readiness_check(
    response: Response,
    llm_manager: LLMManager = Depends(get_llm_manager)
) -> Dict[str, Any]:
    """
    Readiness check - confirms all dependencies are working.
    
    This checks that all the services ARIA needs are available:
    - AI models (Ollama)
    - Database connections
    - Any other critical services
    """
    
    checks = {}
    overall_healthy = True
    
    # Check AI models
    try:
        ollama_healthy = await llm_manager.health_check()
        checks["ollama"] = {
            "status": "healthy" if ollama_healthy else "unhealthy",
            "details": "AI model server"
        }
        if not ollama_healthy:
            overall_healthy = False
    except Exception as e:
        checks["ollama"] = {
            "status": "error",
            "details": f"Error checking Ollama: {str(e)}"
        }
        overall_healthy = False
    
    # TODO: Add database checks when we implement them
    # TODO: Add memory store checks when we implement them
    
    # Set appropriate HTTP status code
    if overall_healthy:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
    await llm_manager.close()
    
    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks
    }

@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check - confirms the application process is alive.
    
    This is used by container orchestrators to know if they should
    restart the application.
    """
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/health/startup")
async def startup_check(response: Response) -> Dict[str, Any]:
    """
    Startup check - confirms the application has finished initializing.
    
    This prevents traffic from being sent to the application before
    it's fully ready to handle requests.
    """
    
    # TODO: Add actual startup checks (model loading, etc.)
    startup_complete = True
    
    if startup_complete:
        response.status_code = status.HTTP_200_OK
        return {
            "status": "ready",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "starting",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
```

### Day 6: Building Your First FastAPI Application

Now let's put it all together into a working web application:

```python
# backend/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import time
from typing import Dict, Any

from core.logging import setup_logging, get_logger, log_api_call
from core.llm_manager import LLMManager
from api.health import router as health_router

# Global variables for shared resources
llm_manager: LLMManager = None
logger = None

@asynccontextmanager
async def lifespan
