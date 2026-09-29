import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# CloudSentinel AI - Multiclass Dataset Preparation
# ============================================================

INPUT_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_dataset_v2.csv"

TRAIN_FILE = r"D:\CloudSentinel-AI\data\processed\multiclass_train.csv"
TEST_FILE = r"D:\CloudSentinel-AI\data\processed\multiclass_test.csv"

print("=" * 65)
print("CloudSentinel AI - Multiclass Dataset Preparation")
print("=" * 65)

# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:")
print(df.shape)

# ------------------------------------------------------------
# Features and multiclass target
# ------------------------------------------------------------

X = df.drop(
    columns=[
        "Label",
        "Attack_Type",
        "Target"
    ]
)

y = df["Attack_Type"]

print("\nNumber of classes:")
print(y.nunique())

print("\nClass distribution:")
print(y.value_counts())

# ------------------------------------------------------------
# Train / Test split
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ------------------------------------------------------------
# Save datasets
# ------------------------------------------------------------

train_data = X_train.copy()
train_data["Attack_Type"] = y_train

test_data = X_test.copy()
test_data["Attack_Type"] = y_test

train_data.to_csv(
    TRAIN_FILE,
    index=False
)

test_data.to_csv(
    TEST_FILE,
    index=False
)

# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

print("\nTraining samples:")
print(len(train_data))

print("\nTesting samples:")
print(len(test_data))

print("\nTraining class distribution:")
print(y_train.value_counts())

print("\nTesting class distribution:")
print(y_test.value_counts())

print("\nTraining file:")
print(TRAIN_FILE)

print("\nTesting file:")
print(TEST_FILE)

print("\nMulticlass preparation completed!")