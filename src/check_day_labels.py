import pandas as pd

path = "data/processed/cloudsentinel_day_dataset.csv"

print("Loading CloudSentinel dataset...")
df = pd.read_csv(path, usecols=["Source_Day", "Attack_Type"])

print("\nAttack classes available for each day:\n")

counts = pd.crosstab(
    df["Source_Day"],
    df["Attack_Type"]
)

print(counts.to_string())

print("\nTotal samples per day:")
print(df["Source_Day"].value_counts().to_string())