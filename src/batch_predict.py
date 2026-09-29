import pandas as pd
import numpy as np
import joblib

print("=" * 70)
print("CloudSentinel AI - Batch Prediction Engine")
print("=" * 70)

MODEL_PATH = (
    r"D:\CloudSentinel-AI\models"
    r"\cloudsentinel_multiclass_model.pkl"
)

TEST_PATH = (
    r"D:\CloudSentinel-AI\data\processed"
    r"\multiclass_test.csv"
)

OUTPUT_PATH = (
    r"D:\CloudSentinel-AI\data\processed"
    r"\predictions.csv"
)

# --------------------------------------------------
# Load model
# --------------------------------------------------

print("\nLoading model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

print("\nLoading test dataset...")

df = pd.read_csv(TEST_PATH)

print("Dataset shape:", df.shape)

# --------------------------------------------------
# Prepare features
# --------------------------------------------------

X = df.drop(columns=["Attack_Type"])

X = X[model.feature_names_in_]

print("Feature count:", X.shape[1])

# --------------------------------------------------
# Generate predictions
# --------------------------------------------------

print("\nAnalyzing all network flows...")
print("Please wait...")

predictions = model.predict(X)
probabilities = model.predict_proba(X)

confidence = np.max(probabilities, axis=1) * 100

# --------------------------------------------------
# Add prediction information
# --------------------------------------------------

df["Predicted_Attack"] = predictions
df["Confidence"] = confidence

df["Status"] = np.where(
    df["Predicted_Attack"] == "BENIGN",
    "BENIGN",
    "ATTACK"
)

def get_risk(conf):
    if conf >= 90:
        return "HIGH"
    elif conf >= 70:
        return "MEDIUM"
    else:
        return "LOW"

df["Risk"] = df["Confidence"].apply(get_risk)

# --------------------------------------------------
# Save results
# --------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# --------------------------------------------------
# Statistics
# --------------------------------------------------

total = len(df)
attacks = (df["Status"] == "ATTACK").sum()
benign = (df["Status"] == "BENIGN").sum()

print("\n" + "=" * 70)
print("CLOUDSENTINEL BATCH ANALYSIS")
print("=" * 70)

print(f"\nTotal flows     : {total}")
print(f"Detected attacks: {attacks}")
print(f"Benign flows    : {benign}")

print("\nPredicted attack distribution:")

print(
    df["Predicted_Attack"]
    .value_counts()
    .to_string()
)

print("\nRisk distribution:")

print(
    df["Risk"]
    .value_counts()
    .to_string()
)

print("\nPrediction results saved:")
print(OUTPUT_PATH)

print("\n" + "=" * 70)
print("Batch prediction completed!")
print("=" * 70)