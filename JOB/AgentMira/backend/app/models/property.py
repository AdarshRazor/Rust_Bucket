"""
Property database model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ARRAY
from sqlalchemy.sql import func
from app.core.database import Base

class Property(Base):
    """Property model for storing property information"""
    
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    location = Column(String(255), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    size_sqft = Column(Integer, nullable=False)
    year_built = Column(Integer)
    amenities = Column(ARRAY(String), default=list)
    image_urls = Column(ARRAY(String), default=list)
    school_rating = Column(Float)
    commute_time = Column(Integer)  # Minutes to city center
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Property(id={self.id}, title='{self.title}', price={self.price})>"
    
    def to_dict(self):
        """Convert property to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "location": self.location,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "size_sqft": self.size_sqft,
            "year_built": self.year_built,
            "amenities": self.amenities or [],
            "image_urls": self.image_urls or [],
            "school_rating": self.school_rating,
            "commute_time": self.commute_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
