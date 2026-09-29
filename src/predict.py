import pandas as pd
import numpy as np
import joblib


# ==========================================================
# CloudSentinel AI - Prediction Engine
# ==========================================================

MODEL_PATH = (
    r"D:\CloudSentinel-AI\models"
    r"\cloudsentinel_multiclass_model.pkl"
)

TEST_DATA_PATH = (
    r"D:\CloudSentinel-AI\data\processed"
    r"\multiclass_test.csv"
)


# ==========================================================
# Load Model
# ==========================================================

print("=" * 65)
print("CloudSentinel AI - Prediction Engine")
print("=" * 65)

print("\nLoading model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")


# ==========================================================
# Load Test Data
# ==========================================================

print("\nLoading test data...")

df = pd.read_csv(TEST_DATA_PATH)

print("Test dataset shape:", df.shape)


# ==========================================================
# Prepare Features
# ==========================================================

X = df.drop(columns=["Attack_Type"])

# Keep exactly the features used during training
X = X[model.feature_names_in_]

print("Feature count:", X.shape[1])


# ==========================================================
# Select One Network Flow
# ==========================================================

sample_index = 0

sample = X.iloc[[sample_index]]

actual_label = df.iloc[sample_index]["Attack_Type"]


# ==========================================================
# Prediction
# ==========================================================

print("\nAnalyzing network flow...")

prediction = model.predict(sample)[0]

probabilities = model.predict_proba(sample)[0]

confidence = np.max(probabilities) * 100


# ==========================================================
# Security Status
# ==========================================================

if prediction == "BENIGN":
    status = "BENIGN"
    risk = "LOW"

else:
    status = "ATTACK"

    if confidence >= 90:
        risk = "HIGH"
    elif confidence >= 70:
        risk = "MEDIUM"
    else:
        risk = "LOW"


# ==========================================================
# Display Result
# ==========================================================

print("\n" + "=" * 65)
print("CLOUDSENTINEL ANALYSIS")
print("=" * 65)

print(f"\nActual traffic type : {actual_label}")
print(f"Predicted type      : {prediction}")
print(f"Confidence          : {confidence:.2f}%")
print(f"Status              : {status}")
print(f"Risk level          : {risk}")

print("\nTop prediction probabilities:")

probability_df = pd.DataFrame({
    "Attack_Type": model.classes_,
    "Probability": probabilities
})

probability_df = probability_df.sort_values(
    by="Probability",
    ascending=False
)

print(
    probability_df.head(5).to_string(
        index=False
    )
)

print("\n" + "=" * 65)
print("Prediction completed!")
print("=" * 65)