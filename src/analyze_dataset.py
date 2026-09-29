import pandas as pd

file_path = r"D:\CloudSentinel-AI\data\raw\MachineLearningCVE\Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv"

df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

print("Dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nLabels:")
print(df["Label"].value_counts())

print("\nData types:")
print(df.dtypes.value_counts())

print("\nInfinite values:")
print(df.isin([float("inf"), float("-inf")]).sum().sum())