import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score


print("=" * 75)
print("CloudSentinel AI - Leave-One-Day-Out Multiclass Validation")
print("=" * 75)

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

DATA_PATH = r"D:\CloudSentinel-AI\data\processed\cloudsentinel_day_dataset.csv"

print("\nLoading dataset...")
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

# --------------------------------------------------
# 2. Available source days
# --------------------------------------------------

days = sorted(df["Source_Day"].unique())

print("\nAvailable source days:")

for day in days:
    print(" -", day)

# --------------------------------------------------
# 3. Results storage
# --------------------------------------------------

results = []

# --------------------------------------------------
# 4. Leave-one-day-out evaluation
# --------------------------------------------------

for test_day in days:

    print("\n" + "=" * 75)
    print("TEST DAY:", test_day)
    print("=" * 75)

    # -------------------------------
    # Split train/test by day
    # -------------------------------

    train_df = df[df["Source_Day"] != test_day].copy()
    test_df = df[df["Source_Day"] == test_day].copy()

    # -------------------------------
    # Find shared classes
    # -------------------------------

    train_classes = set(train_df["Attack_Type"].unique())
    test_classes = set(test_df["Attack_Type"].unique())

    shared_classes = sorted(
        train_classes.intersection(test_classes)
    )

    print("\nShared classes:", len(shared_classes))

    print("Classes:")
    for cls in shared_classes:
        print(" -", cls)

    # Need at least 2 classes
    if len(shared_classes) < 2:
        print("\nSkipping: fewer than 2 shared classes.")
        continue

    # -------------------------------
    # Filter to shared classes
    # -------------------------------

    train_df = train_df[
        train_df["Attack_Type"].isin(shared_classes)
    ]

    test_df = test_df[
        test_df["Attack_Type"].isin(shared_classes)
    ]

    print("\nTraining samples:", len(train_df))
    print("Testing samples :", len(test_df))

    # -------------------------------
    # Features
    # -------------------------------

    DROP_COLUMNS = [
        "Label",
        "Attack_Type",
        "Target",
        "Source_Day"
    ]

    X_train = train_df.drop(columns=DROP_COLUMNS)
    y_train = train_df["Attack_Type"]

    X_test = test_df.drop(columns=DROP_COLUMNS)
    y_test = test_df["Attack_Type"]

    X_test = X_test[X_train.columns]

    # -------------------------------
    # Train model
    # -------------------------------

    print("\nTraining Random Forest...")

    model = RandomForestClassifier(
        n_estimators=150,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # -------------------------------
    # Predict
    # -------------------------------

    print("Generating predictions...")

    y_pred = model.predict(X_test)

    # -------------------------------
    # Metrics
    # -------------------------------

    accuracy = accuracy_score(y_test, y_pred)

    macro_f1 = f1_score(
        y_test,
        y_pred,
        average="macro",
        zero_division=0
    )

    weighted_f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    print("\nResults:")
    print(f"Accuracy   : {accuracy:.4f}")
    print(f"Macro F1   : {macro_f1:.4f}")
    print(f"Weighted F1: {weighted_f1:.4f}")

    # -------------------------------
    # Store results
    # -------------------------------

    results.append({
        "Test_Day": test_day,
        "Shared_Classes": len(shared_classes),
        "Train_Samples": len(train_df),
        "Test_Samples": len(test_df),
        "Accuracy": accuracy,
        "Macro_F1": macro_f1,
        "Weighted_F1": weighted_f1
    })


# --------------------------------------------------
# 5. Final summary
# --------------------------------------------------

print("\n\n" + "=" * 75)
print("LEAVE-ONE-DAY-OUT SUMMARY")
print("=" * 75)

if results:

    results_df = pd.DataFrame(results)

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    # Save results
    RESULTS_PATH = (
        r"D:\CloudSentinel-AI\data\processed"
        r"\multiclass_leave_one_day_results.csv"
    )

    results_df.to_csv(
        RESULTS_PATH,
        index=False
    )

    print("\nResults saved:")
    print(RESULTS_PATH)

else:

    print("\nNo valid multi-class day split was found.")

print("\nDone!")