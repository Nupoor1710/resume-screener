# AI Resume Screening System

Ranks resumes against a job description using NLP + rule-based information extraction.

## How it works
1. **Read** resumes/JD (PDF, DOCX, TXT).
2. **Extract** skills (taxonomy in `skills.py`), education level, years of experience, name, email.
3. **Score** each candidate (0-100):
   `0.5 × skill match + 0.3 × TF-IDF cosine similarity + 0.1 × experience + 0.1 × education`
   (weights adjustable in the UI).
4. **Rank** and show matched / missing skills for every candidate.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py                       # web UI
python cli.py --jd sample_data/job_description.txt --resumes sample_data/resumes   # CLI
```

## Files
| File | Purpose |
|---|---|
| `skills.py` | Skill taxonomy + aliases |
| `parser.py` | File reading + extraction |
| `matcher.py` | Scoring & ranking |
| `app.py` / `cli.py` | Streamlit UI / command line |

## Ideas to extend
- Swap TF-IDF for sentence-transformer embeddings (`all-MiniLM-L6-v2`).
- Mark JD skills as *required* vs *nice-to-have* with different weights.
- Use spaCy NER for names/organizations; add OCR for scanned PDFs.
