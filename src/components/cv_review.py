import re
from collections import Counter
import docx
import src.components.skills_extraction as skills_extraction
from src.data.job_generator import skills_dict
import PyPDF2

section_mapping = {
    # About me
    "About": "About me",
    "About Me": "About me",
    "Summary": "About me",
    "Personal Summary": "About me",
    "Profile": "About me",
    "Professional Summary": "About me",
    
    # Education
    "Education": "Education",
    "Educational Background": "Education",
    "Academic Background": "Education",
    "Academic History": "Education",
    "Academic Qualifications": "Education",
    "Educational Qualifications": "Education",
    
    # Professional Experience
    "Professional Experience": "Professional Experience",
    "Work Experience": "Professional Experience",
    "Employment History": "Professional Experience",
    "Career History": "Professional Experience",
    "Experience": "Professional Experience",
    
    # Organizational Experience
    "Organizational Experience": "Organizational Experience",
    "Organization Experience": "Organizational Experience",
    "Committee Experience": "Organizational Experience",
    "Committee Participation": "Organizational Experience",
    "Volunteer Experience": "Organizational Experience",
    "Volunteering": "Organizational Experience",
    
    # Projects
    "Projects": "Projects",
    "Project Experience": "Projects",
    "Project Work": "Projects",
    "Key Projects": "Projects",
    
    # Skills
    "Skills": "Skills",
    "Skill": "Skills",
    "Key Competencies": "Skills",
    "Competencies": "Skills",
    "Core Competencies": "Skills",
    "Technical Skills": "Skills",
    "Technical Competencies": "Skills",
    "Abilities": "Skills",
    "Expertise": "Skills",
    
    # Courses
    "Courses": "Courses",
    "Certifications": "Courses",
    "Training": "Courses",
    "Professional Development": "Courses",
    "Relevant Coursework": "Courses"
}


# Function to extract text from DOCX file
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to extract text from PDF file using PyPDF2
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text

# Function to extract keywords from the job position using jd_df and skills_dict
def extract_keywords_from_position(job_position):
    if job_position in skills_dict:
        skills_list_from_dict = skills_dict[job_position]
    else:
        skills_list_from_dict = []
    return [skill.lower() for skill in skills_list_from_dict]

def standardize_sections(resume_text):
    standardized_sections = {
        "About me": 0,
        "Education": 0,
        "Professional Experience": 0,
        "Organizational Experience": 0,
        "Projects": 0,
        "Skills": 0,
        "Courses": 0
    }
    
    for section, standard_name in section_mapping.items():
        if re.search(section, resume_text, re.IGNORECASE):
            standardized_sections[standard_name] = 1
    
    return standardized_sections

def review_cv(file_path, job_position):
    try:
        # Extract text from PDF or DOCX resume
        if file_path.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            return None, "Unsupported file format", set(), []

        # Extract keywords from the job position
        required_keywords = extract_keywords_from_position(job_position)
        
        # Extract skills from the resume text
        resume_skills = skills_extraction.skills_extractor(file_path)
        resume_keywords = [skill.lower() for skill in resume_skills]
        
        keyword_counts = Counter(resume_keywords)
        keyword_score = sum(keyword_counts[keyword] for keyword in required_keywords if keyword in keyword_counts)
        
        # Standardize section names
        standardized_sections = standardize_sections(resume_text)
        
        # Overall score
        total_score = sum(standardized_sections.values()) + keyword_score
        max_score = len(standardized_sections) + len(required_keywords)
        grade = (total_score / max_score) * 100
        
        # Identify missing skills
        missing_skills = set(required_keywords) - set(resume_keywords)
        
        return standardized_sections, grade, missing_skills, required_keywords
    
    except Exception as e:
        return None, str(e), set(), []
