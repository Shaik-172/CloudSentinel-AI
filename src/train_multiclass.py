import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ============================================================
# CloudSentinel AI - Multiclass Attack Classifier
# ============================================================

TRAIN_FILE = r"D:\CloudSentinel-AI\data\processed\multiclass_train.csv"
TEST_FILE = r"D:\CloudSentinel-AI\data\processed\multiclass_test.csv"

MODEL_FILE = r"D:\CloudSentinel-AI\models\cloudsentinel_multiclass_model.pkl"

print("=" * 65)
print("CloudSentinel AI - Multiclass Attack Classifier")
print("=" * 65)

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

X_train = train_data.drop(
    columns=["Attack_Type"]
)

y_train = train_data["Attack_Type"]

X_test = test_data.drop(
    columns=["Attack_Type"]
)

y_test = test_data["Attack_Type"]

print("\nTraining shape:", X_train.shape)
print("Testing shape:", X_test.shape)

print("\nNumber of attack classes:")
print(y_train.nunique())

# ------------------------------------------------------------
# Create model
# ------------------------------------------------------------

print("\nCreating Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# ------------------------------------------------------------
# Train
# ------------------------------------------------------------

print("\nTraining multiclass model...")
print("Please wait...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")

# ------------------------------------------------------------
# Predictions
# ------------------------------------------------------------

print("\nGenerating predictions...")

y_pred = model.predict(X_test)

# ------------------------------------------------------------
# Overall accuracy
# ------------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 65)
print("MULTICLASS RESULTS")
print("=" * 65)

print(
    f"\nAccuracy: {accuracy:.4f}"
)

print(
    f"Accuracy percentage: {accuracy * 100:.2f}%"
)

# ------------------------------------------------------------
# Classification report
# ------------------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

# ------------------------------------------------------------
# Confusion matrix
# ------------------------------------------------------------

print("\nConfusion Matrix:")

labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\nClass order:")
print(labels)

print("\nMatrix:")
print(cm)

# ------------------------------------------------------------
# Save model
# ------------------------------------------------------------

joblib.dump(
    model,
    MODEL_FILE
)

print("\n" + "=" * 65)
print("Multiclass model saved!")
print("=" * 65)

print("\nModel:")
print(MODEL_FILE)