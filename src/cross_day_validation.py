import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ============================================================
# CloudSentinel AI - Cross-Day Validation
# ============================================================

INPUT_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_day_dataset.csv"

MODEL_FILE = r"D:\CloudSentinel-AI\models\cloudsentinel_crossday_model.pkl"

print("=" * 65)
print("CloudSentinel AI - Cross-Day Validation")
print("=" * 65)

# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------

print("\nLoading day-aware dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset shape:", df.shape)

# ------------------------------------------------------------
# Define training and testing days
# ------------------------------------------------------------

TRAIN_DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday_Web",
    "Thursday_Infiltration"
]

TEST_DAYS = [
    "Friday_Morning",
    "Friday_PortScan",
    "Friday_DDoS"
]

# ------------------------------------------------------------
# Split by day
# ------------------------------------------------------------

train_df = df[
    df["Source_Day"].isin(TRAIN_DAYS)
].copy()

test_df = df[
    df["Source_Day"].isin(TEST_DAYS)
].copy()

print("\nTraining days:")
print(TRAIN_DAYS)

print("\nTesting days:")
print(TEST_DAYS)

print("\nTraining samples:", len(train_df))
print("Testing samples:", len(test_df))

# ------------------------------------------------------------
# Display class distributions
# ------------------------------------------------------------

print("\nTraining binary distribution:")
print(train_df["Target"].value_counts())

print("\nTesting binary distribution:")
print(test_df["Target"].value_counts())

print("\nTesting attack types:")
print(test_df["Attack_Type"].value_counts())

# ------------------------------------------------------------
# Prepare features
# ------------------------------------------------------------

DROP_COLUMNS = [
    "Label",
    "Attack_Type",
    "Target",
    "Source_Day"
]

X_train = train_df.drop(
    columns=DROP_COLUMNS
)

y_train = train_df["Target"]

X_test = test_df.drop(
    columns=DROP_COLUMNS
)

y_test = test_df["Target"]

print("\nTraining feature shape:", X_train.shape)
print("Testing feature shape:", X_test.shape)

# ------------------------------------------------------------
# Train model
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("Training cross-day Random Forest...")
print("=" * 65)

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("\nTraining completed!")

# ------------------------------------------------------------
# Predict
# ------------------------------------------------------------

print("\nGenerating Friday predictions...")

y_pred = model.predict(X_test)

# ------------------------------------------------------------
# Evaluate
# ------------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 65)
print("CROSS-DAY RESULTS")
print("=" * 65)

print(
    f"\nAccuracy: {accuracy:.4f}"
)

print(
    f"Accuracy percentage: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "BENIGN",
            "ATTACK"
        ]
    )
)

print("\nConfusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred
)

print(cm)

# ------------------------------------------------------------
# Evaluate each Friday source separately
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("RESULTS BY FRIDAY SOURCE")
print("=" * 65)

for day in TEST_DAYS:

    day_data = test_df[
        test_df["Source_Day"] == day
    ]

    X_day = day_data.drop(
        columns=DROP_COLUMNS
    )

    y_day = day_data["Target"]

    predictions = model.predict(X_day)

    day_accuracy = accuracy_score(
        y_day,
        predictions
    )

    print(
        f"\n{day}:"
    )

    print(
        f"Samples: {len(day_data)}"
    )

    print(
        f"Accuracy: {day_accuracy * 100:.2f}%"
    )

# ------------------------------------------------------------
# Save model
# ------------------------------------------------------------

joblib.dump(
    model,
    MODEL_FILE
)

print("\n" + "=" * 65)
print("Cross-day model saved!")
print("=" * 65)

print("\nModel:")
print(MODEL_FILE)