"""Skill taxonomy. Each canonical skill maps to a list of aliases found in text.
Extend this dictionary to cover other domains (finance, HR, marketing, ...)."""

SKILLS = {
    # Languages
    "python": ["python"], "java": ["java"], "javascript": ["javascript", "js", "ecmascript"],
    "typescript": ["typescript"], "c++": ["c++"], "c#": ["c#"], "go": ["golang"],
    "r": ["r programming", "r language"], "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "t-sql"],
    "scala": ["scala"], "kotlin": ["kotlin"], "php": ["php"], "bash": ["bash", "shell scripting"],
    # ML / Data
    "machine learning": ["machine learning", "ml"], "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"], "computer vision": ["computer vision", "opencv"],
    "tensorflow": ["tensorflow"], "pytorch": ["pytorch", "torch"], "keras": ["keras"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "pandas": ["pandas"], "numpy": ["numpy"], "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data visualisation", "matplotlib", "seaborn", "plotly"],
    "statistics": ["statistics", "statistical analysis"], "spark": ["spark", "pyspark"],
    "hadoop": ["hadoop"], "tableau": ["tableau"], "power bi": ["power bi", "powerbi"],
    "excel": ["excel", "ms excel"], "llm": ["llm", "large language models", "generative ai", "gen ai"],
    "transformers": ["transformers", "hugging face", "huggingface", "bert"],
    # Web / Backend
    "react": ["react", "reactjs", "react.js"], "angular": ["angular"], "node.js": ["node.js", "nodejs", "node js"],
    "django": ["django"], "flask": ["flask"], "fastapi": ["fastapi"], "spring boot": ["spring boot", "springboot"],
    "html": ["html", "html5"], "css": ["css", "css3"], "rest api": ["rest api", "restful", "rest apis"],
    "graphql": ["graphql"], "microservices": ["microservices"],
    # Cloud / DevOps
    "aws": ["aws", "amazon web services"], "azure": ["azure"], "gcp": ["gcp", "google cloud"],
    "docker": ["docker"], "kubernetes": ["kubernetes", "k8s"], "git": ["git", "github", "gitlab"],
    "ci/cd": ["ci/cd", "cicd", "jenkins", "github actions"], "linux": ["linux", "unix"],
    "terraform": ["terraform"], "mlops": ["mlops"],
    # Databases
    "mongodb": ["mongodb", "mongo"], "redis": ["redis"], "elasticsearch": ["elasticsearch"],
    "nosql": ["nosql"], "kafka": ["kafka"],
    # Soft / process
    "agile": ["agile", "scrum"], "communication": ["communication"], "leadership": ["leadership", "team lead"],
    "problem solving": ["problem solving", "problem-solving"], "project management": ["project management"],
}
