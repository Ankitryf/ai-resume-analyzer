import spacy
from typing import List, Dict, Tuple
import re
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from io import BytesIO

# Load spacy model
nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PdfReader(BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(BytesIO(file_content))
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")

    @staticmethod
    def parse_resume(file_content: bytes, filename: str) -> str:
        """Parse resume file and extract text"""
        if filename.endswith('.pdf'):
            return ResumeParser.extract_text_from_pdf(file_content)
        elif filename.endswith('.docx'):
            return ResumeParser.extract_text_from_docx(file_content)
        else:
            raise ValueError("Unsupported file format")

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract resume sections"""
        sections = {
            "Contact": "",
            "Summary": "",
            "Experience": "",
            "Education": "",
            "Skills": "",
            "Projects": "",
            "Certifications": ""
        }
        
        section_keywords = {
            "Contact": ["contact", "email", "phone", "address"],
            "Summary": ["summary", "objective", "professional"],
            "Experience": ["experience", "employment", "work history"],
            "Education": ["education", "degree", "university"],
            "Skills": ["skills", "technical", "proficiencies"],
            "Projects": ["projects", "portfolio"],
            "Certifications": ["certifications", "certificates"]
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower()
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    current_section = section
                    break
            
            if current_section:
                sections[current_section] += line + "\n"
        
        return sections

class KeywordExtractor:
    COMMON_SKILLS = [
        # Programming Languages
        "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin",
        "go", "rust", "typescript", "scala", "r", "matlab", "perl", "groovy",
        
        # Web Frameworks
        "react", "angular", "vue.js", "django", "flask", "spring", "fastapi", "node.js",
        "express", "laravel", "ruby on rails", "asp.net",
        
        # Databases
        "sql", "mysql", "postgresql", "mongodb", "cassandra", "redis", "elasticsearch",
        "oracle", "sqlserver", "dynamodb", "firestore",
        
        # DevOps & Tools
        "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "aws", "azure",
        "gcp", "terraform", "ansible", "ci/cd", "linux", "bash", "shell",
        
        # Data Science
        "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "scikit-learn",
        "pandas", "numpy", "matplotlib", "seaborn", "jupyter",
        
        # Cloud
        "aws", "azure", "gcp", "cloud", "serverless", "lambda",
        
        # Other
        "rest api", "graphql", "microservices", "agile", "scrum", "jira",
        "confluence", "slack", "communication", "problem-solving", "teamwork"
    ]
    
    @staticmethod
    def extract_skills(text: str) -> Tuple[List[str], List[str]]:
        """Extract present and identify missing skills from resume"""
        text_lower = text.lower()
        present_skills = []
        
        for skill in KeywordExtractor.COMMON_SKILLS:
            if skill in text_lower:
                if skill not in present_skills:
                    present_skills.append(skill)
        
        return present_skills

    @staticmethod
    def extract_keywords(text: str, job_description: str) -> Tuple[List[str], List[str]]:
        """Extract matching and missing keywords"""
        doc = nlp(text.lower())
        job_doc = nlp(job_description.lower())
        
        # Extract entities and noun chunks from job description
        job_keywords = set()
        for token in job_doc:
            if token.pos_ in ["NOUN", "PROPN"]:
                job_keywords.add(token.text)
        
        for chunk in job_doc.noun_chunks:
            job_keywords.add(chunk.text)
        
        # Find matching keywords in resume
        matching = []
        missing = []
        
        for keyword in job_keywords:
            if keyword in text.lower():
                matching.append(keyword)
            else:
                missing.append(keyword)
        
        return matching, missing

class ATSScorer:
    @staticmethod
    def calculate_score(
        resume_text: str,
        job_description: str,
        keyword_matches: List[str],
        total_keywords: int,
        present_skills: List[str],
        total_required_skills: int
    ) -> float:
        """Calculate ATS score based on multiple factors"""
        
        # Keyword matching score (40%)
        if total_keywords > 0:
            keyword_score = (len(keyword_matches) / total_keywords) * 100
        else:
            keyword_score = 0

        # Skill matching score (40%)
        required_skills = KeywordExtractor.extract_skills(job_description)
        matched_skills = [
            s for s in required_skills
            if s in present_skills
        ]
        skill_score = (
            len(matched_skills)
            / max(1, len(required_skills))
        ) * 100

        # Format score (20%)
        format_score = ATSScorer.evaluate_format(resume_text)

        # Calculate weighted score
        ats_score = (keyword_score * 0.4) + (skill_score * 0.4) + (format_score * 0.2)

        return round(min(100, max(0, ats_score)), 2)

    @staticmethod
    def evaluate_format(text: str) -> float:
        """Evaluate resume format for ATS compatibility"""
        score = 100
        
        # Deduct points for problematic content
        problematic_patterns = [
            (r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", 5),  # URLs
            (r"[^\x00-\x7F]", 2),  # Non-ASCII characters
            (r"<[^>]+>", 5),  # HTML tags
            (r"\b(?:image|chart|graph|photo)\b", 3),  # Image references
        ]
        
        for pattern, deduction in problematic_patterns:
            if re.search(pattern, text):
                score -= deduction
        
        return max(0, min(100, score))
