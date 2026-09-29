import pandas as pd

# Original dataset
file_path = r"D:\CloudSentinel-AI\data\raw\MachineLearningCVE\Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv"

# Load data
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

print("Original shape:", df.shape)

# Replace infinite values with NaN
df = df.replace([float("inf"), float("-inf")], pd.NA)

# Remove rows containing missing values
df = df.dropna()

# Remove duplicate rows
df = df.drop_duplicates()

print("Cleaned shape:", df.shape)

print("\nLabels after cleaning:")
print(df["Label"].value_counts())

# Save cleaned dataset
output_path = r"D:\CloudSentinel-AI\data\processed\ddos_cleaned.csv"

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved to:")
print(output_path)