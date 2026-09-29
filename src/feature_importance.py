import pandas as pd
import joblib

# Load cleaned dataset
data_path = r"D:\CloudSentinel-AI\data\processed\ddos_cleaned.csv"
model_path = r"D:\CloudSentinel-AI\models\cloudsentinel_ddos_model.pkl"

df = pd.read_csv(data_path)

# Separate features
X = df.drop("Label", axis=1)

# Load trained model
model = joblib.load(model_path)

# Get feature importance
importance = pd.Series(
    model.feature_importances_,
    index=X.columns
)

# Sort from highest to lowest
importance = importance.sort_values(ascending=False)

print("\nTop 15 important features:\n")
print(importance.head(15))