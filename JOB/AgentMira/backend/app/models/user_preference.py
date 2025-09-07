"""
User preference database model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ARRAY
from sqlalchemy.sql import func
from app.core.database import Base

class UserPreference(Base):
    """User preference model for storing user search preferences"""
    
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    budget = Column(Float, nullable=False)
    location = Column(String(255))
    min_bedrooms = Column(Integer)
    max_commute_time = Column(Integer)
    min_school_rating = Column(Float)
    preferred_amenities = Column(ARRAY(String), default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<UserPreference(id={self.id}, session_id='{self.session_id}', budget={self.budget})>"
    
    def to_dict(self):
        """Convert user preference to dictionary"""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "budget": self.budget,
            "location": self.location,
            "min_bedrooms": self.min_bedrooms,
            "max_commute_time": self.max_commute_time,
            "min_school_rating": self.min_school_rating,
            "preferred_amenities": self.preferred_amenities or [],
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
