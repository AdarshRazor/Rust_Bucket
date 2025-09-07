"""
Recommendation Engine Service
Implements the multi-factor scoring algorithm for property recommendations
"""

from typing import List, Dict, Any, Tuple
import logging
from app.services.ml_service import ml_service

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service for generating property recommendations"""
    
    def __init__(self):
        self.weights = {
            'price_match': 0.3,
            'bedroom': 0.2,
            'school_rating': 0.15,
            'commute': 0.15,
            'property_age': 0.1,
            'amenities': 0.1
        }
    
    def calculate_price_match_score(self, predicted_price: float, user_budget: float) -> float:
        """
        Calculate price match score (0-100)
        
        Args:
            predicted_price: ML predicted price
            user_budget: User's budget limit
            
        Returns:
            Score between 0-100
        """
        if predicted_price <= user_budget:
            return 100.0
        else:
            # Penalty for exceeding budget
            penalty = ((predicted_price - user_budget) / user_budget) * 100
            return max(0.0, 100.0 - penalty)
    
    def calculate_bedroom_score(self, property_bedrooms: int, user_min_bedrooms: int) -> float:
        """
        Calculate bedroom score (0-100)
        
        Args:
            property_bedrooms: Number of bedrooms in property
            user_min_bedrooms: User's minimum bedroom requirement
            
        Returns:
            Score between 0-100
        """
        if property_bedrooms >= user_min_bedrooms:
            return 100.0
        else:
            return (property_bedrooms / user_min_bedrooms) * 100.0
    
    def calculate_school_rating_score(self, school_rating: float) -> float:
        """
        Calculate school rating score (0-100)
        
        Args:
            school_rating: School rating (0-10 scale)
            
        Returns:
            Score between 0-100
        """
        if school_rating is None:
            return 50.0  # Neutral score for missing data
        return (school_rating / 10.0) * 100.0
    
    def calculate_commute_score(self, commute_time: int) -> float:
        """
        Calculate commute score (0-100)
        
        Args:
            commute_time: Commute time in minutes
            
        Returns:
            Score between 0-100
        """
        if commute_time is None:
            return 50.0  # Neutral score for missing data
        
        if commute_time <= 15:
            return 100.0
        elif commute_time <= 30:
            return 80.0
        elif commute_time <= 45:
            return 50.0
        else:
            return 20.0
    
    def calculate_property_age_score(self, year_built: int) -> float:
        """
        Calculate property age score (0-100)
        
        Args:
            year_built: Year the property was built
            
        Returns:
            Score between 0-100
        """
        if year_built is None:
            return 50.0  # Neutral score for missing data
        
        current_year = 2024  # Could be made dynamic
        age = current_year - year_built
        
        if age <= 5:
            return 100.0
        elif age <= 15:
            return 80.0
        elif age <= 30:
            return 60.0
        else:
            return 40.0
    
    def calculate_amenities_score(self, property_amenities: List[str], user_preferred_amenities: List[str]) -> float:
        """
        Calculate amenities score (0-100)
        
        Args:
            property_amenities: List of property amenities
            user_preferred_amenities: List of user's preferred amenities
            
        Returns:
            Score between 0-100
        """
        if not property_amenities:
            return 50.0  # Neutral score for missing data
        
        if not user_preferred_amenities:
            # If no user preferences, score based on total amenities
            return min(100.0, len(property_amenities) * 20.0)
        
        # Calculate match ratio
        matches = sum(1 for amenity in user_preferred_amenities if amenity in property_amenities)
        match_ratio = matches / len(user_preferred_amenities)
        
        return match_ratio * 100.0
    
    def calculate_total_score(self, property_data: Dict[str, Any], user_preferences: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Calculate total recommendation score for a property
        
        Args:
            property_data: Property information
            user_preferences: User preference data
            
        Returns:
            Tuple of (total_score, component_scores)
        """
        # Get predicted price
        predicted_price = ml_service.predict_price(property_data)
        if predicted_price is None:
            predicted_price = property_data.get('price', 0)  # Fallback to listed price
        
        # Calculate component scores
        component_scores = {
            'price_match': self.calculate_price_match_score(
                predicted_price, 
                user_preferences.get('budget', 0)
            ),
            'bedroom': self.calculate_bedroom_score(
                property_data.get('bedrooms', 0),
                user_preferences.get('min_bedrooms', 1)
            ),
            'school_rating': self.calculate_school_rating_score(
                property_data.get('school_rating')
            ),
            'commute': self.calculate_commute_score(
                property_data.get('commute_time')
            ),
            'property_age': self.calculate_property_age_score(
                property_data.get('year_built')
            ),
            'amenities': self.calculate_amenities_score(
                property_data.get('amenities', []),
                user_preferences.get('preferred_amenities', [])
            )
        }
        
        # Calculate weighted total score
        total_score = sum(
            component_scores[component] * weight
            for component, weight in self.weights.items()
        )
        
        return total_score, component_scores
    
    def generate_recommendations(self, properties: List[Dict[str, Any]], user_preferences: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Generate top N property recommendations
        
        Args:
            properties: List of available properties
            user_preferences: User preference data
            top_n: Number of top recommendations to return
            
        Returns:
            List of recommended properties with scores and reasoning
        """
        scored_properties = []
        
        for property_data in properties:
            try:
                total_score, component_scores = self.calculate_total_score(property_data, user_preferences)
                
                # Add recommendation data
                recommendation = {
                    'property': property_data,
                    'total_score': round(total_score, 2),
                    'component_scores': {k: round(v, 2) for k, v in component_scores.items()},
                    'reasoning': self._generate_reasoning(property_data, component_scores, user_preferences)
                }
                
                scored_properties.append(recommendation)
                
            except Exception as e:
                logger.error(f"Error scoring property {property_data.get('id', 'unknown')}: {str(e)}")
                continue
        
        # Sort by total score (descending) and return top N
        scored_properties.sort(key=lambda x: x['total_score'], reverse=True)
        return scored_properties[:top_n]
    
    def _generate_reasoning(self, property_data: Dict[str, Any], component_scores: Dict[str, float], user_preferences: Dict[str, Any]) -> str:
        """
        Generate human-readable reasoning for the recommendation
        
        Args:
            property_data: Property information
            component_scores: Individual component scores
            user_preferences: User preference data
            
        Returns:
            Reasoning string
        """
        reasoning_parts = []
        
        # Price reasoning
        if component_scores['price_match'] >= 90:
            reasoning_parts.append("Excellent price match within your budget")
        elif component_scores['price_match'] >= 70:
            reasoning_parts.append("Good price match with minor budget considerations")
        else:
            reasoning_parts.append("Price exceeds budget but offers good value")
        
        # Bedroom reasoning
        if component_scores['bedroom'] == 100:
            reasoning_parts.append(f"Meets your {user_preferences.get('min_bedrooms', 1)}+ bedroom requirement")
        elif component_scores['bedroom'] >= 70:
            reasoning_parts.append("Close to your bedroom requirements")
        
        # School rating reasoning
        if component_scores['school_rating'] >= 80:
            reasoning_parts.append("Excellent school district")
        elif component_scores['school_rating'] >= 60:
            reasoning_parts.append("Good school district")
        
        # Commute reasoning
        if component_scores['commute'] >= 80:
            reasoning_parts.append("Short commute to city center")
        elif component_scores['commute'] >= 50:
            reasoning_parts.append("Reasonable commute time")
        
        # Property age reasoning
        if component_scores['property_age'] >= 80:
            reasoning_parts.append("Modern construction")
        elif component_scores['property_age'] >= 60:
            reasoning_parts.append("Well-maintained property")
        
        # Amenities reasoning
        if component_scores['amenities'] >= 80:
            reasoning_parts.append("Includes most of your preferred amenities")
        elif component_scores['amenities'] >= 50:
            reasoning_parts.append("Good amenity selection")
        
        return ". ".join(reasoning_parts) + "."

# Global recommendation service instance
recommendation_service = RecommendationService()
