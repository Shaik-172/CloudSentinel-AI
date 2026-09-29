import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# File paths
MODEL_PATH = "models/cloudsentinel_multiclass_model.pkl"
TEST_PATH = "data/processed/multiclass_test.csv"
REPORT_PATH = "reports/multiclass_evaluation_report.txt"

print("Loading CloudSentinel AI model...")
model = joblib.load(MODEL_PATH)

print("Loading test dataset...")
test = pd.read_csv(TEST_PATH)

# Separate features and actual labels
X_test = test.drop(columns=["Attack_Type"])
y_test = test["Attack_Type"]

print("Generating predictions...")
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
labels = sorted(y_test.unique())

report = classification_report(
    y_test,
    y_pred,
    labels=labels,
    zero_division=0
)

matrix = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

# Build report
content = f"""
CLOUDSENTINEL AI
MULTICLASS MODEL EVALUATION REPORT
==================================

Model: Random Forest
Dataset: CIC-IDS2017
Evaluation: Stratified random test split

Test samples: {len(y_test)}
Features: {X_test.shape[1]}
Classes: {len(labels)}

Accuracy: {accuracy:.4f}
Accuracy percentage: {accuracy * 100:.2f}%

CLASSIFICATION REPORT
=====================
{report}

CONFUSION MATRIX
================
Class order:
{labels}

{matrix}

LIMITATIONS
===========
1. This is a random-split evaluation, not a cross-day test.
2. Rare attack classes have very few test samples.
3. Results may not represent performance on unseen network traffic.
4. The separate binary cross-day evaluation achieved 73.36%
   accuracy and should be reported independently.
"""

os.makedirs("reports", exist_ok=True)

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write(content)

print("\nReport saved successfully!")
print(REPORT_PATH)
print(f"\nAccuracy: {accuracy * 100:.2f}%")