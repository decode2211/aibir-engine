"""
ML Engine for skill extraction from resumes
"""

def extract_skills_from_text(text: str):
    """
    Extract technical skills from resume text
    Returns list of detected skills
    """
    text_lower = text.lower()
    
    # Comprehensive skill list
    all_skills = [
        # Programming Languages
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "swift", "kotlin",
        "ruby", "php", "scala", "r", "matlab", "sql", "bash", "powershell",
        
        # Web Technologies
        "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask",
        "fastapi", "spring", "spring boot", "asp.net", "next.js", "nuxt.js", "gatsby",
        
        # Databases
        "mysql", "postgresql", "mongodb", "redis", "cassandra", "elasticsearch", "dynamodb",
        "oracle", "sqlite", "firebase", "mariadb",
        
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible",
        "ci/cd", "git", "github", "gitlab", "bitbucket", "linux", "nginx", "apache",
        
        # Data Science & ML
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras", "scikit-learn",
        "pandas", "numpy", "matplotlib", "seaborn", "opencv", "nlp", "computer vision",
        "data analysis", "data science", "ai", "neural networks",
        
        # Mobile Development
        "android", "ios", "react native", "flutter", "xamarin", "swift", "kotlin",
        
        # Other Technologies
        "rest api", "graphql", "microservices", "websockets", "oauth", "jwt",
        "agile", "scrum", "jira", "testing", "unit testing", "integration testing"
    ]
    
    detected = []
    for skill in all_skills:
        if skill in text_lower:
            detected.append(skill.title())
    
    # Remove duplicates and return
    return list(dict.fromkeys(detected))
