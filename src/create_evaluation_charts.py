import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Project report directory
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# --------------------------------
# 1. Cross-day confusion matrix
# --------------------------------

cm = np.array([
    [59943, 57],
    [26593, 13428]
])

labels = ["BENIGN", "ATTACK"]

plt.figure(figsize=(8, 6))

sns.heatmap(
    cm,
    annot=True,
    fmt=",",
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels
)

plt.title("CloudSentinel AI - Cross-Day Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.tight_layout()

plt.savefig(
    REPORTS / "cross_day_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------
# 2. Accuracy comparison
# --------------------------------

models = [
    "Random Split",
    "Cross-Day Test"
]

accuracy = [99.92, 73.36]

plt.figure(figsize=(8, 5))

bars = plt.bar(models, accuracy)

plt.ylim(0, 110)
plt.ylabel("Accuracy (%)")
plt.title("CloudSentinel AI - Evaluation Comparison")

for bar, value in zip(bars, accuracy):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{value:.2f}%",
        ha="center",
        fontweight="bold"
    )

plt.tight_layout()

plt.savefig(
    REPORTS / "model_accuracy_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Evaluation charts created successfully!")
print("Saved in the reports folder:")
print("- cross_day_confusion_matrix.png")
print("- model_accuracy_comparison.png")