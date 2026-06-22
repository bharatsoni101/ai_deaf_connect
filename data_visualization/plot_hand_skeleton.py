"""
=========================================================
Plot Hand Skeleton From dataset.csv
=========================================================

Purpose:
--------
Draw a complete MediaPipe hand skeleton from one row
of dataset.csv.

Author:
-------
Bharat Soni
"""

import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------
# Load dataset
# ------------------------------------------------------

df = pd.read_csv("./dataset/dataset.csv")

# ------------------------------------------------------
# Select a sample
# ------------------------------------------------------

# Option 1:
# Select first row

#sample = df.iloc[0]

# ------------------------------------------------------
# Option 2:
# Uncomment to visualize a specific gesture
#
# sample = df[df["label"] == "ONE"].iloc[0]
sample = df[df["label"] == "SIX"].iloc[0]
# sample = df[df["label"] == "ROCK"].iloc[0]
# ------------------------------------------------------


gesture = sample["label"]

# ------------------------------------------------------
# Extract X and Y coordinates
# ------------------------------------------------------

x_coordinates = []
y_coordinates = []

for i in range(21):

    x_coordinates.append(
        sample[f"x{i}"]
    )

    y_coordinates.append(
        sample[f"y{i}"]
    )


# ------------------------------------------------------
# MediaPipe Hand Connections
# ------------------------------------------------------

connections = [

    # Thumb
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),

    # Index finger
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),

    # Middle finger
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    # Ring finger
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),

    # Little finger
    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),

    # Palm connection
    (0, 17)
]

# ------------------------------------------------------
# Create Figure
# ------------------------------------------------------

plt.figure(figsize=(8, 8))

# ------------------------------------------------------
# Draw lines
# ------------------------------------------------------

for start, end in connections:

    plt.plot(

        [x_coordinates[start], x_coordinates[end]],

        [y_coordinates[start], y_coordinates[end]]
    )

# ------------------------------------------------------
# Draw landmarks
# ------------------------------------------------------

plt.scatter(

    x_coordinates,

    y_coordinates
)

# ------------------------------------------------------
# Show landmark numbers
# ------------------------------------------------------

for i in range(21):

    plt.text(

        x_coordinates[i],

        y_coordinates[i],

        str(i),

        fontsize=10
    )

# ------------------------------------------------------
# Invert Y axis
# ------------------------------------------------------

plt.gca().invert_yaxis()

# ------------------------------------------------------
# Labels
# ------------------------------------------------------

plt.title(f"Gesture : {gesture}")

plt.xlabel("X Coordinate")

plt.ylabel("Y Coordinate")

plt.grid(True)

plt.show()