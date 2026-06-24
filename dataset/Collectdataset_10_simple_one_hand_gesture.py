import cv2
import mediapipe as mp
import csv
import os
import time

# -------------------------------
# CONFIGURATION
# -------------------------------

OUTPUT_CSV = "dataset/dataset.csv"       # Where to save the dataset
SAMPLES_PER_GESTURE = 300                # How many samples to collect per gesture
COUNTDOWN_SECONDS = 3                    # Countdown before recording starts

# All 10 gestures defined by your rule-based system in app.py
# Format: (label, finger_pattern_description)
GESTURES = [
    "ZERO",        # [0, 0, 0, 0, 0]
    "ONE",         # [0, 1, 0, 0, 0]
    "TWO",         # [0, 1, 1, 0, 0]
    "THREE",       # [0, 1, 1, 1, 0]
    "FOUR",        # [0, 1, 1, 1, 1]
    "FIVE",        # [1, 1, 1, 1, 1]
    "ROCK",        # [1, 0, 0, 0, 1]
    "SPIDERMAN",   # [1, 1, 0, 0, 1]
    "OK",          # [1, 0, 1, 1, 1]
    "SIX",         # [1, 1, 1, 0, 0]
]

# Reference: finger patterns from your app.py (for display only)
FINGER_PATTERNS = {
    "ZERO":      [0, 0, 0, 0, 0],
    "ONE":       [0, 1, 0, 0, 0],
    "TWO":       [0, 1, 1, 0, 0],
    "THREE":     [0, 1, 1, 1, 0],
    "FOUR":      [0, 1, 1, 1, 1],
    "FIVE":      [1, 1, 1, 1, 1],
    "ROCK":      [1, 0, 0, 0, 1],
    "SPIDERMAN": [1, 1, 0, 0, 1],
    "OK":        [1, 0, 1, 1, 1],
    "SIX":       [1, 1, 1, 0, 0],
}

# -------------------------------
# CSV HEADER
# Columns: label + x0,y0,z0, x1,y1,z1, ..., x20,y20,z20
# Total: 1 + (21 * 3) = 64 columns
# -------------------------------

def build_csv_header():
    header = ["label"]
    for i in range(21):
        header += [f"x{i}", f"y{i}", f"z{i}"]
    return header

# -------------------------------
# EXTRACT LANDMARK ROW FROM RESULTS
# Returns a flat list: [x0, y0, z0, x1, y1, z1, ..., x20, y20, z20]
# -------------------------------

def extract_landmarks(hand_landmarks):
    row = []
    for lm in hand_landmarks.landmark:
        row += [round(lm.x, 6), round(lm.y, 6), round(lm.z, 6)]
    return row

# -------------------------------
# SETUP
# -------------------------------

# Create output folder if not exists
os.makedirs("dataset", exist_ok=True)

# Check if CSV already exists (to append, not overwrite)
csv_exists = os.path.exists(OUTPUT_CSV)

# Open CSV in append mode
csv_file = open(OUTPUT_CSV, "a", newline="")
csv_writer = csv.writer(csv_file)

# Write header only if file is new
if not csv_exists:
    csv_writer.writerow(build_csv_header())
    print(f"✅ Created new dataset file: {OUTPUT_CSV}")
else:
    print(f"📂 Appending to existing dataset: {OUTPUT_CSV}")

# -------------------------------
# MEDIAPIPE SETUP
# -------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -------------------------------
# CAMERA SETUP
# -------------------------------

camera = cv2.VideoCapture(0)

print("\n🖐️  AI DEAF CONNECT — Dataset Collector")
print("=" * 45)
print(f"   Gestures to collect : {len(GESTURES)}")
print(f"   Samples per gesture : {SAMPLES_PER_GESTURE}")
print(f"   Total target samples: {len(GESTURES) * SAMPLES_PER_GESTURE}")
print("=" * 45)
print("\nControls:")
print("  [SPACE]  → Start collecting current gesture")
print("  [S]      → Skip current gesture")
print("  [Q]      → Quit and save")
print("=" * 45)

# -------------------------------
# MAIN COLLECTION LOOP
# -------------------------------

for gesture_index, gesture_label in enumerate(GESTURES):

    pattern = FINGER_PATTERNS[gesture_label]
    pattern_str = "".join(map(str, pattern))
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Little"]

    print(f"\n\n[{gesture_index + 1}/{len(GESTURES)}] Gesture: {gesture_label}")
    print(f"  Finger pattern : {pattern_str}")
    for i, (name, state) in enumerate(zip(finger_names, pattern)):
        status = "OPEN ✋" if state == 1 else "CLOSED ✊"
        print(f"    {name:8s} → {status}")
    print(f"\n  Make this gesture and press [SPACE] to start recording...")

    samples_collected = 0
    state = "WAITING"       # WAITING → COUNTDOWN → RECORDING → DONE
    countdown_start = None

    while True:

        success, frame = camera.read()
        if not success:
            print("⚠️  Webcam unavailable.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # ---- Draw hand skeleton ----
        if results.multi_hand_landmarks:
            for hl in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

        # ---- State machine ----

        if state == "WAITING":
            msg1 = f"Gesture: {gesture_label}  ({pattern_str})"
            msg2 = "Press [SPACE] to start | [S] to skip | [Q] to quit"
            cv2.putText(frame, msg1, (10, 40),  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)
            cv2.putText(frame, msg2, (10, 75),  cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

        elif state == "COUNTDOWN":
            elapsed = time.time() - countdown_start
            remaining = int(COUNTDOWN_SECONDS - elapsed) + 1
            if remaining <= 0:
                state = "RECORDING"
            else:
                cv2.putText(frame, f"Starting in: {remaining}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 165, 255), 3)

        elif state == "RECORDING":
            # Record landmark data
            if results.multi_hand_landmarks:
                for hl in results.multi_hand_landmarks:
                    landmark_row = extract_landmarks(hl)
                    csv_writer.writerow([gesture_label] + landmark_row)
                    samples_collected += 1

            # Progress bar
            progress = int((samples_collected / SAMPLES_PER_GESTURE) * 40)
            bar = "[" + "█" * progress + "." * (40 - progress) + "]"
            cv2.putText(frame, f"RECORDING {gesture_label}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f"{samples_collected}/{SAMPLES_PER_GESTURE} samples", (10, 75),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Terminal progress
            print(f"\r  Collecting: {bar} {samples_collected}/{SAMPLES_PER_GESTURE}", end="", flush=True)

            if samples_collected >= SAMPLES_PER_GESTURE:
                state = "DONE"
                csv_file.flush()    # Save to disk immediately

        elif state == "DONE":
            cv2.putText(frame, f"✅ {gesture_label} DONE! {samples_collected} samples saved.", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 128), 2)
            cv2.putText(frame, "Press any key for next gesture...", (10, 95),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        # ---- Overlay: gesture + sample count ----
        cv2.putText(frame,
                    f"[{gesture_index+1}/{len(GESTURES)}]",
                    (frame.shape[1] - 120, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)

        cv2.imshow("AI Deaf Connect — Dataset Collector", frame)

        # ---- Key handling ----
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == ord('Q'):
            print("\n\n🛑 Quit pressed. Saving and exiting...")
            camera.release()
            cv2.destroyAllWindows()
            csv_file.close()
            print(f"💾 Dataset saved to: {OUTPUT_CSV}")
            exit(0)

        elif key == ord('s') or key == ord('S'):
            print(f"\n  ⏭️  Skipping {gesture_label}...")
            break

        elif key == ord(' ') and state == "WAITING":
            state = "COUNTDOWN"
            countdown_start = time.time()

        elif state == "DONE":
            # Any key moves to next gesture
            if key != 255:
                print(f"\n  ✅ {gesture_label} complete. Moving to next...")
                break

# -------------------------------
# FINAL SUMMARY
# -------------------------------

camera.release()
cv2.destroyAllWindows()
csv_file.close()

# Count rows in CSV
with open(OUTPUT_CSV, "r") as f:
    total_rows = sum(1 for _ in f) - 1  # subtract header

print("\n\n" + "=" * 45)
print("   🎉 DATASET COLLECTION COMPLETE!")
print("=" * 45)
print(f"   File     : {OUTPUT_CSV}")
print(f"   Total rows collected: {total_rows}")
print(f"   Columns  : label + 63 landmark values (x,y,z × 21)")
print("=" * 45)
print("\nNext steps:")
print("  1. Review dataset/dataset.csv")
print("  2. Collect more samples if needed (re-run to append)")
print("  3. Train your model using models/train_model.py")