"""
DataPulse-AI: Autonomous Data Science & Research Copilot
Built with Streamlit, Plotly, Pandas, and Google Gemini API (google-genai).
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from eda_engine import EDASummarizer
from gemini_copilot import generate_gemini_insights

# Configure Streamlit Page
st.set_page_config(
    page_title="DataPulse-AI | Academic Data Science Copilot",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .report-card {
        background: #F9FAFB;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: #EFF6FF;
        color: #1D4ED8;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔬 DataPulse-AI")
st.sidebar.caption("Autonomous EDA & Academic Research Engine")

# Dataset Source Selection
data_source = st.sidebar.radio(
    "Choose Dataset",
    ["🇮🇹 Italian Urban Climate & Air Quality (Sample)", "📂 Upload Custom CSV"]
)

if data_source == "🇮🇹 Italian Urban Climate & Air Quality (Sample)":
    sample_path = os.path.join(os.path.dirname(__file__), "sample_urban_data.csv")
    df = pd.read_csv(sample_path)
    dataset_title = "Italian Urban Air Quality & Climate (Milano, Bologna, Torino, Roma)"
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        dataset_title = uploaded_file.name
    else:
        st.info("Please upload a CSV file or switch back to the sample dataset.")
        st.stop()

# Gemini AI Settings
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Google Gemini Settings")

api_key = st.sidebar.text_input(
    "Google Gemini API Key",
    value=os.environ.get("GEMINI_API_KEY", ""),
    type="password",
    help="Get a free API key at https://aistudio.google.com/"
)

model_choice = st.sidebar.selectbox(
    "Gemini Model",
    ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-4-hydrogen"],
    index=0
)

report_lang = st.sidebar.selectbox(
    "Report Language / Lingua del Rapporto",
    ["English", "Italiano"],
    index=0
)
lang_code = "it" if report_lang == "Italiano" else "en"

# Main Application Title
st.title("🔬 DataPulse-AI: Scientific EDA & Machine Learning Copilot")
st.write(f"Analyzing: **{dataset_title}** | High-precision exploratory data modeling powered by Google Gemini.")

# Initialize Statistical Summarizer
summarizer = EDASummarizer(df)
stats_payload = summarizer.build_statistical_payload()
overview = stats_payload["overview"]

# Top Metrics Row
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Records", f"{overview['total_rows']:,}")
m2.metric("Features", f"{overview['total_columns']}")
m3.metric("Numeric Features", f"{len(overview['numeric_columns'])}")
m4.metric("Categorical Features", f"{len(overview['categorical_columns'])}")
m5.metric("Missing Rate", f"{overview['missing_percentage']}%")

# Main Dashboard Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Statistical Fingerprint",
    "📈 Interactive Analytics & Distributions",
    "🧠 Gemini AI Research Copilot"
])

# TAB 1: Statistical Fingerprint
with tab1:
    st.subheader("📋 Dataset Inspection")
    st.dataframe(df.head(10), use_container_width=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("📐 Descriptive Statistics (Mean, Median, Skewness, IQR)")
        desc_df = pd.DataFrame(stats_payload["descriptive_statistics"]).T
        st.dataframe(desc_df, use_container_width=True)

    with col_right:
        st.subheader("🚨 IQR Outlier Audit")
        outliers_df = pd.DataFrame(stats_payload["outliers_iqr"]).T
        st.dataframe(outliers_df, use_container_width=True)

# TAB 2: Interactive Analytics & Visualizations
with tab2:
    st.subheader("🔥 Pearson Correlation Heatmap")
    corr_df = summarizer.get_correlation_matrix()

    if not corr_df.empty:
        fig_corr = px.imshow(
            corr_df,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            labels=dict(color="Pearson r"),
            title="Correlation Heatmap of Numeric Features"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.subheader("📊 Feature Distribution Histogram")
        if overview["numeric_columns"]:
            sel_num_col = st.selectbox("Select Numeric Feature for Distribution", overview["numeric_columns"], index=0)
            fig_hist = px.histogram(
                df,
                x=sel_num_col,
                nbins=20,
                marginal="box",
                title=f"Empirical Distribution & Outliers: {sel_num_col}",
                color_discrete_sequence=["#2563EB"]
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    with col_v2:
        st.subheader("📉 Bi-Variate Scatter Relationship")
        if len(overview["numeric_columns"]) >= 2:
            x_col = st.selectbox("X-Axis Feature", overview["numeric_columns"], index=0)
            y_col = st.selectbox("Y-Axis Feature", overview["numeric_columns"], index=min(1, len(overview["numeric_columns"])-1))
            
            color_target = overview["categorical_columns"][0] if overview["categorical_columns"] else None
            fig_scatter = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=color_target,
                trendline="ols",
                title=f"{x_col} vs {y_col} with OLS Regression Trendline"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

# TAB 3: Gemini AI Copilot
with tab3:
    st.subheader("🧠 Autonomous Academic Research Report (Google Gemini)")
    st.markdown("""
    This section executes an academic synthesis by piping the computed statistical fingerprint,
    skewness properties, and correlation structures directly into Google's latest **Gemini Flash** architecture.
    """)

    btn_label = "Genera Rapporto Scientifico con Gemini AI 🚀" if lang_code == "it" else "Generate Scientific Research Report with Gemini AI 🚀"

    if st.button(btn_label, type="primary"):
        with st.spinner("Executing statistical reasoning with Google Gemini..."):
            try:
                report = generate_gemini_insights(
                    stats_payload=stats_payload,
                    dataset_name=dataset_title,
                    api_key=api_key,
                    model_name=model_choice,
                    language=lang_code
                )
                st.session_state["cached_report"] = report
            except Exception as e:
                st.error(f"Error communicating with Gemini API: {str(e)}")

    if "cached_report" in st.session_state:
        st.markdown(st.session_state["cached_report"])
        st.markdown("---")
        st.download_button(
            label="📥 Download Research Report (.md)",
            data=st.session_state["cached_report"],
            file_name=f"DataPulse_Research_Report_{lang_code}.md",
            mime="text/markdown"
        )
