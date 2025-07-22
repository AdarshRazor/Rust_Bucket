from .model_service import ModelService
import numpy as np

def predict_price(property_dict):
    model = ModelService.get_model()
    # Try to get feature names from the model
    if hasattr(model, 'feature_names_in_'):
        feature_names = model.feature_names_in_
    elif hasattr(model, 'feature_names'):
        feature_names = model.feature_names
    else:
        raise ValueError('Model does not provide feature names.')
    # Extract features in the correct order
    features = []
    for name in feature_names:
        value = property_dict.get(name)
        if value is None:
            # Handle missing features (could use default, mean, or raise error)
            value = 0
        features.append(value)
    X = np.array([features])
    # Predict price
    predicted = model.predict(X)
    return float(predicted[0]) 