"""
Gemini AI Principal Data Scientist Copilot.
Integrates Google Gemini models using the official google-genai SDK to generate
academic-grade statistical insights, anomaly diagnostics, and machine learning hypotheses.
"""

import json
import os
from typing import Optional

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


def build_eda_prompt(stats_payload: dict, dataset_name: str, language: str = "en") -> str:
    """Constructs an expert data scientist prompt from computed statistical metadata."""
    stats_json_str = json.dumps(stats_payload, indent=2)

    if language == "it":
        return f"""
Sei un Principal Data Scientist e Ricercatore Accademico presso una prestigiosa università (es. Politecnico di Milano, Università di Bologna).
Ti è stato fornito un profilo statistico approfondito del dataset: "{dataset_name}".

Ecco i metadati statistici calcolati in modo rigoroso (Descriptive stats, IQR Outliers, Pearson Correlations):
```json
{stats_json_str}
```

Genera un'analisi approfondita strutturata in sezioni con formato Markdown chiaro e professionale:
1. **Sintesi Esecutiva & Dinamiche dei Dati**: Spiega cosa rappresentano questi dati e le tendenze dominanti.
2. **Audit della Qualità dei Dati & Diagnosi delle Anomalie**: Analizza skewness, valori mancanti e gli outlier rilevati col metodo IQR. Quali sono le cause plausibili nel mondo reale?
3. **Analisi delle Relazioni & Correlazioni**: Interpreta i coefficienti di correlazione di Pearson più significativi. C'è multicollinearità o causalità implicita?
4. **Ipotesi di Machine Learning & Modellazione Predittiva**:
   - Quali modelli di ML consiglieresti (es. XGBoost, Random Forest, Ridge Regression)?
   - Quale variabile target avrebbe senso prevedere?
   - Quali passaggi di Feature Engineering suggerisci (es. normalizzazione logaritmica, lag temporali)?
5. **Conclusioni per la Ricerca Scientifica**: Implicazioni pratiche per politiche urbane o sostenibilità.

Mantieni un tono accademico, rigoroso e orientato alla ricerca scientifica.
"""

    return f"""
You are a Principal Data Scientist and Academic Researcher evaluating data for an advanced university laboratory.
You have been provided with an exhaustive statistical fingerprint of the dataset: "{dataset_name}".

Here is the rigorously computed statistical payload (Descriptive Statistics, IQR Outliers, Pearson Correlation Matrix):
```json
{stats_json_str}
```

Generate an academic-grade Exploratory Data Analysis & AI Research Report formatted cleanly in Markdown:
1. **Executive Summary & Domain Trends**: Synthesize the key phenomena reflected in the data dimensions and distributions.
2. **Data Quality Audit & Anomaly Diagnosis**: Scrutinize skewness values, missing ratios, and IQR-detected outliers. What real-world factors explain these anomalies?
3. **Correlation Dynamics & Interaction Analysis**: Interpret the highest magnitude Pearson correlations. Discuss physical/domain mechanisms and potential multicollinearity risks.
4. **Machine Learning Hypotheses & Modeling Strategy**:
   - Recommend 2-3 optimal ML architectures (e.g., Gradient Boosted Trees, Regularized Regression, Time-Series Decomposition).
   - Formulate ideal target features and validation strategies.
   - Propose specific Feature Engineering transforms (e.g., log-transforms for skewed features, interaction terms).
5. **Academic & Practical Research Takeaways**: Highlight how these insights impact real-world decision-making or scientific inquiry.

Maintain an authoritative, precise, and scientifically grounded tone suitable for university peer review.
"""


def generate_gemini_insights(
    stats_payload: dict,
    dataset_name: str = "Dataset",
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash",
    language: str = "en"
) -> str:
    """
    Calls the Google Gemini API using the modern google-genai SDK.
    Falls back gracefully to a mock research report if no API key is provided.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")

    if not key or not HAS_GENAI:
        # Fallback simulation for offline testing
        lang_title = "Rapporto di Analisi Statistica e Ricerca AI" if language == "it" else "Data Science & AI Research Report"
        overview = stats_payload.get("overview", {})
        top_corr = stats_payload.get("top_correlations", [])
        
        corr_summary = ", ".join([f"{c['feature_a']} ↔ {c['feature_b']} (r={c['pearson_r']})" for c in top_corr[:3]])

        return f"""### 🔬 {lang_title} *(Demonstration Mode)*

> **Notice:** Set your `GEMINI_API_KEY` to enable live inferences via Google Gemini (`{model_name}`).

#### 1. Executive Summary
The dataset **{dataset_name}** encapsulates **{overview.get('total_rows', 0)} observations** across **{overview.get('total_columns', 0)} multidimensional features**. 
Numeric distribution analysis indicates structured environmental and telemetry variability across recording intervals.

#### 2. Key Statistical Discoveries
- **Strongest Correlations:** {corr_summary or "Calculated via Pearson r"}.
- **Outlier Footprint:** IQR screening reveals localized peak excursions, suggesting transient real-world events (e.g. rush-hour traffic or temperature inversions).

#### 3. Recommended Machine Learning Pipeline
1. **Model:** LightGBM / XGBoost Regressor for multi-variable environmental forecasting.
2. **Feature Engineering:** Cyclic encoding for temporal features and StandardScaler normalization.
3. **Validation Strategy:** Stratified K-Fold or Time-Series Split to prevent temporal leakage.
"""

    prompt = build_eda_prompt(stats_payload, dataset_name, language=language)

    client = genai.Client(api_key=key)

    # Use generate_content on models service
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text
