import pandas as pd

input_file = "data/processed/cloudsentinel_dataset_v2.csv"
output_file = "data/processed/dashboard_test_sample.csv"

print("Loading dataset...")

df = pd.read_csv(input_file, nrows=100)

# Keep only the 78 model input features
X = df.drop(columns=["Label", "Attack_Type", "Target"], errors="ignore")

X.to_csv(output_file, index=False)

print("Dashboard test file created!")
print("Rows:", len(X))
print("Features:", len(X.columns))
print("Saved to:", output_file)