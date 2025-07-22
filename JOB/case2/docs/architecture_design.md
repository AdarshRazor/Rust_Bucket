# Agent Mira MVP: Architecture & Design Document

## Overview
Agent Mira is an AI-powered property recommendation system. The MVP consists of a FastAPI backend (Python) and a Next.js frontend (React/Node), orchestrated via Docker Compose.

---

## 1. System Architecture Diagram

```
+-------------------+        HTTP        +-------------------+
|                   | <---------------> |                   |
|    Frontend       |                   |     Backend       |
|  (Next.js, React) | <---Docker Net--->|  (FastAPI, Python)|
|                   |                   |                   |
+-------------------+                   +-------------------+
         |                                      |
         |                                      |
         |                                      v
         |                              +-------------------+
         |                              |   Model & Data    |
         |                              | (Pickle, JSON)    |
         |                              +-------------------+
```

---

## 2. Technology Choices
- **Frontend:** Next.js (React, TypeScript)
- **Backend:** FastAPI (Python 3.10)
- **ML Model:** Pickled scikit-learn or custom model
- **Data:** JSON files, mocked fields
- **Containerization:** Docker, Docker Compose

---

## 3. Scaling for 1k Users
- **Single Docker Compose deployment** on a VM or cloud instance
- **Backend:** Uvicorn with workers (e.g., `--workers 4`)
- **Frontend:** Next.js dev or production mode
- **Stateless:** No DB, all data in JSON/model files
- **Load:** Can handle 1k users with moderate hardware (2-4 vCPUs, 4-8GB RAM)

---

## 4. Scaling for 20k Users
- **Backend:**
  - Deploy with a production WSGI server (e.g., Gunicorn + Uvicorn workers)
  - Use a load balancer (e.g., Nginx, AWS ALB)
  - Horizontal scaling: multiple backend containers
  - Move model/data to a shared volume or object storage (e.g., S3)
- **Frontend:**
  - Deploy static build to CDN (Vercel, Netlify, S3+CloudFront)
  - Use environment variables for API endpoint
- **Observability:**
  - Add monitoring (Prometheus, Grafana)
  - Centralized logging (ELK, Loki)
- **Persistence:**
  - For production, migrate to a real database (Postgres, MongoDB)

---

## 5. Security & Best Practices
- Use HTTPS in production
- Restrict CORS as needed
- Do not expose model files publicly
- Use environment variables for secrets

---

## 6. Future Enhancements
- Add authentication & user accounts
- Integrate real property data sources
- Add caching (Redis) for model predictions
- Autoscale with Kubernetes

---

*This document covers both MVP and future scaling for 1k and 20k users.* 