import pandas as pd
import joblib

from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Project paths
ROOT = Path(__file__).resolve().parent.parent

TEST_FILE = ROOT / "data" / "processed" / "multiclass_test.csv"
MODEL_FILE = ROOT / "models" / "cloudsentinel_multiclass_model.pkl"
REPORT_FILE = ROOT / "reports" / "dashboard_evaluation.txt"
SAMPLE_FILE = ROOT / "data" / "processed" / "dashboard_labeled_test.csv"
FEATURE_FILE = ROOT / "data" / "processed" / "dashboard_test_sample.csv"

print("=" * 60)
print("CloudSentinel AI - Dashboard Validation")
print("=" * 60)

# Load the held-out test data and trained model
print("\nLoading test data...")
df = pd.read_csv(TEST_FILE)

print("Loading trained model...")
model = joblib.load(MODEL_FILE)

# Separate input features from actual labels
X = df.drop(columns=["Attack_Type"])
y_true = df["Attack_Type"]

print(f"Test rows: {len(df):,}")
print(f"Input features: {X.shape[1]}")

# Predict every row in the held-out test set
print("\nGenerating predictions...")
y_pred = model.predict(X)
probabilities = model.predict_proba(X)
confidence = probabilities.max(axis=1)

# Calculate evaluation metrics
accuracy = accuracy_score(y_true, y_pred)
labels = model.classes_

report = classification_report(
    y_true,
    y_pred,
    labels=labels,
    zero_division=0
)

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=labels
)

# Save a detailed evaluation report
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write("CloudSentinel AI - Dashboard Validation\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Test samples: {len(df)}\n")
    f.write(f"Features: {X.shape[1]}\n")
    f.write(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)\n\n")
    f.write("Classification Report:\n")
    f.write(report)
    f.write("\n\nClass order for confusion matrix:\n")
    f.write(", ".join(map(str, labels)))
    f.write("\n\nConfusion Matrix:\n")
    f.write(str(matrix))

# Create a reproducible 100-row dashboard sample
sample_size = min(100, len(df))
sample = df.sample(n=sample_size, random_state=42)

sample_X = sample.drop(columns=["Attack_Type"])
sample_true = sample["Attack_Type"]
sample_pred = model.predict(sample_X)
sample_prob = model.predict_proba(sample_X).max(axis=1)

# Save ground truth alongside predictions for evaluation
evaluation = sample_X.copy()
evaluation["Actual_Label"] = sample_true.to_numpy()
evaluation["Predicted_Attack"] = sample_pred
evaluation["Confidence"] = sample_prob
evaluation["Correct"] = (
    evaluation["Actual_Label"] == evaluation["Predicted_Attack"]
)

evaluation.to_csv(SAMPLE_FILE, index=False)

# Save features only, suitable for uploading to the dashboard
sample_X.to_csv(FEATURE_FILE, index=False)

print("\n" + "=" * 60)
print("DASHBOARD VALIDATION RESULTS")
print("=" * 60)
print(f"Full test accuracy: {accuracy * 100:.2f}%")
print(f"100-row sample accuracy: "
      f"{(sample_true.to_numpy() == sample_pred).mean() * 100:.2f}%")
print(f"Correct predictions: "
      f"{(sample_true.to_numpy() == sample_pred).sum()}/{sample_size}")

print("\nClassification Report:")
print(report)

print("\nConfusion Matrix:")
print("Class order:", list(labels))
print(matrix)

print("\nFiles saved:")
print(REPORT_FILE)
print(SAMPLE_FILE)
print(FEATURE_FILE)