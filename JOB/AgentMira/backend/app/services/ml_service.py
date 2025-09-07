"""
ML Model Service for property price prediction
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class MLModelService:
    """Service for handling ML model operations"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self) -> bool:
        """Load the ML model from file"""
        try:
            model_path = settings.ml_model_path
            self.model = joblib.load(model_path)
            self.model_loaded = True
            logger.info(f"ML model loaded successfully from {model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load ML model: {str(e)}")
            self.model_loaded = False
            return False
    
    def predict_price(self, property_features: Dict[str, Any]) -> Optional[float]:
        """
        Predict property price based on features
        
        Args:
            property_features: Dictionary containing property features
            
        Returns:
            Predicted price or None if prediction fails
        """
        if not self.model_loaded:
            logger.error("Model not loaded, cannot make predictions")
            return None
        
        try:
            # Convert features to DataFrame
            # Note: This is a placeholder - actual feature engineering depends on model requirements
            features_df = self._prepare_features(property_features)
            
            # Make prediction
            prediction = self.model.predict(features_df)
            
            # Return the first prediction (assuming single property)
            return float(prediction[0]) if len(prediction) > 0 else None
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return None
    
    def _prepare_features(self, property_features: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepare features for model prediction
        
        This is a placeholder implementation. The actual feature preparation
        depends on the specific model requirements and training data format.
        """
        # Extract relevant features
        features = {
            'bedrooms': property_features.get('bedrooms', 0),
            'bathrooms': property_features.get('bathrooms', 0),
            'size_sqft': property_features.get('size_sqft', 0),
            'year_built': property_features.get('year_built', 2020),
            'location_encoded': self._encode_location(property_features.get('location', '')),
            'amenities_count': len(property_features.get('amenities', [])),
        }
        
        # Convert to DataFrame
        return pd.DataFrame([features])
    
    def _encode_location(self, location: str) -> int:
        """
        Encode location string to numeric value
        
        This is a placeholder implementation. In a real scenario,
        you would use proper encoding techniques like label encoding
        or one-hot encoding based on the model's training data.
        """
        # Simple hash-based encoding for demonstration
        return hash(location) % 1000 if location else 0
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.model_loaded:
            return {"status": "not_loaded", "error": "Model not loaded"}
        
        try:
            # Get model attributes if available
            model_info = {
                "status": "loaded",
                "model_type": type(self.model).__name__,
                "model_path": settings.ml_model_path,
            }
            
            # Add model-specific information if available
            if hasattr(self.model, 'feature_names_in_'):
                model_info["features"] = self.model.feature_names_in_.tolist()
            
            if hasattr(self.model, 'n_features_in_'):
                model_info["n_features"] = self.model.n_features_in_
            
            return model_info
            
        except Exception as e:
            return {
                "status": "loaded",
                "error": f"Could not retrieve model info: {str(e)}"
            }
    
    def is_healthy(self) -> bool:
        """Check if the ML service is healthy"""
        return self.model_loaded

# Global ML service instance
ml_service = MLModelService()
