"""
DataPulse-AI: Command-Line Interface (CLI Mode)
Executes automated statistical profiling and Gemini AI synthesis directly from terminal.
"""

import argparse
import os
import sys
import pandas as pd
from eda_engine import EDASummarizer
from gemini_copilot import generate_gemini_insights


def main():
    parser = argparse.ArgumentParser(
        description="DataPulse-AI: Scientific EDA & Autonomous Research Copilot"
    )
    parser.add_argument(
        "--data", "-d",
        type=str,
        default="sample_urban_data.csv",
        help="Path to CSV dataset (default: sample_urban_data.csv)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="gemini-2.5-flash",
        help="Gemini model name (default: gemini-2.5-flash)"
    )
    parser.add_argument(
        "--lang", "-l",
        type=str,
        choices=["en", "it"],
        default="en",
        help="Language for report: 'en' (English) or 'it' (Italiano)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="report_output.md",
        help="File path to save the generated markdown report"
    )

    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"[-] Error: File not found: {args.data}")
        sys.exit(1)

    print(f"\n[+] Loading dataset: {args.data}...")
    df = pd.read_csv(args.data)
    
    print("[+] Calculating statistical fingerprint (Mean, IQR, Skewness, Pearson r)...")
    summarizer = EDASummarizer(df)
    payload = summarizer.build_statistical_payload()

    overview = payload["overview"]
    print(f"    - Rows: {overview['total_rows']}, Columns: {overview['total_columns']}")
    print(f"    - Missing Values: {overview['total_missing_values']} ({overview['missing_percentage']}%)")

    top_corr = payload["top_correlations"]
    if top_corr:
        print("\n[+] Top Feature Correlations:")
        for c in top_corr[:3]:
            print(f"    • {c['feature_a']} <-> {c['feature_b']}: r = {c['pearson_r']}")

    print(f"\n[+] Invoking Google Gemini ({args.model}) in [{args.lang.upper()}] mode...")
    report = generate_gemini_insights(
        stats_payload=payload,
        dataset_name=os.path.basename(args.data),
        model_name=args.model,
        language=args.lang
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[✓] Research report generated and saved to: {args.output}")
    print("=" * 70)
    print(report[:600] + "\n...[Full report saved to file]...\n")


if __name__ == "__main__":
    main()
