# Stub for unpickling the model. Replace with the real class if available.
class ComplexTrapModelRenamed:
    def predict(self, X):
        # Return a list of fake prices (e.g., 100000 for each input row)
        return [100000] * len(X)

import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../docs/complex_price_model_v2.pkl')

class ModelService:
    _model = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            with open(MODEL_PATH, 'rb') as f:
                import sys
                sys.modules['__main__'].ComplexTrapModelRenamed = ComplexTrapModelRenamed
                cls._model = pickle.load(f)
        return cls._model

    @classmethod
    def get_model(cls):
        if cls._model is None:
            return cls.load_model()
        return cls._model 