from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .model_service import ModelService
from .predict_price import predict_price
from .score import calculate_total_score
from .reasoning import generate_reasoning
import json
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic logging setup
logging.basicConfig(level=logging.INFO)

@app.exception_handler(Exception)
def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})

@app.on_event("startup")
def load_model_on_startup():
    ModelService.load_model()

@app.get('/')
def read_root():
    return {"message": "Agent Mira backend is running."}

@app.post('/recommendations')
def get_recommendations(user_prefs: dict):
    # Load properties
    data_path = os.path.join(os.path.dirname(__file__), '../docs/merged_properties.json')
    if not os.path.exists(data_path):
        raise HTTPException(status_code=500, detail="Property data not found.")
    with open(data_path, 'r') as f:
        properties = json.load(f)
    # Score all properties
    results = []
    for prop in properties:
        predicted = predict_price(prop)
        scores = calculate_total_score(prop, user_prefs, predicted)
        reasoning = generate_reasoning(prop, scores, user_prefs)
        results.append({
            'property': prop,
            'predicted_price': predicted,
            'total_match_score': scores['total_match_score'],
            'component_scores': scores['component_scores'],
            'reasoning': reasoning
        })
    # Sort and return top 3
    top = sorted(results, key=lambda x: x['total_match_score'], reverse=True)[:3]
    return {'recommendations': top} 