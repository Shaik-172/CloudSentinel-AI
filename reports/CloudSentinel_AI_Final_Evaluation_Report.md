# CloudSentinel AI

## Final Model Evaluation Report

### 1. Project Overview

CloudSentinel AI is a machine-learning-based network intrusion detection project developed using the CIC-IDS2017 dataset. It uses network-flow features to distinguish benign traffic from malicious activity and to classify traffic into multiple attack categories.

The project uses Random Forest classifiers and evaluates performance using both random train-test splitting and a cross-day testing approach.

### 2. Dataset and Preparation

* **Dataset:** CIC-IDS2017 MachineLearningCSV
* **Features:** 78 network-flow features
* **Multiclass categories:** 15, including BENIGN and 14 attack categories
* **Preprocessing:** Cleaning and preparation of CSV data, handling invalid values, and creating training and testing datasets
* **Model:** Random Forest classifier

The multiclass dataset was prepared using a stratified random split with 80% of the data for training and 20% for testing.

### 3. Multiclass Model Results

The multiclass Random Forest model was evaluated on a held-out random test set.

| Metric            | Result |
| ----------------- | -----: |
| Test accuracy     | 99.15% |
| Number of classes |     15 |
| Training samples  | 89,808 |
| Testing samples   | 22,452 |
| Features          |     78 |

The classification report showed strong overall performance. The macro-average F1-score was approximately 0.91, while the weighted-average F1-score was approximately 0.99.

Some attack categories were harder to identify consistently. Web Attack XSS had a reported recall of 0.37, while Web Attack Brute Force had a recall of 0.73. The SQL Injection test class contained only four samples, so its reported metrics are highly uncertain.

### 4. Binary Cross-Day Evaluation

A separate binary experiment trained on data from earlier source days and tested on Friday traffic. This tests generalization across source days rather than randomly mixing traffic from the same days into both sets.

| Metric             |  Result |
| ------------------ | ------: |
| Cross-day accuracy |  73.36% |
| Test samples       | 100,021 |
| Benign samples     |  60,000 |
| Attack samples     |  40,021 |
| Attack recall      |    0.34 |
| Benign recall      |    1.00 |

The confusion matrix was:

| Actual / Predicted | BENIGN | ATTACK |
| ------------------ | -----: | -----: |
| BENIGN             | 59,943 |     57 |
| ATTACK             | 26,593 | 13,428 |

The model correctly identified 13,428 attack samples but missed 26,593 attacks in this test. This indicates that the model did not generalize equally well to the held-out Friday traffic, particularly for attack detection.

### 5. Interpretation

The 99.15% multiclass accuracy reflects performance on a stratified random test split drawn from the same prepared dataset. It should not be interpreted as proof of equivalent performance on unseen networks or future traffic.

The 73.36% binary cross-day accuracy provides a different and more challenging evaluation. The low attack recall shows that the model missed many attacks in the held-out data, despite identifying benign traffic very consistently.

These results demonstrate why evaluation design matters: random splitting and testing on a different source day measure different aspects of model performance.

### 6. Limitations

1. **Dataset limitations:** CIC-IDS2017 is a benchmark dataset and may not represent all real-world network environments.
2. **Random-split optimism:** Samples from similar source periods can appear in both training and test sets, potentially producing optimistic results.
3. **Cross-day generalization:** The binary cross-day test showed substantially lower attack recall than the random-split experiments.
4. **Rare attack categories:** Some multiclass categories have very few test examples. For example, SQL Injection had four test samples, making its metrics unstable.
5. **Sampling:** The prepared dataset uses capped sampling and does not preserve the original dataset's full class distribution.
6. **Deployment readiness:** The model has not yet been established as suitable for production security monitoring. Further validation on independent traffic is needed.

### 7. Conclusion

CloudSentinel AI demonstrates an end-to-end machine-learning workflow for network intrusion detection, including dataset preparation, model training, evaluation, feature analysis, and a Streamlit interface.

The multiclass model achieved 99.15% accuracy on a random test split. However, the separate binary cross-day experiment achieved 73.36% accuracy and 0.34 attack recall, highlighting a significant generalization challenge.

The project therefore demonstrates both the potential of machine learning for intrusion detection and the importance of testing models on data that differs from their training data.

### 8. Future Work

* Improve attack detection on unseen source days.
* Investigate class-specific errors and rare attack categories.
* Evaluate on additional independent datasets or network traffic.
* Add confidence scores and clearer warnings in the dashboard.
* Document the model's limitations before considering real-world deployment.

**Important:** The reported results apply to the specific prepared datasets and evaluation procedures described above. They are not a guarantee of real-world detection performance.
