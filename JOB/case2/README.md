# Agent Mira - AI-Powered Property Recommendation System

## Overview
Agent Mira is an AI-powered web application that recommends the best-matching properties to homebuyers based on their preferences. It uses a machine learning model to predict property prices and a scoring engine to rank listings.

---

## Features
- User-friendly web form for homebuyer preferences
- AI-powered backend with price prediction and scoring
- Top 3 property recommendations with clear reasoning
- Modern Next.js frontend and FastAPI backend
- Fully containerized for easy deployment

---

## Architecture
- **Frontend:** Next.js (React, TypeScript)
- **Backend:** FastAPI (Python 3.10)
- **ML Model:** Pickled model (`docs/complex_price_model_v2.pkl`)
- **Data:** Merged and augmented JSON (`docs/merged_properties.json`)
- **Containerization:** Docker, Docker Compose

See `docs/architecture_design.md` for details.

---

## Quick Start (Docker Compose)

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd <your-repo>
   ```
2. **Build and start services:**
   ```sh
   docker-compose up --build
   ```
3. **Access the app:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Local Development (without Docker)

### Backend
1. Install Python 3.10+
2. Install dependencies:
   ```sh
   cd server
   pip install -r requirements.txt
   ```
3. Start FastAPI server:
   ```sh
   uvicorn server.main:app --reload
   ```

### Frontend
1. Install Node.js 18+
2. Install dependencies:
   ```sh
   cd client
   npm install
   ```
3. Start Next.js dev server:
   ```sh
   npm run dev
   ```
4. Update API endpoint in frontend if backend runs on a different port or host.

---

## Usage
1. Open the web app in your browser.
2. Fill out your homebuying preferences and submit.
3. View the top 3 recommended properties with detailed reasoning.

---

## Troubleshooting
- **Backend errors:** Check logs in the Docker container or terminal.
- **Frontend errors:** Check browser console and terminal output.
- **Model loading issues:** Ensure `docs/complex_price_model_v2.pkl` is present and compatible.
- **Data issues:** Ensure `docs/merged_properties.json` exists (run the data loader if needed).

---

## Documentation
- [Product Requirements (PRD.md)](./PRD.md)
- [Architecture & Design](./docs/architecture_design.md)
- [Monitoring & Error Handling](./docs/monitoring_logging_error_handling.md)

---

## License
MIT (or your license here) 