# import cv2
# import imutils
# import numpy as np
# from PIL import Image
# from repository import TumorDetectionRepository

# class TumorDetectionService:
#     def __init__(self, model_path: str):
#         self.repository = TumorDetectionRepository(model_path)

#     def crop_brain_contour(self, image: np.ndarray) -> np.ndarray:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (5, 5), 0)
#         thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
#         thresh = cv2.erode(thresh, None, iterations=2)
#         thresh = cv2.dilate(thresh, None, iterations=2)
#         cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         cnts = imutils.grab_contours(cnts)

#         if not cnts:
#             return image

#         c = max(cnts, key=cv2.contourArea)
#         extLeft = tuple(c[c[:, :, 0].argmin()][0])
#         extRight = tuple(c[c[:, :, 0].argmax()][0])
#         extTop = tuple(c[c[:, :, 1].argmin()][0])
#         extBot = tuple(c[c[:, :, 1].argmax()][0])
#         new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]
#         return new_image

#     def preprocess_image(self, image: Image.Image) -> np.ndarray:
#         image = np.array(image)
#         image = self.crop_brain_contour(image)
#         image = cv2.resize(image, (240, 240), interpolation=cv2.INTER_CUBIC)
#         image = image / 255.0
#         return np.expand_dims(image, axis=0)  # Add batch dimension

#     def predict(self, image: Image.Image) -> dict:
#         processed_image = self.preprocess_image(image)
#         probability = self.repository.predict(processed_image)
#         return {
#             "probability": probability,
#             "tumor_detected": bool(probability > 0.5)
#         }

import cv2
import imutils
import numpy as np
from PIL import Image
from repository import TumorDetectionRepository

class TumorDetectionService:
    def __init__(self, model_path: str):
        self.repository = TumorDetectionRepository(model_path)

    def crop_brain_contour(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if not cnts:
            return image

        c = max(cnts, key=cv2.contourArea)
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]
        return new_image

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        image = np.array(image)
        image = self.crop_brain_contour(image)
        image = cv2.resize(image, (240, 240), interpolation=cv2.INTER_CUBIC)
        image = image / 255.0
        return np.expand_dims(image, axis=0)

    def predict(self, image: Image.Image) -> dict:
        processed_image = self.preprocess_image(image)
        probability = self.repository.predict(processed_image)
        return {
            "probability": probability,
            "tumor_detected": bool(probability > 0.5)
        }
