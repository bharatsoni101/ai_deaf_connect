# 🖐️ Hand Gesture Word Identifier with Text-to-Speech

A Streamlit-based application that uses **MediaPipe**, **OpenCV**, and **Google Text-to-Speech (gTTS)** to detect hand gestures from a webcam feed, convert them into predefined words, and automatically speak the detected words.

This project currently recognizes **10 predefined hand gestures** and provides **real-time visual and audio feedback**.

---

# 📌 Features

* 🎥 Real-time webcam processing
* 🖐️ Hand tracking using MediaPipe
* ✋ Finger state detection (Open / Closed)
* 🔤 Recognizes 10 predefined words
* 🔊 Automatic Text-to-Speech conversion
* 🖥️ Simple Streamlit user interface
* ⚡ Runs completely on a local machine
* 🧩 Beginner-friendly project structure

---

# 🛠️ Technologies Used

* Python 3.11
* Streamlit
* OpenCV
* MediaPipe
* NumPy
* Google Text-to-Speech (gTTS)

---

# 📁 Project Structure

```text
project_folder/
│
├── app.py
├── text_to_speech.py
├── requirements.txt
└── README.md
```

---

# 📦 Requirements

Create a `requirements.txt` file with the following content:

```text
streamlit==1.54.0
mediapipe==0.10.21
numpy==1.26.4
opencv-python==4.9.0.80
gTTS==2.5.3
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone <repository_url>

cd <repository_name>
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

Using pip:

```bash
pip install -r requirements.txt
```

or using uv:

```bash
uv pip install -r requirements.txt
```

---

# 🚀 Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

Default URL:

```text
http://localhost:8501
```

---

# 🧠 How It Works

1. The webcam captures live video frames.
2. MediaPipe detects the hand and its 21 landmarks.
3. Finger positions are analyzed.
4. Each finger is marked as Open (1) or Closed (0).
5. The finger pattern is mapped to a predefined word.
6. The detected word is displayed on the screen.
7. The detected word is automatically converted into speech.

---

# 🖐️ Supported Gestures

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

---

## Finger Order

```text
Thumb
Index
Middle
Ring
Little
```

Where:

```text
1 = Finger Open
0 = Finger Closed
```

Example:

```text
01100

Thumb  = Closed
Index  = Open
Middle = Open
Ring   = Closed
Little = Closed

Result = TWO
```

---

# 🎮 Application Controls

## Start Webcam Feed

Enable the checkbox to start hand detection.

## Stop Webcam Feed

Disable the checkbox to stop webcam detection.

---

# 🔊 Text-to-Speech

The application automatically converts detected words into speech.

Examples:

```text
ONE
TWO
THREE
FOUR
FIVE
ROCK
SPIDERMAN
OK
```

The following values are ignored:

```text
UNRECOGNIZED
No Hand Detected
```

---

# ⚠️ Troubleshooting

## Webcam not accessed or unavailable

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

Close applications that may be using the webcam:

* Zoom
* Microsoft Teams
* Google Meet
* WhatsApp Desktop
* OBS Studio
* Skype

---

# ⚠️ Current Limitations

This application uses simple finger-count logic.

It is **not a complete sign language recognition system**.

Currently, it does not support:

* Dynamic gestures
* Sentence formation
* Continuous sign language recognition
* Full sign language vocabulary
* Two-person communication
* Multi-hand detection

---

# 🚀 Future Enhancements

Planned improvements:

* 🤖 AI-based gesture recognition
* 📚 Support for 200+ sign language words
* 📝 Sentence generation
* 🗣️ Speech-to-Text conversion
* 🔊 Improved Text-to-Speech
* 🎥 Two-person video conferencing
* 🌐 Real-time communication system
* ♿ Integration with AI Deaf Connect

---

# 👨‍💻 Author

Bharat Soni

Techno-managerial professional and AI enthusiast working on AI-powered accessibility applications.

---

# 📄 License

This project is intended for educational, learning, and research purposes.
