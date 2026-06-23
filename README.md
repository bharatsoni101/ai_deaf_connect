# 🖐️ AI Deaf Connect – Hand Gesture Recognition (Phase 1)

An AI-powered hand gesture recognition application built using **Python**, **MediaPipe**, **OpenCV**, **Scikit-learn**, and **Streamlit**.

The application captures live video from a webcam, detects hand landmarks using MediaPipe, predicts gestures using a trained **Random Forest Machine Learning model**, and converts the detected gesture into speech.

This project is the **Phase 1 Proof of Concept (POC)** for the **AI Deaf Connect** project, whose long-term goal is to enable seamless communication between hearing and hearing-impaired individuals.

---

# 🚀 Features

* ✅ Real-time webcam hand tracking
* ✅ Hand landmark detection using MediaPipe
* ✅ Custom dataset creation (CSV)
* ✅ Machine Learning based gesture recognition
* ✅ Random Forest Classifier
* ✅ Real-time confidence score
* ✅ Automatic Text-to-Speech
* ✅ Dataset visualization using Matplotlib
* ✅ Modular project structure
* ✅ Easy to extend with new gestures

---

# 🧠 Technologies Used

| Technology    | Purpose                     |
| ------------- | --------------------------- |
| Python 3.11   | Programming Language        |
| Streamlit     | Web UI                      |
| OpenCV        | Webcam and Image Processing |
| MediaPipe     | Hand Landmark Detection     |
| Scikit-learn  | Machine Learning            |
| Random Forest | Gesture Classification      |
| NumPy         | Numerical Computation       |
| Pandas        | Dataset Handling            |
| Matplotlib    | Dataset Visualization       |
| gTTS          | Text to Speech              |
| Joblib        | Save and Load ML Model      |

---

# 📁 Project Structure

```text
ai_deaf_connect/

│
├── app.py
├── dataset.csv
├── requirements.txt
├── README.md
│
├── models/
│   └── gesture_model.pkl
│
├── services/
│   ├── gesture_predictor.py
│   └── text_to_speech.py
│
├── training/
│   ├── collect_dataset.py
│   └── train_model.py
│
└── visualization/
    ├── plot_distribution.py
    ├── plot_landmarks.py
    ├── plot_hand_skeleton.py
    ├── plot_multiple_samples.py
    └── plot_pca.py
```

---

# 📊 Dataset

The dataset is generated using MediaPipe hand landmarks.

Each sample contains:

* Gesture Label
* 21 Hand Landmarks
* X Coordinate
* Y Coordinate
* Z Coordinate

Total Features:

```
21 Landmarks × 3 Coordinates = 63 Features
```

Example:

```text
label,x0,y0,z0,x1,y1,z1,...,x20,y20,z20

ONE,...

TWO,...

FIVE,...
```

Approximately **300 samples** were collected for each gesture.

---

# ✋ Supported Gestures

| Gesture   |
| --------- |
| ZERO      |
| ONE       |
| TWO       |
| THREE     |
| FOUR      |
| FIVE      |
| ROCK      |
| SPIDERMAN |
| OK        |
| SIX       |

---

# 🤖 Machine Learning Pipeline

```text
Webcam
   │
   ▼
OpenCV
   │
   ▼
MediaPipe
   │
   ▼
21 Hand Landmarks
   │
   ▼
Feature Vector (63 Features)
   │
   ▼
Random Forest Classifier
   │
   ▼
Predicted Gesture
   │
   ▼
Text To Speech
```

---

# 📈 Dataset Visualization

The project includes several visualization utilities.

| File                     | Purpose                 |
| ------------------------ | ----------------------- |
| plot_distribution.py     | Gesture distribution    |
| plot_landmarks.py        | Plot one hand sample    |
| plot_hand_skeleton.py    | Draw MediaPipe skeleton |
| plot_multiple_samples.py | Compare gesture samples |
| plot_pca.py              | PCA visualization       |

Example:

```bash
python visualization/plot_hand_skeleton.py
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository_url>

cd ai_deaf_connect
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

Using pip

```bash
pip install -r requirements.txt
```

or using uv

```bash
uv pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

Open browser

```
http://localhost:8501
```

---

# 🎯 Training Your Own Model

## Step 1

Collect Dataset

```bash
python training/collect_dataset.py
```

Dataset will be stored as:

```
dataset.csv
```

---

## Step 2

Train Model

```bash
python training/train_model.py
```

Output:

```
models/
    gesture_model.pkl
```

---

## Step 3

Run the Application

```bash
streamlit run app.py
```

---

# 📊 Current ML Model

| Property     | Value               |
| ------------ | ------------------- |
| Algorithm    | Random Forest       |
| Features     | 63                  |
| Input        | MediaPipe Landmarks |
| Output       | Gesture Label       |
| Model Format | gesture_model.pkl   |

---

# 🔊 Text To Speech

Detected gestures are automatically converted into speech.

Example:

```
Gesture

↓

FIVE

↓

Audio

↓

"Five"
```

Speech is generated only when the gesture changes to avoid repeated playback.

---

# 📌 Current Limitations

* Supports only static gestures
* One hand at a time
* English gesture labels
* Basic Random Forest model
* No sentence formation
* No dynamic gesture recognition

---

# 🚀 Future Roadmap

## Phase 2

* Confidence Threshold
* Prediction Smoothing
* FPS Counter
* Gesture History

## Phase 3

* 50+ Sign Language Gestures
* Sentence Builder
* Auto Sentence Speaking

## Phase 4

* Speech-to-Text
* Live Caption Generation
* Translation Support
* Multiple Languages

## Phase 5

* AI Deaf Connect Video Calling
* Real-Time Gesture Translation
* Real-Time Voice Translation
* WebRTC Integration

## Phase 6

* TensorFlow / PyTorch Model
* LSTM for Dynamic Gestures
* Transformer-based Sign Language Recognition

---

# 📚 Learning Outcomes

This project demonstrates:

* Computer Vision
* MediaPipe Hand Tracking
* Dataset Collection
* Feature Engineering
* Machine Learning
* Model Training
* Model Serialization
* Real-Time Prediction
* Data Visualization
* Streamlit Application Development

---

# 👨‍💻 Author

**Bharat Soni/Khushiram Ginnare/Rakesh Chhapre**

Python | AI | Machine Learning | Computer Vision Enthusiast

Working towards building **AI Deaf Connect**, an accessibility platform that enables seamless communication between hearing and hearing-impaired communities using Artificial Intelligence.

---

# 📜 License

This project is intended for educational, research, and learning purposes.

Feel free to fork, learn, and build upon it.