# CloudSentinel AI — Model Evaluation Report

## 1. Project Overview

CloudSentinel AI is a machine-learning-based network intrusion detection system developed using the CIC-IDS2017 dataset. It uses a Random Forest classifier to identify benign network traffic and potential attacks. A multiclass model is also used to classify different attack categories.

## 2. Dataset

* **Dataset:** CIC-IDS2017 MachineLearningCSV
* **Features:** 78 network-flow features
* **Preprocessing:** Missing values, duplicate records, and infinite values were handled during data preparation.
* **Models:** Random Forest classifiers
* **Evaluation approaches:** Random train/test split and cross-day validation

The processed datasets use selected and capped samples from the original dataset. Therefore, their class distributions are not the original CIC-IDS2017 distributions.

## 3. Binary Classification — Random Split

The binary model was evaluated using a stratified random train/test split.

| Metric          | Result |
| --------------- | -----: |
| Accuracy        | 99.92% |
| True negatives  |  3,997 |
| False positives |      3 |
| False negatives |     15 |
| True positives  | 18,437 |

The model performed well on this randomly held-out test set. However, records from the same collection days may appear in both training and testing data. Consequently, this result should not be interpreted as proof of equivalent performance on unseen network environments.

## 4. Binary Classification — Cross-Day Validation

The model was trained on selected earlier collection days and evaluated on Friday traffic.

| Metric           |  Result |
| ---------------- | ------: |
| Test samples     | 100,021 |
| Accuracy         |  73.36% |
| Benign recall    |    1.00 |
| Attack recall    |    0.34 |
| Attack precision |    1.00 |

### Confusion Matrix

Class order: BENIGN, ATTACK

| Actual / Predicted | BENIGN | ATTACK |
| ------------------ | -----: | -----: |
| BENIGN             | 59,943 |     57 |
| ATTACK             | 26,593 | 13,428 |

The cross-day test shows a substantial reduction in performance. In particular, the model missed many attacks in the held-out Friday data. This demonstrates why evaluation on different collection days is important for intrusion detection.

## 5. Multiclass Classification

The multiclass dataset contains 15 traffic categories. The dataset was divided using a stratified random train/test split.

The leave-one-day-out multiclass experiment did not produce valid evaluation results: each held-out day shared only the BENIGN class with the remaining training data. The script therefore skipped those splits.

This is a limitation of the available day-wise class distribution, not evidence that the model achieved zero accuracy.

## 6. Limitations

* The random-split results may overestimate generalization to unseen days.
* Cross-day testing revealed a high number of missed attacks.
* Some attack categories have very few samples, making their metrics unstable.
* The experiment uses selected CIC-IDS2017 CSV data and does not establish performance on live production traffic.
* Model confidence is not the same as a calibrated probability of correctness.

## 7. Conclusion

CloudSentinel AI demonstrates an end-to-end prototype for network-flow classification, batch prediction, and dashboard-based analysis. The evaluation highlights the difference between random-split performance and cross-day generalization.

Further work should focus on improving detection of attacks from unseen days, evaluating rare classes with sufficient data, and testing the system on additional datasets or live traffic.
