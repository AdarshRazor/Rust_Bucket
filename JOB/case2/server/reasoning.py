def generate_reasoning(property_dict, scores, user_prefs):
    lines = []
    lines.append(f"**Overall Match: {scores['total_match_score']}/100**")
    cs = scores['component_scores']
    # Price
    if cs['price'] >= 80:
        lines.append("✅ **Excellent Price:** Our model predicts a value near the listing price, and it's within your budget.")
    elif cs['price'] >= 50:
        lines.append("⚠️ **Good Price:** The price is reasonable compared to the predicted value and your budget.")
    else:
        lines.append("❌ **Price Mismatch:** The price is above your budget or far from predicted value.")
    # Bedrooms
    if cs['bedrooms'] >= 100:
        lines.append(f"✅ **Meets Bedroom Needs:** Has {property_dict['bedrooms']} bedrooms, meeting your minimum requirement.")
    else:
        lines.append(f"⚠️ **Bedrooms:** Has {property_dict['bedrooms']} bedrooms, which is below your minimum.")
    # Commute
    if cs['commute'] >= 80:
        lines.append(f"✅ **Great Commute:** Commute time is {property_dict.get('commute_time', '?')} min, within your limit.")
    elif cs['commute'] > 0:
        lines.append(f"⚠️ **Commute:** Commute time is {property_dict.get('commute_time', '?')} min, slightly above your limit.")
    else:
        lines.append(f"❌ **Commute:** Commute time is {property_dict.get('commute_time', '?')} min, above your limit.")
    # School
    if cs['school'] >= 80:
        lines.append(f"✅ **Great School Rating:** School rating is {property_dict.get('school_rating', '?')}/10.")
    elif cs['school'] > 0:
        lines.append(f"⚠️ **School Rating:** School rating is {property_dict.get('school_rating', '?')}/10.")
    else:
        lines.append(f"❌ **School Rating:** No school rating available.")
    # Amenities
    if cs['amenities'] >= 100:
        lines.append("✅ **All Desired Amenities Present.")
    elif cs['amenities'] > 0:
        lines.append("⚠️ **Some Desired Amenities Present.")
    else:
        lines.append("❌ **No Desired Amenities Present.")
    return lines 