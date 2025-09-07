"""
Data seeding script for Agent Mira Property Recommendation System
Populates the database with sample property data from the case study
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine, Base
from app.models.property import Property
import json

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_case_study_data():
    """Load data from case study JSON files"""
    
    # Property basic info (from Case Study 3 JSON 1)
    basic_properties = [
        {"id": 1, "title": "3 BHK Apartment in Downtown", "price": 450000, "location": "New York, NY"},
        {"id": 2, "title": "2 BHK Condo with Sea View", "price": 380000, "location": "Miami, FL"},
        {"id": 3, "title": "Luxury Villa with Private Garden", "price": 850000, "location": "Los Angeles, CA"},
        {"id": 4, "title": "1 BHK Budget Apartment", "price": 250000, "location": "Austin, TX"},
        {"id": 5, "title": "Penthouse with Skyline View", "price": 1200000, "location": "San Francisco, CA"},
        {"id": 6, "title": "Cozy Studio in Central Park", "price": 300000, "location": "New York, NY"},
        {"id": 7, "title": "Lakefront House with Dock", "price": 750000, "location": "Chicago, IL"},
        {"id": 8, "title": "Modern Townhouse with Backyard", "price": 600000, "location": "Dallas, TX"},
        {"id": 9, "title": "4 BHK Duplex with Home Office", "price": 920000, "location": "Seattle, WA"},
        {"id": 10, "title": "Minimalist Smart Home", "price": 700000, "location": "Boston, MA"}
    ]
    
    # Property details (from Case Study 3 JSON 2)
    property_details = [
        {"id": 1, "bedrooms": 3, "bathrooms": 2, "size_sqft": 1500, "amenities": ["Gym", "Swimming Pool", "Parking"]},
        {"id": 2, "bedrooms": 2, "bathrooms": 2, "size_sqft": 1200, "amenities": ["Beach Access", "Security", "Balcony"]},
        {"id": 3, "bedrooms": 4, "bathrooms": 3, "size_sqft": 2800, "amenities": ["Private Garden", "Smart Home", "Garage"]},
        {"id": 4, "bedrooms": 1, "bathrooms": 1, "size_sqft": 800, "amenities": ["Gym", "Laundry", "Security"]},
        {"id": 5, "bedrooms": 5, "bathrooms": 4, "size_sqft": 3500, "amenities": ["Rooftop Terrace", "Smart Security", "Private Elevator"]},
        {"id": 6, "bedrooms": 1, "bathrooms": 1, "size_sqft": 600, "amenities": ["Park View", "24/7 Concierge", "Fitness Center"]},
        {"id": 7, "bedrooms": 3, "bathrooms": 2, "size_sqft": 2000, "amenities": ["Private Dock", "Boat Parking", "BBQ Area"]},
        {"id": 8, "bedrooms": 3, "bathrooms": 3, "size_sqft": 1800, "amenities": ["Backyard", "Community Pool", "Pet Friendly"]},
        {"id": 9, "bedrooms": 4, "bathrooms": 3, "size_sqft": 2500, "amenities": ["Home Office", "Solar Panels", "Two-Car Garage"]},
        {"id": 10, "bedrooms": 3, "bathrooms": 2, "size_sqft": 1900, "amenities": ["Minimalist Design", "Smart Appliances", "Energy Efficient"]}
    ]
    
    # Property images (from Case Study 3 JSON 3)
    property_images = [
        {"id": 1, "image_url": "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg"},
        {"id": 2, "image_url": "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg"},
        {"id": 3, "image_url": "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg"},
        {"id": 4, "image_url": "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg"},
        {"id": 5, "image_url": "https://images.pexels.com/photos/534151/pexels-photo-534151.jpeg"},
        {"id": 6, "image_url": "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg"},
        {"id": 7, "image_url": "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg"},
        {"id": 8, "image_url": "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg"},
        {"id": 9, "image_url": "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg"},
        {"id": 10, "image_url": "https://images.pexels.com/photos/534151/pexels-photo-534151.jpeg"}
    ]
    
    return basic_properties, property_details, property_images

def create_sample_properties():
    """Create sample properties with additional realistic data"""
    
    basic_properties, property_details, property_images = load_case_study_data()
    
    # Additional realistic data for scoring
    additional_data = {
        1: {"year_built": 2018, "school_rating": 8.5, "commute_time": 20},
        2: {"year_built": 2020, "school_rating": 7.8, "commute_time": 25},
        3: {"year_built": 2015, "school_rating": 9.2, "commute_time": 35},
        4: {"year_built": 2022, "school_rating": 6.5, "commute_time": 15},
        5: {"year_built": 2019, "school_rating": 9.8, "commute_time": 30},
        6: {"year_built": 2021, "school_rating": 8.0, "commute_time": 10},
        7: {"year_built": 2012, "school_rating": 7.5, "commute_time": 40},
        8: {"year_built": 2017, "school_rating": 8.2, "commute_time": 22},
        9: {"year_built": 2016, "school_rating": 8.8, "commute_time": 28},
        10: {"year_built": 2023, "school_rating": 7.0, "commute_time": 18}
    }
    
    properties = []
    
    for basic, details, images in zip(basic_properties, property_details, property_images):
        # Get additional data
        extra = additional_data.get(basic["id"], {})
        
        property_obj = Property(
            id=basic["id"],
            title=basic["title"],
            price=basic["price"],
            location=basic["location"],
            bedrooms=details["bedrooms"],
            bathrooms=details["bathrooms"],
            size_sqft=details["size_sqft"],
            year_built=extra.get("year_built"),
            amenities=details["amenities"],
            image_urls=[images["image_url"]],
            school_rating=extra.get("school_rating"),
            commute_time=extra.get("commute_time")
        )
        
        properties.append(property_obj)
    
    return properties

def seed_database():
    """Seed the database with sample data"""
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Creating sample properties...")
    properties = create_sample_properties()
    
    print("Inserting data into database...")
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Property).delete()
        db.commit()
        
        # Insert new data
        for property_obj in properties:
            db.add(property_obj)
        
        db.commit()
        print(f"Successfully inserted {len(properties)} properties")
        
        # Verify data
        count = db.query(Property).count()
        print(f"Database now contains {count} properties")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeding...")
    seed_database()
    print("Database seeding completed!")
