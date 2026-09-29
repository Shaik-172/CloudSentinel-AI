import pandas as pd
import joblib
import matplotlib.pyplot as plt

print("=" * 70)
print("CloudSentinel AI - Multiclass Feature Importance")
print("=" * 70)

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

MODEL_PATH = (
    r"D:\CloudSentinel-AI\models"
    r"\cloudsentinel_multiclass_model.pkl"
)

DATA_PATH = (
    r"D:\CloudSentinel-AI\data\processed"
    r"\multiclass_train.csv"
)

CSV_OUTPUT = (
    r"D:\CloudSentinel-AI\data\processed"
    r"\multiclass_feature_importance.csv"
)

IMAGE_OUTPUT = (
    r"D:\CloudSentinel-AI\reports"
    r"\multiclass_feature_importance.png"
)

# --------------------------------------------------
# 2. Load model
# --------------------------------------------------

print("\nLoading trained multiclass model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")

# --------------------------------------------------
# 3. Load training data
# --------------------------------------------------

print("\nLoading training data...")

df = pd.read_csv(DATA_PATH)

# Attack_Type is the target
X = df.drop(columns=["Attack_Type"])

print("Feature count:", X.shape[1])

# --------------------------------------------------
# 4. Extract feature importance
# --------------------------------------------------

print("\nCalculating feature importance...")

importance = model.feature_importances_

feature_names = X.columns

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
})

# Sort highest → lowest
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
).reset_index(drop=True)

# --------------------------------------------------
# 5. Display top 20
# --------------------------------------------------

print("\n" + "=" * 70)
print("TOP 20 IMPORTANT FEATURES")
print("=" * 70)

print(
    importance_df.head(20).to_string(
        index=False
    )
)

# --------------------------------------------------
# 6. Save complete feature importance
# --------------------------------------------------

importance_df.to_csv(
    CSV_OUTPUT,
    index=False
)

print("\nComplete feature importance saved:")
print(CSV_OUTPUT)

# --------------------------------------------------
# 7. Plot top 20
# --------------------------------------------------

top_n = 20

top_features = importance_df.head(top_n)

plt.figure(figsize=(12, 8))

plt.barh(
    top_features["Feature"][::-1],
    top_features["Importance"][::-1]
)

plt.xlabel("Importance")
plt.ylabel("Network Feature")
plt.title(
    "CloudSentinel AI - Top 20 Multiclass Feature Importance"
)

plt.tight_layout()

plt.savefig(
    IMAGE_OUTPUT,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFeature importance chart saved:")
print(IMAGE_OUTPUT)

print("\n" + "=" * 70)
print("FEATURE IMPORTANCE ANALYSIS COMPLETED")
print("=" * 70)