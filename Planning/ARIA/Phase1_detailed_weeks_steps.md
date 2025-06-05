# Phase 1: Foundation & Local AI Setup - Detailed Implementation Guide

## 🎯 Phase Overview

**What You'll Build:** A solid foundation for ARIA with local AI capabilities, memory systems, and agent framework.

**Why This Matters:** This phase establishes the core infrastructure that everything else builds upon. Think of it as laying the foundation for a house - everything depends on getting this right.

**End Goal:** By the end of this phase, you'll have a working local AI assistant that can:
- Process conversations using local LLMs (no cloud dependency)
- Store and retrieve memories
- Handle multiple AI agents working together
- Provide a solid API foundation for future features

## 📋 Prerequisites

Before starting, ensure you have:
- **Hardware:** 16GB+ RAM (32GB recommended for larger models)
- **Software:** Python 3.11+, Docker, Git
- **Skills:** Basic Python knowledge, familiarity with command line
- **Time:** ~40 hours over 6 weeks (6-8 hours per week)

## 🚀 Success Metrics

You'll know you've succeeded when:
- [ ] Local LLM responds to basic queries
- [ ] Memory system stores and retrieves information
- [ ] Agent framework processes workflows
- [ ] All tests pass
- [ ] API endpoints return expected responses

## Part 1: Development Environment Setup (Week 1)

### Day 1-2: Project Initialization

#### Steps:
1. Create project directory structure
2. Initialize Git repository with .gitignore
3. Set up Docker environment
4. Configure development tools

#### Code Snippets:

```bash
# Project Directory Structure
aria/
├── backend/
│   ├── api/
│   ├── core/
│   ├── agents/
│   ├── memory/
│   └── tests/
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── public/
│   └── styles/
└── docker/
    ├── backend/
    ├── frontend/
    └── db/
```

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - ENVIRONMENT=development
      
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: aria_db
      POSTGRES_USER: aria_user
      POSTGRES_PASSWORD: aria_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Day 3-4: Local LLM Setup

#### Steps:
1. Install Ollama
2. Download and configure base models
3. Set up LM Studio as backup
4. Create model management scripts

#### Code Snippets:

```python
# backend/core/llm_manager.py
from typing import Optional
import requests

class LLMManager:
    def __init__(self):
        self.ollama_base_url = "http://localhost:11434"
        self.models = {
            "general": "llama2:13b",
            "coding": "codellama:7b",
            "fast": "mistral:7b"
        }
    
    async def generate_response(
        self,
        prompt: str,
        model_type: str = "general",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.models[model_type],
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )
            return response.json().get("response")
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

    async def list_available_models(self) -> list:
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags")
            return response.json().get("models", [])
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
```

### Day 5: Logging & Monitoring

#### Steps:
1. Set up structured logging
2. Implement health checks
3. Configure monitoring endpoints
4. Create logging utilities

#### Code Snippets:

```python
# backend/core/logging.py
import logging
import json
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, "extra"):
            log_data.update(record.extra)
            
        return json.dumps(log_data)

def setup_logging():
    logger = logging.getLogger("aria")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    return logger
```

```python
# backend/api/health.py
from fastapi import APIRouter, Response, status
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness_check() -> Response:
    # Add checks for required services (database, LLM, etc.)
    services_ready = True
    
    if services_ready:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
```

## Part 2: Memory Foundation (Week 2)

### Day 1-2: ChromaDB Setup

#### Steps:
1. Install and configure ChromaDB
2. Create embedding pipeline
3. Implement basic vector operations
4. Set up memory schemas

#### Code Snippets:

```python
# backend/memory/vector_store.py
import chromadb
from chromadb.config import Settings
from typing import List, Optional

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./.chromadb"
        ))
        self.collection = self.client.create_collection(
            name="aria_memory",
            metadata={"description": "ARIA's primary memory store"}
        )
    
    async def store_memory(
        self,
        text: str,
        metadata: dict,
        id: Optional[str] = None
    ) -> str:
        memory_id = id or str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[memory_id]
        )
        return memory_id
    
    async def search_memories(
        self,
        query: str,
        n_results: int = 5
    ) -> List[dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return [
            {"text": doc, "metadata": meta}
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
```

### Day 3-4: Memory Management System

#### Steps:
1. Implement short-term memory
2. Create long-term memory storage
3. Build episodic memory system
4. Set up memory persistence

#### Code Snippets:

```python
# backend/memory/memory_manager.py
from datetime import datetime
from typing import Optional, List, Dict
from .vector_store import VectorStore

class MemoryManager:
    def __init__(self):
        self.vector_store = VectorStore()
        self.short_term_memory: List[Dict] = []
        self.max_short_term_size = 10
    
    async def add_memory(
        self,
        content: str,
        memory_type: str,
        importance: float = 0.5,
        metadata: Optional[Dict] = None
    ):
        base_metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": memory_type,
            "importance": importance
        }
        
        if metadata:
            base_metadata.update(metadata)
            
        if memory_type == "short_term":
            self.short_term_memory.append({
                "content": content,
                "metadata": base_metadata
            })
            
            if len(self.short_term_memory) > self.max_short_term_size:
                self._consolidate_memories()
        else:
            await self.vector_store.store_memory(
                text=content,
                metadata=base_metadata
            )
    
    async def _consolidate_memories(self):
        # Consolidate short-term memories into long-term storage
        consolidated = "\n".join(
            [m["content"] for m in self.short_term_memory]
        )
        
        await self.vector_store.store_memory(
            text=consolidated,
            metadata={
                "type": "consolidated",
                "timestamp": datetime.utcnow().isoformat(),
                "source_count": len(self.short_term_memory)
            }
        )
        
        self.short_term_memory.clear()
```

### Day 5: Memory Testing

#### Steps:
1. Create test suite for memory operations
2. Verify persistence functionality
3. Test retrieval accuracy
4. Implement memory benchmarks

#### Code Snippets:

```python
# backend/tests/test_memory.py
import pytest
from memory.memory_manager import MemoryManager
from memory.vector_store import VectorStore

@pytest.fixture
async def memory_manager():
    return MemoryManager()

@pytest.mark.asyncio
async def test_short_term_memory(memory_manager):
    test_content = "Test memory content"
    await memory_manager.add_memory(
        content=test_content,
        memory_type="short_term"
    )
    
    assert len(memory_manager.short_term_memory) == 1
    assert memory_manager.short_term_memory[0]["content"] == test_content

@pytest.mark.asyncio
async def test_memory_consolidation(memory_manager):
    # Add more than max_short_term_size memories
    for i in range(memory_manager.max_short_term_size + 1):
        await memory_manager.add_memory(
            content=f"Memory {i}",
            memory_type="short_term"
        )
    
    # Check if consolidation occurred
    assert len(memory_manager.short_term_memory) == 0
    
    # Verify consolidated memory in vector store
    results = await memory_manager.vector_store.search_memories(
        query="Memory",
        n_results=1
    )
    assert len(results) == 1
    assert "Memory" in results[0]["text"]
```

## Part 3: Agent Framework (Week 3-4)

### Day 1-3: LangGraph Setup

#### Steps:
1. Install and configure LangGraph
2. Create basic agent templates
3. Set up workflow orchestration
4. Implement agent communication

#### Code Snippets:

```python
# backend/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.state: Dict[str, Any] = {}
    
    @abstractmethod
    async def process_message(self, message: str) -> str:
        pass
    
    @abstractmethod
    async def update_state(self, data: Dict[str, Any]):
        pass
    
    async def get_state(self) -> Dict[str, Any]:
        return self.state
```

```python
# backend/agents/conversation_agent.py
from .base_agent import BaseAgent
from core.llm_manager import LLMManager

class ConversationAgent(BaseAgent):
    def __init__(self):
        super().__init__("conversation")
        self.llm = LLMManager()
    
    async def process_message(self, message: str) -> str:
        # Add conversation context
        context = self._build_context()
        
        # Generate response using LLM
        response = await self.llm.generate_response(
            prompt=f"{context}\nUser: {message}\nAssistant:",
            model_type="general"
        )
        
        # Update conversation history
        self._update_history(message, response)
        
        return response
    
    async def update_state(self, data: Dict[str, Any]):
        self.state.update(data)
    
    def _build_context(self) -> str:
        history = self.state.get("conversation_history", [])
        return "\n".join(history[-5:])  # Last 5 exchanges
    
    def _update_history(self, user_message: str, assistant_response: str):
        if "conversation_history" not in self.state:
            self.state["conversation_history"] = []
        
        self.state["conversation_history"].extend([
            f"User: {user_message}",
            f"Assistant: {assistant_response}"
        ])
```

### Day 4-5: Agent Communication

#### Steps:
1. Implement message passing
2. Create agent registry
3. Set up event system
4. Build workflow manager

#### Code Snippets:

```python
# backend/agents/agent_registry.py
from typing import Dict, Type
from .base_agent import BaseAgent

class AgentRegistry:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.agents: Dict[str, BaseAgent] = {}
            cls._instance.agent_types: Dict[str, Type[BaseAgent]] = {}
        return cls._instance
    
    def register_agent_type(self, name: str, agent_class: Type[BaseAgent]):
        self.agent_types[name] = agent_class
    
    def create_agent(self, agent_type: str) -> BaseAgent:
        if agent_type not in self.agent_types:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent = self.agent_types[agent_type]()
        self.agents[agent.name] = agent
        return agent
    
    def get_agent(self, name: str) -> BaseAgent:
        return self.agents.get(name)
```

```python
# backend/agents/workflow_manager.py
from typing import List, Dict, Any
from .agent_registry import AgentRegistry

class WorkflowManager:
    def __init__(self):
        self.registry = AgentRegistry()
        self.workflows: Dict[str, List[str]] = {}
    
    async def execute_workflow(
        self,
        workflow_name: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        result = input_data
        for agent_name in self.workflows[workflow_name]:
            agent = self.registry.get_agent(agent_name)
            if agent:
                result = await agent.process_message(str(result))
        
        return {"result": result}
    
    def register_workflow(self, name: str, agent_sequence: List[str]):
        self.workflows[name] = agent_sequence
```

## Part 4: Testing & Integration (Week 5-6)

### Day 1-3: Component Testing

#### Steps:
1. Create test suites for each component
2. Implement integration tests
3. Set up CI/CD pipeline
4. Create test utilities

#### Code Snippets:

```python
# backend/tests/test_agents.py
import pytest
from agents.conversation_agent import ConversationAgent
from agents.agent_registry import AgentRegistry

@pytest.fixture
def agent_registry():
    registry = AgentRegistry()
    registry.register_agent_type("conversation", ConversationAgent)
    return registry

@pytest.mark.asyncio
async def test_conversation_agent(agent_registry):
    agent = agent_registry.create_agent("conversation")
    
    # Test basic conversation
    response = await agent.process_message("Hello!")
    assert response and isinstance(response, str)
    
    # Test conversation history
    state = await agent.get_state()
    assert "conversation_history" in state
    assert len(state["conversation_history"]) == 2  # User + Assistant
```

### Day 4-5: System Integration

#### Steps:
1. Connect all components
2. Implement error handling
3. Add system monitoring
4. Create deployment scripts

#### Code Snippets:

```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from typing import Dict, Any

from core.logging import setup_logging
from agents.workflow_manager import WorkflowManager
from api.health import router as health_router

app = FastAPI(title="ARIA API")
logger = setup_logging()
workflow_manager = WorkflowManager()

# Register routes
app.include_router(health_router, tags=["health"])

@app.post("/chat")
async def chat(
    message: Dict[str, Any]
) -> Dict[str, Any]:
    try:
        response = await workflow_manager.execute_workflow(
            workflow_name="chat",
            input_data=message
        )
        return response
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

# Initialize components
@app.on_event("startup")
async def startup():
    # Register agents and workflows
    registry = AgentRegistry()
    registry.register_agent_type("conversation", ConversationAgent)
    
    workflow_manager.register_workflow(
        name="chat",
        agent_sequence=["conversation"]
    )
```

### Day 6-10: Documentation & Optimization

#### Steps:
1. Write technical documentation
2. Create API documentation
3. Optimize performance
4. Implement caching

#### Code Snippets:

```python
# backend/core/cache.py
from typing import Any, Optional
from redis import Redis
import json

class Cache:
    def __init__(self):
        self.redis = Redis(
            host="localhost",
            port=6379,
            db=0
        )
        self.default_ttl = 3600  # 1 hour
    
    async def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )
    
    async def delete(self, key: str):
        self.redis.delete(key)
```

```python
# backend/core/performance.py
from functools import wraps
import time
from typing import Callable, Any

def measure_performance(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        
        # Log performance metrics
        logger.info(
            "Performance measurement",
            extra={
                "function": func.__name__,
                "duration_ms": (end_time - start_time) * 1000,
                "args_count": len(args),
                "kwargs_count": len(kwargs)
            }
        )
        
        return result
    return wrapper
```