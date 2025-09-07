"""
API routes for Agent Mira Property Recommendation System
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from app.core.database import get_db, get_redis
from app.models.property import Property
from app.models.user_preference import UserPreference
from app.services.ml_service import ml_service
from app.services.recommendation_service import recommendation_service

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "agent-mira-api",
        "ml_service": ml_service.is_healthy()
    }

@router.post("/preferences", response_model=Dict[str, Any])
async def submit_preferences(
    preferences: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Submit user preferences for property recommendations
    
    Expected payload:
    {
        "session_id": "unique_session_id",
        "budget": 500000,
        "location": "New York, NY",
        "min_bedrooms": 2,
        "max_commute_time": 30,
        "min_school_rating": 7.0,
        "preferred_amenities": ["Gym", "Pool", "Parking"]
    }
    """
    try:
        # Validate required fields
        required_fields = ["session_id", "budget"]
        for field in required_fields:
            if field not in preferences:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}"
                )
        
        # Create user preference record
        user_preference = UserPreference(
            session_id=preferences["session_id"],
            budget=preferences["budget"],
            location=preferences.get("location"),
            min_bedrooms=preferences.get("min_bedrooms"),
            max_commute_time=preferences.get("max_commute_time"),
            min_school_rating=preferences.get("min_school_rating"),
            preferred_amenities=preferences.get("preferred_amenities", [])
        )
        
        db.add(user_preference)
        db.commit()
        db.refresh(user_preference)
        
        return {
            "message": "Preferences submitted successfully",
            "preference_id": user_preference.id,
            "session_id": user_preference.session_id
        }
        
    except Exception as e:
        logger.error(f"Error submitting preferences: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit preferences"
        )

@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_recommendations(
    session_id: str,
    top_n: int = 3,
    db: Session = Depends(get_db)
):
    """
    Get property recommendations based on user preferences
    
    Args:
        session_id: User session identifier
        top_n: Number of recommendations to return (default: 3)
    """
    try:
        # Get user preferences
        user_preference = db.query(UserPreference).filter(
            UserPreference.session_id == session_id
        ).order_by(UserPreference.created_at.desc()).first()
        
        if not user_preference:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No preferences found for this session"
            )
        
        # Get all properties
        properties = db.query(Property).all()
        
        if not properties:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No properties available"
            )
        
        # Convert properties to dictionaries
        property_data = [prop.to_dict() for prop in properties]
        
        # Convert user preferences to dictionary
        user_prefs = user_preference.to_dict()
        
        # Generate recommendations
        recommendations = recommendation_service.generate_recommendations(
            property_data, user_prefs, top_n
        )
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get recommendations"
        )

@router.get("/properties", response_model=List[Dict[str, Any]])
async def get_properties(
    skip: int = 0,
    limit: int = 100,
    location: str = None,
    min_bedrooms: int = None,
    max_price: float = None,
    db: Session = Depends(get_db)
):
    """
    Get list of properties with optional filtering
    
    Args:
        skip: Number of properties to skip
        limit: Maximum number of properties to return
        location: Filter by location
        min_bedrooms: Minimum number of bedrooms
        max_price: Maximum price
    """
    try:
        query = db.query(Property)
        
        # Apply filters
        if location:
            query = query.filter(Property.location.ilike(f"%{location}%"))
        if min_bedrooms:
            query = query.filter(Property.bedrooms >= min_bedrooms)
        if max_price:
            query = query.filter(Property.price <= max_price)
        
        # Apply pagination
        properties = query.offset(skip).limit(limit).all()
        
        return [prop.to_dict() for prop in properties]
        
    except Exception as e:
        logger.error(f"Error getting properties: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get properties"
        )

@router.get("/properties/{property_id}", response_model=Dict[str, Any])
async def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific property
    
    Args:
        property_id: Property identifier
    """
    try:
        property = db.query(Property).filter(Property.id == property_id).first()
        
        if not property:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Property not found"
            )
        
        return property.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting property {property_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get property"
        )

@router.post("/ml/predict-price", response_model=Dict[str, Any])
async def predict_price(
    property_features: Dict[str, Any]
):
    """
    Predict property price using ML model
    
    Expected payload:
    {
        "bedrooms": 3,
        "bathrooms": 2,
        "size_sqft": 1500,
        "year_built": 2020,
        "location": "New York, NY",
        "amenities": ["Gym", "Pool"]
    }
    """
    try:
        predicted_price = ml_service.predict_price(property_features)
        
        if predicted_price is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to predict price"
            )
        
        return {
            "predicted_price": predicted_price,
            "features": property_features
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting price: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to predict price"
        )

@router.get("/ml/model-info", response_model=Dict[str, Any])
async def get_model_info():
    """Get information about the loaded ML model"""
    try:
        model_info = ml_service.get_model_info()
        return model_info
        
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get model information"
        )
