import cv2
import streamlit as st
import mediapipe as mp

from services.gesture_predictor import GesturePredictor
from services.text_to_speech import speak_text


# ==========================================================
# STREAMLIT PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Hand Gesture Recognition",
    layout="centered"
)

st.title("🖐️ AI Hand Gesture Recognition")
st.write("Detects hand gestures using MediaPipe + Machine Learning.")

# ==========================================================
# INITIALIZE MACHINE LEARNING MODEL
# ==========================================================

# Load the trained Random Forest model only once
predictor = GesturePredictor()

# ==========================================================
# INITIALIZE MEDIAPIPE
# ==========================================================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ==========================================================
# STREAMLIT CONTROLS
# ==========================================================

run = st.checkbox("Start Webcam Feed")

FRAME_WINDOW = st.image([])

camera = cv2.VideoCapture(0)

# ==========================================================
# SESSION STATE
# ==========================================================

if "last_spoken_word" not in st.session_state:
    st.session_state.last_spoken_word = ""

# ==========================================================
# MAIN LOOP
# ==========================================================

while run:

    success, frame = camera.read()

    if not success:
        st.warning("Unable to access webcam.")
        break

    # Mirror image
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    # Default text if no hand is detected
    word_detected = "No Hand Detected"
    confidence = 0.0

    # ------------------------------------------------------
    # Hand Detected
    # ------------------------------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # -------------------------------
            # ML Prediction
            # -------------------------------

            word_detected, confidence = predictor.predict(
                hand_landmarks.landmark
            )

            # Speak only when gesture changes
            if (
                word_detected != st.session_state.last_spoken_word
                and word_detected not in ["UNRECOGNIZED", "No Hand Detected"]
            ):

                speak_text(word_detected)

                st.session_state.last_spoken_word = word_detected

    # ======================================================
    # DRAW TEXT ON FRAME
    # ======================================================

    cv2.putText(
        frame,
        f"Gesture : {word_detected}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Confidence : {confidence:.2f}%",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # Convert frame back to RGB
    output_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Show frame
    FRAME_WINDOW.image(output_frame)

# ==========================================================
# CLEANUP
# ==========================================================

else:

    camera.release()

    st.info("Webcam stopped.")