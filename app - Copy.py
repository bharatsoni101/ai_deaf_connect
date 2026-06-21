import cv2
import streamlit as st
import mediapipe as mp
from services.text_to_speech import speak_text
import time

# -------------------------------
# STREAMLIT UI CONFIGURATION
# -------------------------------

# Set page title and layout
st.set_page_config(
    page_title="Hand Gesture Word Identifier",
    layout="centered"
)

st.title("🖐️ 10-Word Hand Gesture Identifier")

st.text("This app uses your webcam and detects hand gestures using MediaPipe.")

# -------------------------------
# MEDIA PIPE INITIALIZATION
# -------------------------------

# MediaPipe solution for hand tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Create hand detection model
# max_num_hands=1 → only detect one hand at a time
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -------------------------------
# STREAMLIT CONTROLS
# -------------------------------

# Checkbox to start/stop webcam
run = st.checkbox('Start Webcam Feed')

# Placeholder where video frames will be shown
FRAME_WINDOW = st.image([])

# Open webcam (0 = default camera)
camera = cv2.VideoCapture(0)

# -------------------------------
# FUNCTION: DETECT GESTURE
# -------------------------------

def evaluate_gesture(landmarks):
    """
    This function converts hand landmarks into finger states
    and maps them to a word.

    Input:
        landmarks → 21 hand points from MediaPipe

    Output:
        String word (ZERO, ONE, TWO, etc.)
    """

    # Finger tip IDs in MediaPipe model
    # Thumb = 4, Index = 8, Middle = 12, Ring = 16, Little = 20
    tip_ids = [4, 8, 12, 16, 20]

    # Store finger states (1 = open, 0 = closed)
    fingers = []

    # -------------------------------
    # THUMB CHECK (horizontal movement)
    # -------------------------------
    # Thumb behaves differently than other fingers
    # So we compare X-axis positions
    if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x:
        fingers.append(1)  # Thumb is open
    else:
        fingers.append(0)  # Thumb is closed

    # -------------------------------
    # OTHER 4 FINGERS CHECK (vertical movement)
    # -------------------------------
    # We compare Y-axis values for finger open/close
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:
            fingers.append(1)  # Finger is open
        else:
            fingers.append(0)  # Finger is closed

    # -------------------------------
    # MAP FINGER PATTERN TO WORDS
    # -------------------------------

    if fingers == [0, 0, 0, 0, 0]:
        return "ZERO"

    elif fingers == [0, 1, 0, 0, 0]:
        return "ONE"

    elif fingers == [0, 1, 1, 0, 0]:
        return "TWO"

    elif fingers == [0, 1, 1, 1, 0]:
        return "THREE"

    elif fingers == [0, 1, 1, 1, 1]:
        return "FOUR"

    elif fingers == [1, 1, 1, 1, 1]:
        return "FIVE"

    elif fingers == [1, 0, 0, 0, 1]:
        return "ROCK"

    elif fingers == [1, 1, 0, 0, 1]:
        return "SPIDERMAN"

    elif fingers == [1, 0, 1, 1, 1]:
        return "OK"

    elif fingers == [1, 1, 1, 0, 0]:
        return "SIX"

    else:
        return "UNRECOGNIZED"

# -------------------------------
# MAIN VIDEO LOOP
# -------------------------------
if "last_spoken_word" not in st.session_state:
    st.session_state.last_spoken_word = ""

while run:

    # Read frame from webcam
    success, frame = camera.read()

    # If camera fails
    if not success:
        st.warning("Webcam not accessed or unavailable.")
        break

    # Flip frame horizontally (mirror view)
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame to detect hands
    results = hands.process(rgb_frame)

    # Default text if no hand is detected
    word_detected = "No Hand Detected"

    # If hand is found in frame
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand skeleton on screen
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Convert landmarks into a word
            word_detected = evaluate_gesture(hand_landmarks.landmark)

            # inside loop after word_detected:
            if word_detected != st.session_state.last_spoken_word:
                speak_text(word_detected)
                st.session_state.last_spoken_word = word_detected

    # -------------------------------
    # DISPLAY OUTPUT ON SCREEN
    # -------------------------------

    # Write detected word on frame
    cv2.putText(
        frame,
        f"WORD: {word_detected}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )

    # Convert back to RGB for Streamlit display
    output_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Show frame in Streamlit UI
    FRAME_WINDOW.image(output_frame)

# -------------------------------
# CLEANUP WHEN STOPPED
# -------------------------------

else:
    camera.release()
    st.info("Webcam stopped.")