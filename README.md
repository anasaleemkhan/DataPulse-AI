# 🔬 DataPulse-AI: Autonomous Exploratory Data Science & Multimodal Research Copilot

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![AI](https://img.shields.io/badge/Google%20Gemini-google--genai%20v3-orange.svg)
![Data Science](https://img.shields.io/badge/Data%20Science-EDA%20%7C%20Pearson%20r%20%7C%20IQR-green.svg)
![UI](https://img.shields.io/badge/UI-Streamlit%20%2B%20Plotly-red.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**DataPulse-AI** is an academic-grade Exploratory Data Analysis (EDA) engine and AI Research Copilot designed to automate rigorous statistical profiling on tabular datasets and generate executive machine learning hypotheses. Powered by Google's latest **Gemini Flash models** (`gemini-2.5-flash` / `gemini-1.5-flash`) via the modern `google-genai` SDK, it supports bilingual synthesis in **English** and **Italian**.

---

## 🏛️ Motivation & Academic Relevance (Italian University Applications)
Top European universities (such as *Politecnico di Milano*, *Sapienza Università di Roma*, *Politecnico di Torino*, and *Università di Bologna*) prioritize applicants who demonstrate:
1. **Mathematical & Statistical Foundations:** Not merely prompting LLMs, but computing distributions, quantiles, skewness, and interquartile ranges (IQR).
2. **Explainable AI (XAI) & Ethical Modeling:** Transparent anomaly detection and hypothesis generation grounded in real-world environmental or urban telemetry.
3. **Bilingual Academic Readiness:** Support for both English and Italian scientific reporting (`Rapporto di Analisi Dati e Ricerca`).

---

## 🌟 Key Features

- **Automated Statistical Fingerprint:** Computes central tendency, spread (std, IQR), skewness, and missingness metrics.
- **Robust IQR Outlier Auditing:** Mathematical boundary calculations ($Q_1 - 1.5 \times IQR$ and $Q_3 + 1.5 \times IQR$) to detect genuine telemetry anomalies.
- **Pearson Correlation Matrix:** Vectorized correlation modeling with automated detection of top linear dependencies and multicollinearity flags.
- **Interactive Plotly Visualizations:**
  - Dynamic Correlation Heatmap.
  - Empirical distribution histograms with marginal box plots.
  - Bi-variate scatter plots with Ordinary Least Squares (OLS) regression trendlines.
- **Gemini Copilot Synthesis (google-genai SDK):**
  - Synthesizes statistical fingerprints into peer-review-grade research briefs.
  - Proposes concrete ML architectures (XGBoost, Random Forest, Regularized Regression).
  - Outlines feature engineering roadmaps (log-transforms, cyclic temporal encoding).
  - Bilingual mode (**English** and **Italiano**).
- **Dual Execution Modes:** Web UI (`streamlit run app.py`) or Terminal CLI (`python cli.py`).

---

## 📁 Repository Architecture

```text
DataPulse-AI/
├── app.py                   # Interactive Streamlit Web Dashboard
├── cli.py                   # Terminal CLI for automated headless runs
├── eda_engine.py            # Mathematical & Statistical Profiling Engine
├── gemini_copilot.py        # Google Gemini Integration (google-genai SDK)
├── sample_urban_data.csv    # Real-world Italian Urban Air Quality & Climate Dataset
├── serve_website.py         # Zero-dependency local server for the showcase website
├── website/                 # Interactive Portfolio & Academic Showcase Website
│   ├── index.html           # Modern glassmorphism showcase UI with Chart.js
│   ├── css/style.css        # Academic dark research theme styling
│   └── js/                  # Interactive telemetry, terminal sim & bilingual reports
├── index.html               # Root redirect for GitHub Pages / static hosting
├── requirements.txt         # Production dependencies
├── .gitignore               # Clean repository tracking rules
└── README.md                # Research & project documentation
```

---

## 🛠️ Installation & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/anasaleemkhan/DataPulse-AI.git
cd DataPulse-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Set your Gemini API Key
Get a free API key at [Google AI Studio](https://aistudio.google.com/):
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Linux / macOS
export GEMINI_API_KEY="your-api-key-here"
```
*(You can also input your key directly into the Web UI sidebar).*

---

## 🚀 Execution

### A. Run Interactive Web Dashboard
```bash
streamlit run app.py
```
*Access in browser at `http://localhost:8501`.*

### B. Run in Terminal (CLI Mode)
```bash
# English analysis on sample data
python cli.py --data sample_urban_data.csv --lang en

# Italian analysis on sample data
python cli.py --data sample_urban_data.csv --lang it
```

### C. Run Portfolio & Showcase Website (For University / Job Applications)
```bash
# Launch the local web server with automatic browser launch
python serve_website.py
```
*Access in browser at `http://localhost:8000` (or double-click `website/index.html` directly in your file browser without needing any server).*

---

## 📄 Resume / CV Ready Snippet (For College Admissions)

```markdown
**DataPulse-AI — Autonomous Data Science & Academic Research Copilot** | *Python, Gemini API, Pandas, Plotly*
• Engineered an automated Exploratory Data Analysis (EDA) pipeline computing central tendencies, skewness, Pearson correlation matrices, and IQR-based outlier boundaries on urban environmental datasets.
• Integrated Google Gemini Flash models via the official `google-genai` SDK to transform statistical fingerprints into bilingual (EN/IT) research briefings with predictive ML hypotheses.
• Built an interactive analytical dashboard using Streamlit and Plotly featuring dynamic heatmaps, distribution plots with marginal boxplots, and OLS regression trendlines.
```

---

## 👤 Author
Developed by **Anas Saleem Khan**  
GitHub: [@anasaleemkhan](https://github.com/anasaleemkhan)

---

## 📜 License
Distributed under the [MIT License](LICENSE).
