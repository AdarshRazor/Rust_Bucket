from typing import Dict

def calculate_total_score(property_dict: Dict, user_prefs: Dict, predicted_price: float) -> Dict:
    # Weights for each component (adjust as needed)
    WEIGHTS = {
        'price': 0.4,
        'bedrooms': 0.2,
        'commute': 0.15,
        'school': 0.15,
        'amenities': 0.1,
    }
    # Price match: higher score if listing price <= user budget and close to predicted price
    price_score = 0
    if property_dict['price'] <= user_prefs['budget']:
        diff = abs(property_dict['price'] - predicted_price)
        price_score = max(0, 1 - diff / max(predicted_price, 1))  # normalized
    # Bedroom match: 1 if meets/exceeds, else partial
    bedrooms_score = min(1, property_dict['bedrooms'] / user_prefs['min_bedrooms']) if user_prefs['min_bedrooms'] else 1
    # Commute: 1 if within limit, else partial
    commute_score = 0
    if 'commute_time' in property_dict and 'max_commute' in user_prefs:
        commute_score = max(0, 1 - (property_dict['commute_time'] - user_prefs['max_commute']) / 60) if property_dict['commute_time'] <= user_prefs['max_commute'] else 0
    # School: normalized to 0-1
    school_score = property_dict.get('school_rating', 0) / 10
    # Amenities: fraction of desired amenities present
    desired_amenities = user_prefs.get('amenities', [])
    if desired_amenities:
        matched = sum(1 for amenity in desired_amenities if property_dict.get(f'has_{amenity.lower()}', False))
        amenities_score = matched / len(desired_amenities)
    else:
        amenities_score = 1
    # Weighted total
    total_score = (
        WEIGHTS['price'] * price_score +
        WEIGHTS['bedrooms'] * bedrooms_score +
        WEIGHTS['commute'] * commute_score +
        WEIGHTS['school'] * school_score +
        WEIGHTS['amenities'] * amenities_score
    )
    # Return breakdown for reasoning
    return {
        'total_match_score': round(total_score * 100, 2),
        'component_scores': {
            'price': round(price_score * 100, 1),
            'bedrooms': round(bedrooms_score * 100, 1),
            'commute': round(commute_score * 100, 1),
            'school': round(school_score * 100, 1),
            'amenities': round(amenities_score * 100, 1),
        }
    } 