import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt


# ==========================================================
# CloudSentinel AI - Security Monitoring Dashboard v2
# ==========================================================

MODEL_PATH = (
    r"D:\CloudSentinel-AI\models"
    r"\cloudsentinel_multiclass_model.pkl"
)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="CloudSentinel AI",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================================
# Custom CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# Header
# ==========================================================

st.markdown(
    '<div class="main-title">🛡️ CloudSentinel AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Network Security Monitoring Center'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================================
# Load Model
# ==========================================================

@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)


try:

    model = load_model()

except Exception as e:

    st.error(f"Could not load model: {e}")
    st.stop()


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🛡️ CloudSentinel")

st.sidebar.markdown(
    """
    **Network Intrusion Detection**

    Upload a CIC-IDS2017-style CSV containing
    the 78 network-flow features used by the
    trained Random Forest model.
    """
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Network Traffic CSV",
    type=["csv"]
)


# ==========================================================
# No File Uploaded
# ==========================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a network traffic CSV from the sidebar "
        "to start CloudSentinel analysis."
    )

    st.markdown("## 🤖 Model Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Model",
            "Random Forest"
        )

    with col2:
        st.metric(
            "Classes",
            "15"
        )

    with col3:
        st.metric(
            "Features",
            "78"
        )

    with col4:
        st.metric(
            "Dataset",
            "CIC-IDS2017"
        )

    st.markdown("---")

    st.subheader("🔐 Supported Detection Classes")

    classes = [
        "BENIGN",
        "Bot",
        "DDoS",
        "DoS GoldenEye",
        "DoS Hulk",
        "DoS Slowhttptest",
        "DoS slowloris",
        "FTP-Patator",
        "Heartbleed",
        "Infiltration",
        "PortScan",
        "SSH-Patator",
        "Web Attack Brute Force",
        "Web Attack SQL Injection",
        "Web Attack XSS"
    ]

    class_text = " • ".join(classes)

    st.write(class_text)

    st.stop()


# ==========================================================
# Read CSV
# ==========================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(f"Could not read CSV: {e}")
    st.stop()


st.success(
    f"CSV loaded successfully — "
    f"{len(df):,} network flows detected."
)


# ==========================================================
# Prepare Features
# ==========================================================

try:

    # Remove target column if present
    if "Attack_Type" in df.columns:

        X = df.drop(
            columns=["Attack_Type"]
        )

    else:

        X = df.copy()

    # Remove non-feature columns
    columns_to_remove = [
        "Label",
        "Target",
        "Source_Day",
        "Predicted_Attack",
        "Confidence",
        "Status",
        "Risk"
    ]

    X = X.drop(
        columns=[
            col
            for col in columns_to_remove
            if col in X.columns
        ],
        errors="ignore"
    )

    # Required model features
    required_features = list(
        model.feature_names_in_
    )

    # Check missing features
    missing_features = [
        feature
        for feature in required_features
        if feature not in X.columns
    ]

    if missing_features:

        st.error(
            f"The uploaded CSV is missing "
            f"{len(missing_features)} required features."
        )

        st.write("Missing features:")

        st.write(missing_features)

        st.stop()

    # Correct feature order
    X = X[required_features]


except Exception as e:

    st.error(
        f"Feature preparation failed: {e}"
    )

    st.stop()


# ==========================================================
# Prediction
# ==========================================================

with st.spinner(
    "🔍 CloudSentinel is analyzing network traffic..."
):

    predictions = model.predict(X)

    probabilities = model.predict_proba(X)

    confidence = (
        np.max(probabilities, axis=1) * 100
    )


# ==========================================================
# Create Results
# ==========================================================

results = df.copy()

results["Predicted_Attack"] = predictions

results["Confidence"] = confidence

results["Status"] = np.where(
    results["Predicted_Attack"] == "BENIGN",
    "BENIGN",
    "ATTACK"
)


# ==========================================================
# Dashboard Statistics
# ==========================================================

total_flows = len(results)

attack_count = (
    results["Status"] == "ATTACK"
).sum()

benign_count = (
    results["Status"] == "BENIGN"
).sum()

attack_rate = (
    attack_count / total_flows * 100
    if total_flows > 0
    else 0
)

average_confidence = (
    results["Confidence"].mean()
    if total_flows > 0
    else 0
)

top_attack_series = (
    results[
        results["Status"] == "ATTACK"
    ]["Predicted_Attack"]
    .value_counts()
)

if len(top_attack_series) > 0:

    top_attack = top_attack_series.index[0]
    top_attack_count = top_attack_series.iloc[0]

else:

    top_attack = "None"
    top_attack_count = 0


# ==========================================================
# Main Metrics
# ==========================================================

st.markdown("---")

st.subheader("📡 Network Security Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "🌐 Total Flows",
        f"{total_flows:,}"
    )

with col2:

    st.metric(
        "🚨 Attacks",
        f"{attack_count:,}"
    )

with col3:

    st.metric(
        "✅ Benign",
        f"{benign_count:,}"
    )

with col4:

    st.metric(
        "📈 Attack Rate",
        f"{attack_rate:.2f}%"
    )

with col5:

    st.metric(
        "🎯 Avg Confidence",
        f"{average_confidence:.2f}%"
    )


# ==========================================================
# Top Attack Alert
# ==========================================================

if top_attack != "None":

    st.warning(
        f"🚨 Most frequently detected attack: "
        f"**{top_attack}** "
        f"({top_attack_count:,} flows)"
    )

else:

    st.success(
        "✅ No attack traffic detected."
    )


# ==========================================================
# Charts
# ==========================================================

st.markdown("---")

st.subheader("📊 Attack Distribution")

prediction_counts = (
    results["Predicted_Attack"]
    .value_counts()
)

st.bar_chart(
    prediction_counts,
    height=400
)


# ==========================================================
# Status Breakdown
# ==========================================================

st.subheader("🛡️ Traffic Status")

status_counts = (
    results["Status"]
    .value_counts()
)

col1, col2 = st.columns(2)

with col1:

    st.bar_chart(
        status_counts,
        height=300
    )

with col2:

    st.write("### Status Summary")

    status_df = pd.DataFrame({
        "Status": status_counts.index,
        "Flows": status_counts.values
    })

    status_df["Percentage"] = (
        status_df["Flows"]
        / total_flows
        * 100
    )

    st.dataframe(
        status_df,
        hide_index=True,
        use_container_width=True
    )


# ==========================================================
# Confidence Distribution
# ==========================================================

st.markdown("---")

st.subheader("🎯 Model Confidence Distribution")

confidence_bins = pd.cut(
    results["Confidence"],
    bins=[
        0,
        50,
        70,
        90,
        100
    ],
    labels=[
        "<50%",
        "50–70%",
        "70–90%",
        "90–100%"
    ],
    include_lowest=True
)

confidence_counts = (
    confidence_bins
    .value_counts()
    .sort_index()
)

st.bar_chart(
    confidence_counts,
    height=300
)


# ==========================================================
# Attack Filter
# ==========================================================

st.markdown("---")

st.subheader("🔎 Prediction Explorer")

available_predictions = sorted(
    results["Predicted_Attack"]
    .unique()
)

selected_attack = st.selectbox(
    "Filter by predicted class",
    ["All"] + available_predictions
)


if selected_attack == "All":

    filtered_results = results.copy()

else:

    filtered_results = results[
        results["Predicted_Attack"]
        == selected_attack
    ].copy()


# ==========================================================
# Prediction Table
# ==========================================================

display_columns = []

if "Attack_Type" in filtered_results.columns:

    display_columns.append(
        "Attack_Type"
    )

display_columns.extend(
    [
        "Predicted_Attack",
        "Confidence",
        "Status"
    ]
)

st.write(
    f"Showing "
    f"**{len(filtered_results):,}** "
    f"matching flows."
)

st.dataframe(
    filtered_results[
        display_columns
    ].head(500),
    hide_index=True,
    use_container_width=True
)


# ==========================================================
# Download Results
# ==========================================================

st.markdown("---")

st.subheader("📥 Export Analysis")

csv_data = results.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Complete Prediction Results",
    data=csv_data,
    file_name="cloudsentinel_predictions.csv",
    mime="text/csv"
)


# ==========================================================
# Model Information
# ==========================================================

st.markdown("---")

with st.expander(
    "ℹ️ About the CloudSentinel AI Model"
):

    st.write(
        """
        CloudSentinel AI uses a Random Forest classifier
        trained on CIC-IDS2017 network-flow data.

        The multiclass model identifies 15 traffic categories
        using 78 network-flow features.

        The model's confidence represents the maximum
        class probability returned by the Random Forest.
        It should not be interpreted as a formally validated
        cybersecurity risk score.
        """
    )


# ==========================================================
# Footer
# ==========================================================

st.markdown("---")

st.caption(
    "CloudSentinel AI • AI-Powered Network Intrusion Detection"
)
# ==========================================
# MODEL EVALUATION & PERFORMANCE
# ==========================================

from pathlib import Path

st.divider()

st.header("📊 Model Evaluation & Performance")

st.write(
    "Explore CloudSentinel AI's evaluation results, "
    "including its cross-day confusion matrix and "
    "random-split versus cross-day accuracy."
)

# Locate the reports folder from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"

confusion_matrix_path = (
    REPORTS_DIR / "cross_day_confusion_matrix.png"
)

accuracy_chart_path = (
    REPORTS_DIR / "model_accuracy_comparison.png"
)

# Display evaluation charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cross-Day Confusion Matrix")

    if confusion_matrix_path.exists():
        st.image(
            str(confusion_matrix_path),
            use_container_width=True
        )
    else:
        st.warning("Confusion matrix image not found.")

with col2:
    st.subheader("Accuracy Comparison")

    if accuracy_chart_path.exists():
        st.image(
            str(accuracy_chart_path),
            use_container_width=True
        )
    else:
        st.warning("Accuracy comparison image not found.")

st.caption(
    "Note: Random-split and cross-day results use "
    "different evaluation setups. Random-split "
    "accuracy may overestimate performance on "
    "unseen network traffic."
)