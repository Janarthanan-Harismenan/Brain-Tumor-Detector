# import tensorflow as tf
# import numpy as np

# class TumorDetectionRepository:
#     def __init__(self, model_path: str):
#         self.model = tf.keras.models.load_model(model_path)

#     def predict(self, image: np.ndarray) -> float:
#         prediction = self.model.predict(image)[0][0]  # Extract single prediction value
#         return float(prediction)  # Convert NumPy type to Python float

import tensorflow as tf
import numpy as np

class TumorDetectionRepository:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, image: np.ndarray) -> float:
        prediction = self.model.predict(image)[0][0]
        return float(prediction)
