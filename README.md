
# 🛡️ CloudSentinel AI
### AI-Powered Network Intrusion Detection System

CloudSentinel AI is a machine-learning-based network intrusion detection project that analyzes network traffic features to identify benign activity and potential cyberattacks.

The project uses the CIC-IDS2017 dataset and Random Forest classifiers to perform binary intrusion detection and multiclass attack classification. It also evaluates model performance on data from different days to investigate generalization to unseen traffic.

## 🎯 Project Objectives

- Detect benign and malicious network traffic.
- Classify traffic into 15 categories.
- Evaluate model performance using standard classification metrics.
- Compare random-split performance with cross-day evaluation.
- Provide a Streamlit dashboard for interactive analysis.

## 🧰 Technologies Used

- **Language:** Python
- **Machine Learning:** Scikit-learn, Random Forest
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Dashboard:** Streamlit
- **Model Storage:** Joblib
- **Development Environment:** VS Code

## 📊 Dataset

This project uses the CIC-IDS2017 MachineLearningCSV dataset.

The dataset contains network-flow features and labels representing benign traffic and different attack types.

The project uses prepared and sampled CSV datasets for model development and evaluation. The processed datasets are not identical to the original dataset distribution.

### Attack categories

The multiclass classifier supports 15 labels:

BENIGN, Bot, DDoS, DoS GoldenEye, DoS Hulk, DoS Slowhttptest, DoS slowloris, FTP-Patator, Heartbleed, Infiltration, PortScan, SSH-Patator, Web Attack Brute Force, Web Attack SQL Injection, and Web Attack XSS.

## 🧠 Models

### 1. Binary Classification

A Random Forest classifier predicts whether network traffic is BENIGN or ATTACK.

- Random Forest: 150 trees
- Class weighting: Balanced
- Random train/test split: 80/20
- Random-split accuracy: **99.92%**

### 2. Multiclass Classification

A Random Forest classifier predicts one of the 15 traffic categories.

- Random Forest: 150 trees
- Input features: 78
- Training samples: 89,808
- Testing samples: 22,452
- Random-split accuracy: **99.15%**

The multiclass evaluation includes precision, recall, F1-score, and a confusion matrix.

### 3. Cross-Day Binary Evaluation

To investigate generalization, the binary model was trained on selected source days and tested on Friday traffic.

- Training samples: 152,239
- Test samples: 100,021
- Test benign samples: 60,000
- Test attack samples: 40,021
- Accuracy: **73.36%**
- Attack recall: **0.34**

The cross-day test showed that performance was substantially lower than the random-split result. In particular, the model missed many attacks in the held-out traffic.

> **Important:** The random-split and cross-day results come from different evaluation setups. They should not be treated as directly equivalent measurements.

## 📈 Evaluation and Reports

Evaluation artifacts are available in the `reports/` directory:

- `CloudSentinel_AI_Final_Evaluation_Report.md`
- `multiclass_evaluation_report.txt`
- `model_evaluation_summary.md`
- `cross_day_confusion_matrix.png`
- `model_accuracy_comparison.png`
- `multiclass_feature_importance.png`

These files document model performance, classification errors, feature importance, and evaluation limitations.

## 🖥️ Dashboard

CloudSentinel AI includes a Streamlit dashboard for uploading network-traffic CSV files and viewing model predictions.

The dashboard displays model information and provides an interface for analyzing uploaded traffic.

### Run the dashboard

From the project root, activate the virtual environment and run:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run dashboard\app.py
```

Then open the local URL shown in the terminal, usually:

`http://localhost:8501`

The uploaded CSV must contain the network-flow features expected by the application.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CloudSentinel-AI
```

### 2. Create a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Create a `requirements.txt` file containing the packages used by the project, then run:

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run dashboard/app.py
```

## 📁 Project Structure

```text
CloudSentinel-AI/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   ├── cloudsentinel_binary_model.pkl
│   ├── cloudsentinel_crossday_model.pkl
│   └── cloudsentinel_multiclass_model.pkl
├── reports/
│   ├── CloudSentinel_AI_Final_Evaluation_Report.md
│   ├── multiclass_evaluation_report.txt
│   ├── cross_day_confusion_matrix.png
│   └── model_accuracy_comparison.png
├── src/
│   ├── train_cloudsentinel.py
│   ├── train_multiclass.py
│   ├── cross_day_validation.py
│   └── predict.py
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure above highlights the main project components; your repository may contain additional scripts and artifacts.*

## ⚠️ Limitations

- The prepared datasets use sampling and class caps, so their class distribution differs from the original CIC-IDS2017 dataset.
- Some attack categories have very few samples. For example, the multiclass test set contains only 2 Heartbleed samples, 4 SQL Injection samples, and 7 Infiltration samples. Metrics for these categories are therefore unstable.
- Random train/test splits can produce optimistic results when similar traffic appears in both sets.
- The cross-day experiment showed limited detection of attacks in the held-out data.
- The model has not been established as suitable for production security monitoring.
- Results may change when evaluated on independent datasets or live network traffic.

## 🚀 Future Work

- Improve detection of attacks from unseen traffic sources.
- Investigate false negatives and class-specific errors.
- Evaluate on additional independent datasets.
- Add prediction confidence and clear warnings to the dashboard.
- Improve data validation and handling of unseen attack categories.
- Explore deployment and monitoring options.

## 👨‍💻 Author

**Khaja Nawaz**  
B.Tech — Computer Science and Engineering (AI & ML)

## 📌 Disclaimer

CloudSentinel AI is an educational and experimental project. Its reported metrics apply to the specific datasets and evaluation procedures used in this project. They do not guarantee real-world intrusion detection performance.