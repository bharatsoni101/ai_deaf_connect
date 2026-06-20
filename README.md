# 🖐️ Hand Gesture Word Identifier

A Streamlit-based application that uses MediaPipe and OpenCV to detect hand gestures from a webcam feed and identify simple words based on finger positions.

This project recognizes 10 predefined gestures and displays the detected word in real time.

---

## Features

* Real-time webcam processing
* Hand tracking using MediaPipe
* Finger state detection (open/closed)
* Recognizes 10 predefined words
* Simple Streamlit user interface
* Runs completely on a local machine

---

## Technologies Used

* Python 3.11
* Streamlit
* OpenCV
* MediaPipe
* NumPy

---

## Project Structure

```text
project_folder/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Requirements

Create a `requirements.txt` file containing:

```text
streamlit==1.54.0
opencv-python==4.12.0.88
mediapipe==0.10.21
numpy==2.2.6
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository_url>

cd <repository_name>
```

### 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate environment

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

or

```bash
uv pip install -r requirements.txt
```

---

## Run the application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

Usually:

```text
http://localhost:8501
```

---

## How It Works

1. The webcam captures live video frames.
2. MediaPipe detects hand landmarks.
3. Finger positions are analyzed.
4. The application determines which fingers are open or closed.
5. A predefined gesture is mapped to a word.
6. The detected word is displayed on the screen.

---

## Supported Gestures

| Finger Pattern | Detected Word |
| -------------- | ------------- |
| 00000          | ZERO          |
| 01000          | ONE           |
| 01100          | TWO           |
| 01110          | THREE         |
| 01111          | FOUR          |
| 11111          | FIVE          |
| 10001          | ROCK          |
| 11001          | SPIDERMAN     |
| 10111          | OK            |
| 11100          | SIX           |

Where:

* 1 = Finger Open
* 0 = Finger Closed

Finger order:

```text
Thumb
Index
Middle
Ring
Little
```

---

## Controls

### Start Webcam Feed

Check the box to start webcam detection.

### Stop Webcam Feed

Uncheck the box to stop webcam detection.

---

## Troubleshooting

### Webcam not accessed or unavailable

Possible reasons:

* Another application is using the webcam.
* Camera permissions are disabled.
* Webcam drivers are not installed.
* Incorrect camera index is selected.

Enable Windows camera permissions:

```text
Settings
→ Privacy & Security
→ Camera

Enable:

✓ Camera access

✓ Let apps access your camera

✓ Let desktop apps access your camera
```

Close applications that may use the webcam:

* Zoom
* Microsoft Teams
* Google Meet
* WhatsApp Desktop
* OBS Studio

---

## Limitations

This application uses simple finger-count logic.

It is not a complete sign language recognition system.

The following are not supported:

* Dynamic gestures
* Sentence formation
* Full sign language vocabulary
* Multi-hand conversations

---

## Future Enhancements

* Support 200+ sign language words
* AI-based gesture recognition
* Sentence generation
* Text-to-Speech conversion
* Speech-to-Text conversion
* Two-person video conferencing
* Integration with AI Deaf Connect

---

## Author

Bharat Soni

AI and Python enthusiast working on AI-based accessibility applications.

---

## License

This project is for educational and learning purposes.
