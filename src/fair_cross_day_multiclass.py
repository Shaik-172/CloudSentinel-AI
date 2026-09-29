import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print("=" * 70)
print("CloudSentinel AI - Fair Multiclass Cross-Day Validation")
print("=" * 70)

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

DATA_PATH = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_day_dataset.csv"

print("\nLoading day-aware dataset...")
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

# --------------------------------------------------
# 2. Define training and testing days
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

# --------------------------------------------------
# 3. Create initial train/test split
# --------------------------------------------------

train_df = df[df["Source_Day"].isin(TRAIN_DAYS)].copy()
test_df = df[df["Source_Day"].isin(TEST_DAYS)].copy()

print("\nInitial training samples:", len(train_df))
print("Initial testing samples :", len(test_df))

# --------------------------------------------------
# 4. Find classes shared by both sets
# --------------------------------------------------

train_classes = set(train_df["Attack_Type"].unique())
test_classes = set(test_df["Attack_Type"].unique())

shared_classes = sorted(train_classes.intersection(test_classes))

print("\nClasses available in BOTH training and testing:")
for cls in shared_classes:
    print(" -", cls)

print("\nNumber of shared classes:", len(shared_classes))

# --------------------------------------------------
# 5. Keep only shared classes
# --------------------------------------------------

train_df = train_df[
    train_df["Attack_Type"].isin(shared_classes)
].copy()

test_df = test_df[
    test_df["Attack_Type"].isin(shared_classes)
].copy()

print("\nAfter shared-class filtering:")
print("Training samples:", len(train_df))
print("Testing samples :", len(test_df))

# --------------------------------------------------
# 6. Show distributions
# --------------------------------------------------

print("\nTraining distribution:")
print(train_df["Attack_Type"].value_counts())

print("\nTesting distribution:")
print(test_df["Attack_Type"].value_counts())

# --------------------------------------------------
# 7. Prepare features
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

# Ensure identical feature order
X_test = X_test[X_train.columns]

print("\nFeature count:", X_train.shape[1])

# --------------------------------------------------
# 8. Create model
# --------------------------------------------------

print("\nCreating Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# --------------------------------------------------
# 9. Train
# --------------------------------------------------

print("Training fair cross-day model...")
print("Please wait...")

model.fit(X_train, y_train)

print("Training completed!")

# --------------------------------------------------
# 10. Predict
# --------------------------------------------------

print("\nGenerating predictions...")

y_pred = model.predict(X_test)

# --------------------------------------------------
# 11. Evaluate
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 70)
print("FAIR MULTICLASS CROSS-DAY RESULTS")
print("=" * 70)

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
# 12. Confusion matrix
# --------------------------------------------------

labels = sorted(shared_classes)

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
# 13. Save model
# --------------------------------------------------

MODEL_PATH = (
    r"D:\CloudSentinel-AI\models"
    r"\cloudsentinel_fair_crossday_multiclass_model.pkl"
)

joblib.dump(model, MODEL_PATH)

print("\n" + "=" * 70)
print("Fair cross-day model saved!")
print("=" * 70)

print("\nModel:")
print(MODEL_PATH)