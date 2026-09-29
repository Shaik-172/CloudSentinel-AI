import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ============================================================
# CloudSentinel AI - Binary Attack Detection
# ============================================================

TRAIN_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_train.csv"
TEST_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_test.csv"

MODEL_FILE = r"D:\CloudSentinel-AI\models\cloudsentinel_binary_model.pkl"

print("=" * 60)
print("CloudSentinel AI - Training Binary Detector")
print("=" * 60)

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

print("\nLoading training data...")
train_data = pd.read_csv(TRAIN_FILE)

print("Loading testing data...")
test_data = pd.read_csv(TEST_FILE)

# ------------------------------------------------------------
# Separate features and target
# ------------------------------------------------------------

X_train = train_data.drop(columns=["Target"])
y_train = train_data["Target"]

X_test = test_data.drop(columns=["Target"])
y_test = test_data["Target"]

print("\nTraining shape:", X_train.shape)
print("Testing shape:", X_test.shape)

# ------------------------------------------------------------
# Create Random Forest
# ------------------------------------------------------------

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# ------------------------------------------------------------
# Train
# ------------------------------------------------------------

print("\nTraining CloudSentinel...")
print("Please wait...")

model.fit(X_train, y_train)

print("Training completed!")

# ------------------------------------------------------------
# Predictions
# ------------------------------------------------------------

print("\nGenerating predictions...")

y_pred = model.predict(X_test)

# ------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print(f"\nAccuracy: {accuracy:.4f}")
print(f"Accuracy percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["BENIGN", "ATTACK"]
    )
)

print("Confusion Matrix:")

cm = confusion_matrix(y_test, y_pred)

print(cm)

# ------------------------------------------------------------
# Save model
# ------------------------------------------------------------

joblib.dump(model, MODEL_FILE)

print("\nModel saved to:")
print(MODEL_FILE)

print("\nCloudSentinel binary detector completed!")