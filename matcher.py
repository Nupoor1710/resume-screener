"""Scoring and ranking logic."""
from dataclasses import dataclass

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from parser import EDU_NAMES, parse_job_description, parse_resume, read_text


@dataclass
class Weights:
    skills: float = 0.50      # share of JD skills the candidate has
    similarity: float = 0.30  # TF-IDF cosine similarity of full text
    experience: float = 0.10  # years vs. JD minimum
    education: float = 0.10   # degree level vs. JD requirement

    def normalized(self):
        t = self.skills + self.similarity + self.experience + self.education or 1
        return Weights(self.skills / t, self.similarity / t, self.experience / t, self.education / t)


def _tfidf_scores(jd_text: str, resume_texts: list[str]) -> list[float]:
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True, token_pattern=r"(?u)\b[\w+#.]{2,}\b")
    m = vec.fit_transform([jd_text] + resume_texts)
    return cosine_similarity(m[0:1], m[1:]).ravel().tolist()


def screen(jd_text: str, resumes: list[tuple[str, str]], weights: Weights | None = None) -> pd.DataFrame:
    """resumes: list of (filename, text). Returns a ranked DataFrame."""
    w = (weights or Weights()).normalized()
    jd = parse_job_description(jd_text)
    sims = _tfidf_scores(jd_text, [t for _, t in resumes])

    rows = []
    for (fname, text), sim in zip(resumes, sims):
        r = parse_resume(text, fallback_name=fname.rsplit(".", 1)[0])
        matched = sorted(jd["skills"] & r["skills"])
        missing = sorted(jd["skills"] - r["skills"])
        skill_score = len(matched) / len(jd["skills"]) if jd["skills"] else 0.0
        sim_score = min(sim / 0.5, 1.0)  # raw cosine rarely exceeds ~0.5 for real resumes; rescale
        exp_score = 1.0 if jd["min_experience"] == 0 else min(r["experience_years"] / jd["min_experience"], 1.0)
        edu_score = 1.0 if jd["education_level"] == 0 else min(r["education_level"] / jd["education_level"], 1.0)

        total = (w.skills * skill_score + w.similarity * sim_score +
                 w.experience * exp_score + w.education * edu_score) * 100
        rows.append({
            "Candidate": r["name"], "File": fname, "Email": r["email"],
            "Match Score": round(total, 1),
            "Skill Match %": round(skill_score * 100, 1),
            "Text Similarity %": round(sim_score * 100, 1),
            "Experience (yrs)": r["experience_years"],
            "Education": EDU_NAMES[r["education_level"]],
            "Matched Skills": ", ".join(matched),
            "Missing Skills": ", ".join(missing),
            "Other Skills": ", ".join(sorted(r["skills"] - jd["skills"])),
        })

    df = pd.DataFrame(rows).sort_values("Match Score", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)
    df.attrs["jd_skills"] = sorted(jd["skills"])
    df.attrs["jd_min_experience"] = jd["min_experience"]
    df.attrs["jd_education"] = EDU_NAMES[jd["education_level"]]
    return df


def screen_files(jd_path: str, resume_paths: list[str], weights: Weights | None = None) -> pd.DataFrame:
    jd_text = read_text(jd_path)
    resumes = [(p.split("/")[-1], read_text(p)) for p in resume_paths]
    return screen(jd_text, resumes, weights)
