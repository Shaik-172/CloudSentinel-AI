import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# CloudSentinel AI - Dataset Preparation
# ============================================================

INPUT_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_dataset_v2.csv"

TRAIN_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_train.csv"
TEST_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_test.csv"

print("=" * 60)
print("CloudSentinel AI - Preparing Training Data")
print("=" * 60)

# Load dataset
df = pd.read_csv(INPUT_FILE)

print("\nOriginal dataset:")
print(df.shape)

# Remove unnecessary text label
# Attack_Type will be used later for multiclass classification
X = df.drop(columns=["Label", "Attack_Type", "Target"])

y = df["Target"]

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

# Add target back
train_data = X_train.copy()
train_data["Target"] = y_train

test_data = X_test.copy()
test_data["Target"] = y_test

# Save
train_data.to_csv(TRAIN_FILE, index=False)
test_data.to_csv(TEST_FILE, index=False)

# ------------------------------------------------------------
# Results
# ------------------------------------------------------------

print("\nTraining samples:")
print(len(train_data))

print("\nTesting samples:")
print(len(test_data))

print("\nTraining distribution:")
print(y_train.value_counts())

print("\nTesting distribution:")
print(y_test.value_counts())

print("\nTraining file:")
print(TRAIN_FILE)

print("\nTesting file:")
print(TEST_FILE)

print("\nDataset preparation completed!")