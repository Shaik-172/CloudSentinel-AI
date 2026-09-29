import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print("=" * 65)
print("CloudSentinel AI - Multiclass Cross-Day Validation")
print("=" * 65)

# --------------------------------------------------
# 1. Load day-aware dataset
# --------------------------------------------------

DATA_PATH = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_day_dataset.csv"

print("\nLoading day-aware dataset...")
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

# --------------------------------------------------
# 2. Define train/test days
# --------------------------------------------------

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

print("\nTraining days:")
for day in TRAIN_DAYS:
    print(" -", day)

print("\nTesting days:")
for day in TEST_DAYS:
    print(" -", day)

# --------------------------------------------------
# 3. Split by source day
# --------------------------------------------------

train_df = df[df["Source_Day"].isin(TRAIN_DAYS)].copy()
test_df = df[df["Source_Day"].isin(TEST_DAYS)].copy()

print("\nTraining samples:", len(train_df))
print("Testing samples :", len(test_df))

# --------------------------------------------------
# 4. Display class distribution
# --------------------------------------------------

print("\nTraining class distribution:")
print(train_df["Attack_Type"].value_counts())

print("\nTesting class distribution:")
print(test_df["Attack_Type"].value_counts())

# --------------------------------------------------
# 5. Prepare features
# --------------------------------------------------

DROP_COLUMNS = [
    "Label",
    "Attack_Type",
    "Target",
    "Source_Day"
]

X_train = train_df.drop(columns=DROP_COLUMNS)
y_train = train_df["Attack_Type"]

X_test = test_df.drop(columns=DROP_COLUMNS)
y_test = test_df["Attack_Type"]

# Make sure train/test feature order is identical
X_test = X_test[X_train.columns]

print("\nFeature count:", X_train.shape[1])

# --------------------------------------------------
# 6. Create Random Forest
# --------------------------------------------------

print("\nCreating Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# --------------------------------------------------
# 7. Train
# --------------------------------------------------

print("Training multiclass cross-day model...")
print("Please wait...")

model.fit(X_train, y_train)

print("Training completed!")

# --------------------------------------------------
# 8. Predictions
# --------------------------------------------------

print("\nGenerating predictions...")

y_pred = model.predict(X_test)

# --------------------------------------------------
# 9. Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 65)
print("MULTICLASS CROSS-DAY RESULTS")
print("=" * 65)

print(f"\nAccuracy: {accuracy:.4f}")
print(f"Accuracy percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

# --------------------------------------------------
# 10. Confusion Matrix
# --------------------------------------------------

labels = sorted(
    set(y_test.unique()) |
    set(y_pred)
)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\nConfusion Matrix:")

print("\nClass order:")
print(labels)

print("\nMatrix:")
print(cm)

# --------------------------------------------------
# 11. Save model
# --------------------------------------------------

MODEL_PATH = (
    r"D:\CloudSentinel-AI\models"
    r"\cloudsentinel_multiclass_crossday_model.pkl"
)

joblib.dump(model, MODEL_PATH)

print("\n" + "=" * 65)
print("Cross-day multiclass model saved!")
print("=" * 65)

print("\nModel:")
print(MODEL_PATH)