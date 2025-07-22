import pytest
from server.score import calculate_total_score

def test_calculate_total_score_basic():
    property_dict = {
        'price': 400000,
        'bedrooms': 3,
        'commute_time': 20,
        'school_rating': 8,
        'has_pool': True,
        'has_garage': False,
        'has_garden': True,
    }
    user_prefs = {
        'budget': 500000,
        'min_bedrooms': 3,
        'max_commute': 30,
        'school_rating': 7,
        'amenities': ['Pool', 'Garden'],
    }
    predicted_price = 410000
    result = calculate_total_score(property_dict, user_prefs, predicted_price)
    assert 'total_match_score' in result
    assert 'component_scores' in result
    assert result['total_match_score'] > 0 