import pandas as pd
from sklearn.model_selection import train_test_split

# Load cleaned dataset
file_path = r"D:\CloudSentinel-AI\data\processed\ddos_cleaned.csv"

df = pd.read_csv(file_path)

# Separate features and target
X = df.drop("Label", axis=1)
y = df["Label"]

# Convert labels to numbers
y = y.map({
    "BENIGN": 0,
    "DDoS": 1
})

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Total records:", len(df))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining label distribution:")
print(y_train.value_counts())

print("\nTesting label distribution:")
print(y_test.value_counts())