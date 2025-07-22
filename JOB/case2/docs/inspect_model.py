import pickle

MODEL_PATH = './complex_price_model_v2.pkl'

def main():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print('Model type:', type(model))
    # Try to print input features if possible
    if hasattr(model, 'feature_names_in_'):
        print('Input features:', model.feature_names_in_)
    elif hasattr(model, 'get_booster') and hasattr(model.get_booster(), 'feature_names'):
        print('Input features:', model.get_booster().feature_names)
    elif hasattr(model, 'feature_names'):
        print('Input features:', model.feature_names)
    else:
        print('Input features: Unknown (model type not recognized)')
    # Try to print output format
    if hasattr(model, 'predict'):
        print('Output: model.predict(X) returns predicted price(s)')
    else:
        print('Output: Unknown (no predict method)')

if __name__ == '__main__':
    main() 