import cv2
import mediapipe as mp
import csv
import os
import time

# -------------------------------
# CONFIGURATION
# -------------------------------

OUTPUT_CSV = "dataset/dataset_AtoZ.csv"  # Where to save the dataset
SAMPLES_PER_GESTURE = 300                # How many samples to collect per gesture
COUNTDOWN_SECONDS = 3                    # Countdown before recording starts

# ASL A-Z alphabet gestures
# Finger pattern format: [Thumb, Index, Middle, Ring, Little]
# 1 = extended/open, 0 = closed/bent
# Note: Many ASL letters involve subtle hand shapes beyond simple open/close.
# The patterns below indicate the DOMINANT finger state for each letter.
# For letters like A, E, M, N, S, T — all fingers are curled/closed with thumb variation.
# Collect landmark data to let the ML model learn the fine-grained differences.
GESTURES = [
    "A",   # Fist with thumb to side
    "B",   # Four fingers up, thumb tucked across palm
    "C",   # Curved hand (C-shape)
    "D",   # Index up, other fingers curl to touch thumb
    "E",   # All fingers bent/hooked, thumb tucked under
    "F",   # Index+thumb form circle, other three fingers up
    "G",   # Index points sideways, thumb parallel
    "H",   # Index+middle point sideways together
    "I",   # Pinky up, others closed
    "J",   # Pinky up + J motion (static: same as I)
    "K",   # Index+middle up (V-shape), thumb between them
    "L",   # L-shape: thumb + index out
    "M",   # Three fingers fold over thumb (fist variant)
    "N",   # Two fingers fold over thumb (fist variant)
    "O",   # All fingers curve to touch thumb (O-shape)
    "P",   # K-shape pointing downward
    "Q",   # G-shape pointing downward
    "R",   # Index+middle crossed/twisted
    "S",   # Fist with thumb over fingers
    "T",   # Fist with thumb between index and middle
    "U",   # Index+middle up together (parallel)
    "V",   # Index+middle up in V/peace sign
    "W",   # Index+middle+ring up (3 fingers)
    "X",   # Index finger hooked/bent
    "Y",   # Thumb+pinky out (hang loose)
    "Z",   # Index draws Z in air (static: index pointing forward)
]

# Finger state reference: [Thumb, Index, Middle, Ring, Little]
# Used for on-screen guidance during collection.
# 1 = extended, 0 = closed/curled
# ⚠️  ASL relies heavily on hand SHAPE, not just open/closed state.
#     These are approximate guides — the ML model learns exact landmarks.
FINGER_PATTERNS = {
    "A": [1, 0, 0, 0, 0],   # Fist, thumb rests at side
    "B": [0, 1, 1, 1, 1],   # 4 fingers up, thumb tucked
    "C": [1, 1, 1, 1, 1],   # All curved into C
    "D": [0, 1, 0, 0, 0],   # Index up, rest curl to thumb
    "E": [0, 0, 0, 0, 0],   # All fingers hooked/bent
    "F": [0, 0, 1, 1, 1],   # Index+thumb circle, 3 fingers up
    "G": [1, 1, 0, 0, 0],   # Index+thumb pointing sideways
    "H": [0, 1, 1, 0, 0],   # Index+middle pointing sideways
    "I": [0, 0, 0, 0, 1],   # Pinky only
    "J": [0, 0, 0, 0, 1],   # Pinky only (+ J motion)
    "K": [1, 1, 1, 0, 0],   # Index+middle up, thumb out
    "L": [1, 1, 0, 0, 0],   # Thumb+index L-shape
    "M": [0, 0, 0, 0, 0],   # Three fingers over thumb (closed)
    "N": [0, 0, 0, 0, 0],   # Two fingers over thumb (closed)
    "O": [0, 0, 0, 0, 0],   # All curve to form O
    "P": [1, 1, 1, 0, 0],   # K pointing down
    "Q": [1, 1, 0, 0, 0],   # G pointing down
    "R": [0, 1, 1, 0, 0],   # Index+middle crossed
    "S": [0, 0, 0, 0, 0],   # Fist, thumb over fingers
    "T": [0, 0, 0, 0, 0],   # Fist, thumb between index+middle
    "U": [0, 1, 1, 0, 0],   # Index+middle up together
    "V": [0, 1, 1, 0, 0],   # Index+middle V (peace)
    "W": [0, 1, 1, 1, 0],   # Index+middle+ring up
    "X": [0, 1, 0, 0, 0],   # Index hooked/bent
    "Y": [1, 0, 0, 0, 1],   # Thumb+pinky out
    "Z": [0, 1, 0, 0, 0],   # Index pointing forward (draws Z)
}

# Per-letter human-readable shape hints shown in terminal during collection
GESTURE_HINTS = {
    # "A": "Fist with thumb resting at side of index finger",
    # "B": "Four fingers straight up, thumb tucked flat across palm",
    # "C": "All fingers curve into a C-shape (as if holding a cup)",
    # "D": "Index finger points up, other fingers curl to meet thumb",
    # "E": "All fingers bent/hooked, thumb tucked under fingers",
    # "F": "Index+thumb form a circle; middle, ring, pinky point up",
    # "G": "Index points sideways, thumb parallel (like a gun sideways)",
    # "H": "Index+middle together pointing sideways horizontally",
    # "I": "Pinky finger only extended, others closed in fist",
    # "J": "Start with pinky up (like I), then trace a J in air",
    # "K": "Index+middle up in V, thumb touching middle — like a K",
    # "L": "Index up + thumb out to side forming an L-shape",
    # "M": "Three fingers (index, middle, ring) folded over thumb",
    # "N": "Two fingers (index, middle) folded over thumb",
    # "O": "All fingers and thumb curve to form an O shape",
    # "P": "K-shape rotated so fingers point downward",
    "Q": "G-shape rotated so fingers point downward",
    # "R": "Index and middle fingers crossed (twisted together)",
    # "S": "Fist with thumb wrapped over all fingers",
    # "T": "Fist with thumb tucked between index and middle fingers",
    # "U": "Index+middle pointing up together side by side",
    # "V": "Index+middle up apart in a V / peace sign",
    # "W": "Index+middle+ring all up, thumb+pinky closed",
    # "X": "Index finger bent/hooked, all others closed",
    # "Y": "Thumb + pinky extended (hang loose / shaka sign)",
    # "Z": "Index points out; trace a Z in air (hold start position)",
}
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

print("\n🖐️  AI DEAF CONNECT — Dataset Collector (A-Z ASL Alphabet)")
print("=" * 55)
print(f"   Gestures to collect : {len(GESTURES)} (A to Z)")
print(f"   Samples per gesture : {SAMPLES_PER_GESTURE}")
print(f"   Total target samples: {len(GESTURES) * SAMPLES_PER_GESTURE}")
print("=" * 55)
print("\n  TIPS FOR ACCURATE DATA:")
print("  * Keep hand clearly visible and well-lit")
print("  * Vary hand angle slightly across samples")
print("  * For similar letters (M/N, U/V, S/T/E/A),")
print("    hold the exact correct shape carefully")
print("  * J and Z involve motion -- hold the START position")
print("=" * 55)
print("\nControls:")
print("  [SPACE]  -> Start collecting current gesture")
print("  [S]      -> Skip current gesture")
print("  [Q]      -> Quit and save")
print("=" * 55)

# -------------------------------
# MAIN COLLECTION LOOP
# -------------------------------

for gesture_index, gesture_label in enumerate(GESTURES):

    hint = GESTURE_HINTS[gesture_label]
    pattern = FINGER_PATTERNS[gesture_label]
    pattern_str = "".join(map(str, pattern))
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Little"]

    print(f"\n\n[{gesture_index + 1}/{len(GESTURES)}] Letter: {gesture_label}")
    print(f"  Shape hint     : {hint}")
    print(f"  Finger pattern : {pattern_str}  (T I M R L)")
    for i, (name, state) in enumerate(zip(finger_names, pattern)):
        status = "EXTENDED" if state == 1 else "CLOSED  "
        print(f"    {name:8s} -> {status}")
    print(f"\n  Make the '{gesture_label}' sign and press [SPACE] to start recording...")

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
            msg1 = f"Letter: {gesture_label}  |  {hint[:45]}"
            msg2 = "SPACE=start  S=skip  Q=quit"
            cv2.putText(frame, msg1, (10, 40),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
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
            cv2.putText(frame, f"RECORDING '{gesture_label}'", (10, 40),
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

print("\n\n" + "=" * 55)
print("   DATASET COLLECTION COMPLETE!")
print("=" * 55)
print(f"   File     : {OUTPUT_CSV}")
print(f"   Total rows collected: {total_rows}")
print(f"   Columns  : label + 63 landmark values (x,y,z x 21)")
print(f"   Labels   : A to Z  ({len(GESTURES)} classes)")
print("=" * 55)
print("\nNext steps:")
print("  1. Review dataset/dataset.csv")
print("  2. Collect more samples if needed (re-run to append)")
print("  3. Train your model using models/train_model.py")