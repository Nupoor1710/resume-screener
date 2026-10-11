"""Usage: python cli.py --jd job.txt --resumes resumes_folder [--top 5] [--out results.csv]"""
import argparse
from pathlib import Path

import pandas as pd

from matcher import screen_files

p = argparse.ArgumentParser(description="AI Resume Screening System (CLI)")
p.add_argument("--jd", required=True, help="Job description file (.txt/.pdf/.docx)")
p.add_argument("--resumes", required=True, help="Folder containing resumes")
p.add_argument("--top", type=int, default=10)
p.add_argument("--out", help="Save full results to CSV")
a = p.parse_args()

files = [str(f) for f in sorted(Path(a.resumes).iterdir()) if f.suffix.lower() in {".pdf", ".docx", ".txt"}]
df = screen_files(a.jd, files)
pd.set_option("display.width", 200)
print(f"\nJD skills detected: {', '.join(df.attrs['jd_skills'])}")
print(f"Min experience: {df.attrs['jd_min_experience']} yrs | Education: {df.attrs['jd_education']}\n")
print(df[["Rank", "Candidate", "Match Score", "Skill Match %", "Experience (yrs)", "Education"]].head(a.top).to_string(index=False))
if a.out:
    df.to_csv(a.out, index=False)
    print(f"\nSaved to {a.out}")
