import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load cleaned dataset
file_path = r"D:\CloudSentinel-AI\data\processed\ddos_cleaned.csv"

df = pd.read_csv(file_path)

# Separate features and target
X = df.drop("Label", axis=1)
y = df["Label"].map({
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

print("Training Random Forest...")

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train
model.fit(X_train, y_train)

print("Training completed!")

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["BENIGN", "DDoS"]
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
model_path = r"D:\CloudSentinel-AI\models\cloudsentinel_ddos_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved to:")
print(model_path)