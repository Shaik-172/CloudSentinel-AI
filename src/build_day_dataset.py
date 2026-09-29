import pandas as pd
import os

# ============================================================
# CloudSentinel AI - Day-Aware Dataset
# ============================================================

DATA_DIR = r"D:\CloudSentinel-AI\data\raw\MachineLearningCVE"

OUTPUT_FILE = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_day_dataset.csv"

CHUNK_SIZE = 100000
MAX_PER_LABEL = 20000

files = {
    "Monday": "Monday-WorkingHours.pcap_ISCX.csv",
    "Tuesday": "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday": "Wednesday-workingHours.pcap_ISCX.csv",
    "Thursday_Web": "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Thursday_Infiltration": "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Friday_Morning": "Friday-WorkingHours-Morning.pcap_ISCX.csv",
    "Friday_PortScan": "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday_DDoS": "Friday-WorkingHours-Afternoon-DDoS.pcap_ISCX.csv"
}

label_data = {}

print("=" * 65)
print("CloudSentinel AI - Building Day-Aware Dataset")
print("=" * 65)

for day, filename in files.items():

    file_path = os.path.join(DATA_DIR, filename)

    print(f"\nProcessing: {day}")
    print(f"File: {filename}")

    if not os.path.exists(file_path):
        print("ERROR: File not found!")
        continue

    chunk_number = 0

    for chunk in pd.read_csv(
        file_path,
        chunksize=CHUNK_SIZE
    ):

        chunk_number += 1

        chunk.columns = chunk.columns.str.strip()

        chunk = chunk.replace(
            [float("inf"), float("-inf")],
            pd.NA
        )

        chunk = chunk.dropna()
        chunk = chunk.drop_duplicates()

        chunk["Label"] = (
            chunk["Label"]
            .astype(str)
            .str.strip()
        )

        # Store the original source day
        chunk["Source_Day"] = day

        for label in chunk["Label"].unique():

            label_rows = chunk[
                chunk["Label"] == label
            ]

            # Key keeps day and attack label separate
            key = (day, label)

            if key not in label_data:
                label_data[key] = []

            current_count = sum(
                len(x)
                for x in label_data[key]
            )

            remaining = MAX_PER_LABEL - current_count

            if remaining <= 0:
                continue

            label_rows = label_rows.head(remaining)

            if len(label_rows) > 0:
                label_data[key].append(label_rows)

        if chunk_number % 5 == 0:
            print(
                f"  Processed chunk {chunk_number}..."
            )

    print(f"Finished: {day}")


# ============================================================
# Combine
# ============================================================

print("\n" + "=" * 65)
print("Combining samples...")
print("=" * 65)

all_data = []

for (day, label), chunks in label_data.items():

    if not chunks:
        continue

    data = pd.concat(
        chunks,
        ignore_index=True
    )

    all_data.append(data)

    print(
        f"{day:<25} "
        f"{label:<30} "
        f"{len(data):>8}"
    )


combined = pd.concat(
    all_data,
    ignore_index=True
)

combined = combined.drop_duplicates()

# ============================================================
# Create targets
# ============================================================

combined["Attack_Type"] = combined["Label"]

combined["Target"] = combined["Label"].apply(
    lambda x: 0
    if x.strip().upper() == "BENIGN"
    else 1
)

# ============================================================
# Shuffle
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
# Final information
# ============================================================

print("\n" + "=" * 65)
print("Day-aware dataset created!")
print("=" * 65)

print("\nDataset shape:")
print(combined.shape)

print("\nRows by Source_Day:")
print(
    combined["Source_Day"]
    .value_counts()
)

print("\nAttack types:")
print(
    combined["Attack_Type"]
    .value_counts()
)

print("\nBinary distribution:")
print(
    combined["Target"]
    .value_counts()
)

print("\nSaved to:")
print(OUTPUT_FILE)