import pandas as pd
import os

# ============================================================
# CloudSentinel AI - Full Dataset Sampler
# ============================================================

DATA_DIR = r"D:\CloudSentinel-AI\data\raw\MachineLearningCVE"

OUTPUT_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_dataset_v2.csv"

# Number of rows read at a time
CHUNK_SIZE = 100000

# Maximum number of samples kept for each label
MAX_PER_LABEL = 20000

files = [
    "Monday-WorkingHours.pcap_ISCX.csv",
    "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv",
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Friday-WorkingHours-Morning.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv"
]

# Store collected samples
label_data = {}

print("=" * 60)
print("CloudSentinel AI - Building Improved Dataset")
print("=" * 60)

for filename in files:

    file_path = os.path.join(DATA_DIR, filename)

    print(f"\nProcessing: {filename}")

    if not os.path.exists(file_path):
        print("ERROR: File not found!")
        print(file_path)
        continue

    chunk_number = 0

    for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):

        chunk_number += 1

        # Clean column names
        chunk.columns = chunk.columns.str.strip()

        # Clean infinite values
        chunk = chunk.replace(
            [float("inf"), float("-inf")],
            pd.NA
        )

        # Remove missing values
        chunk = chunk.dropna()

        # Remove duplicates inside chunk
        chunk = chunk.drop_duplicates()

        if "Label" not in chunk.columns:
            print("ERROR: Label column not found!")
            break

        # Clean label text
        chunk["Label"] = chunk["Label"].astype(str).str.strip()

        # Process every attack label
        for label in chunk["Label"].unique():

            # Create label-specific data
            label_rows = chunk[chunk["Label"] == label]

            # Initialize storage
            if label not in label_data:
                label_data[label] = []

            # Current number already collected
            current_count = sum(
                len(x) for x in label_data[label]
            )

            # Remaining samples needed
            remaining = MAX_PER_LABEL - current_count

            if remaining <= 0:
                continue

            # Take only what we still need
            label_rows = label_rows.head(remaining)

            if len(label_rows) > 0:
                label_data[label].append(label_rows)

        if chunk_number % 5 == 0:
            print(
                f"  Processed chunk {chunk_number}..."
            )

    print(f"Finished: {filename}")


# ============================================================
# Combine all collected labels
# ============================================================

print("\n" + "=" * 60)
print("Combining samples...")
print("=" * 60)

all_data = []

for label, chunks in label_data.items():

    if len(chunks) == 0:
        continue

    label_df = pd.concat(
        chunks,
        ignore_index=True
    )

    all_data.append(label_df)

    print(
        f"{label:<35} {len(label_df):>8} rows"
    )


combined = pd.concat(
    all_data,
    ignore_index=True
)

# Remove duplicates again after combining
combined = combined.drop_duplicates()

# ============================================================
# Create CloudSentinel labels
# ============================================================

combined["Attack_Type"] = combined["Label"]

combined["Target"] = combined["Label"].apply(
    lambda x: 0
    if x.strip().upper() == "BENIGN"
    else 1
)

# ============================================================
# Shuffle dataset
# ============================================================

combined = combined.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ============================================================
# Save
# ============================================================

combined.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# Final report
# ============================================================

print("\n" + "=" * 60)
print("CloudSentinel dataset created successfully!")
print("=" * 60)

print("\nDataset shape:")
print(combined.shape)

print("\nBinary distribution:")
print(combined["Target"].value_counts())

print("\nAttack types:")
print(combined["Attack_Type"].value_counts())

print("\nSaved to:")
print(OUTPUT_FILE)