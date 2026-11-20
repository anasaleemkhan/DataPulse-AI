"""
Automated Exploratory Data Analysis (EDA) & Statistical Profiling Engine.
Calculates statistical fingerprints, distribution metrics, outlier ratios,
and correlation structures for tabular datasets.
"""

import pandas as pd
import numpy as np


class EDASummarizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_df = df.select_dtypes(include=[np.number])
        self.categorical_df = df.select_dtypes(exclude=[np.number])

    def get_dataset_overview(self) -> dict:
        """Returns fundamental dataset dimensions and missing value telemetry."""
        total_cells = self.df.size
        missing_cells = int(self.df.isnull().sum().sum())
        missing_pct = round((missing_cells / total_cells) * 100, 2) if total_cells > 0 else 0

        return {
            "total_rows": int(len(self.df)),
            "total_columns": int(len(self.df.columns)),
            "numeric_columns": list(self.numeric_df.columns),
            "categorical_columns": list(self.categorical_df.columns),
            "total_missing_values": missing_cells,
            "missing_percentage": missing_pct,
            "memory_usage_kb": round(float(self.df.memory_usage().sum() / 1024), 2)
        }

    def get_descriptive_stats(self) -> dict:
        """Computes mean, std, quantiles, and skewness for numeric features."""
        stats = {}
        for col in self.numeric_df.columns:
            series = self.numeric_df[col].dropna()
            if len(series) == 0:
                continue

            q25 = float(series.quantile(0.25))
            q50 = float(series.median())
            q75 = float(series.quantile(0.75))
            iqr = q75 - q25
            skew = float(series.skew()) if len(series) > 2 else 0.0

            stats[col] = {
                "mean": round(float(series.mean()), 2),
                "std": round(float(series.std()), 2),
                "min": round(float(series.min()), 2),
                "25%": round(q25, 2),
                "median": round(q50, 2),
                "75%": round(q75, 2),
                "max": round(float(series.max()), 2),
                "skewness": round(skew, 2),
                "iqr": round(iqr, 2)
            }
        return stats

    def detect_outliers_iqr(self) -> dict:
        """Identifies outlier counts and bounds per numeric feature using the IQR method."""
        outliers = {}
        for col in self.numeric_df.columns:
            series = self.numeric_df[col].dropna()
            if len(series) < 4:
                continue

            q25 = series.quantile(0.25)
            q75 = series.quantile(0.75)
            iqr = q75 - q25
            lower_bound = q25 - (1.5 * iqr)
            upper_bound = q75 + (1.5 * iqr)

            outlier_mask = (series < lower_bound) | (series > upper_bound)
            outlier_count = int(outlier_mask.sum())
            outlier_pct = round((outlier_count / len(series)) * 100, 2)

            outliers[col] = {
                "outlier_count": outlier_count,
                "outlier_percentage": outlier_pct,
                "lower_threshold": round(float(lower_bound), 2),
                "upper_threshold": round(float(upper_bound), 2)
            }
        return outliers

    def get_correlation_matrix(self) -> pd.DataFrame:
        """Returns Pearson correlation matrix for numeric columns."""
        if len(self.numeric_df.columns) < 2:
            return pd.DataFrame()
        return self.numeric_df.corr().round(3)

    def extract_top_correlations(self, top_n: int = 5) -> list:
        """Identifies the strongest positive and negative linear relationships."""
        corr = self.get_correlation_matrix()
        if corr.empty:
            return []

        pairs = []
        cols = corr.columns
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                col1, col2 = cols[i], cols[j]
                val = corr.loc[col1, col2]
                if not np.isnan(val):
                    pairs.append((col1, col2, round(float(val), 3)))

        # Sort by absolute strength
        pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        return pairs[:top_n]

    def build_statistical_payload(self) -> dict:
        """Packages comprehensive statistical metadata for Gemini AI consumption."""
        return {
            "overview": self.get_dataset_overview(),
            "descriptive_statistics": self.get_descriptive_stats(),
            "outliers_iqr": self.detect_outliers_iqr(),
            "top_correlations": [
                {"feature_a": p[0], "feature_b": p[1], "pearson_r": p[2]}
                for p in self.extract_top_correlations(top_n=6)
            ]
        }
