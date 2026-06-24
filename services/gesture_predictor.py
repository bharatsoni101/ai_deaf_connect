"""
=========================================================
Hand Gesture Prediction Service
=========================================================

Purpose:
--------
This module loads the trained Machine Learning model
(Random Forest) and predicts the hand gesture from
MediaPipe landmarks.

Input:
------
MediaPipe hand landmarks (21 landmarks)

Output:
-------
Predicted gesture label
Prediction confidence

Author:
-------
Bharat Soni
"""

import os
import joblib
import numpy as np


class GesturePredictor:
    """
    Loads the trained gesture recognition model and
    predicts hand gestures from MediaPipe landmarks.
    """

    def __init__(self, model_path="models/gesture_AtoZ_model.pkl"):
        """
        Load the trained model once during initialization.
        """

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}\n"
                "Please train the model first using training/train_model.py"
            )

        self.model = joblib.load(model_path)

        print("===================================")
        print(" Gesture Prediction Service Ready ")
        print("===================================")
        print(f"Model Loaded : {model_path}")

    # ----------------------------------------------------
    # Convert MediaPipe landmarks into feature vector
    # ----------------------------------------------------
    def extract_features(self, landmarks):
        """
        Convert MediaPipe landmarks into a feature vector.

        Parameters
        ----------
        landmarks : list
            MediaPipe landmarks (21 landmarks)

        Returns
        -------
        numpy.ndarray
            Shape = (1, 63)
        """

        features = []

        for landmark in landmarks:
            features.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        return np.array(features).reshape(1, -1)

    # ----------------------------------------------------
    # Predict Gesture
    # ----------------------------------------------------
    def predict(self, landmarks):
        """
        Predict gesture and confidence score.

        Parameters
        ----------
        landmarks : list
            MediaPipe landmarks

        Returns
        -------
        tuple
            (gesture_name, confidence)
        """

        try:

            features = self.extract_features(landmarks)

            # Predict gesture
            prediction = self.model.predict(features)[0]

            # Predict confidence
            probability = self.model.predict_proba(features)

            confidence = np.max(probability) * 100

            return prediction, confidence

        except Exception as error:

            print(f"Prediction Error : {error}")

            return "UNRECOGNIZED", 0.0