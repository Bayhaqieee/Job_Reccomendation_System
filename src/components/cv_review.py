import re
from collections import Counter
import docx
import PyPDF2
import src.components.skills_extraction as skills_extraction
from src.data.job_generator import skills_dict

# Function to extract text from DOCX file
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to extract text from PDF file using PyPDF2
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        text = ''
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extract_text()
    return text

# Function to extract keywords from the job position using skills_dict
def extract_keywords_from_position(job_position):
    # Extract skills from skills_dict
    if job_position in skills_dict:
        skills_list = skills_dict[job_position]
    else:
        skills_list = []
    
    # Return lowercase skills
    return [skill.lower() for skill in skills_list]

def review_cv(file_path, job_position):
    try:
        # Extract text from PDF or DOCX resume
        if file_path.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            return None, "Unsupported file format"
        
        # Extract keywords from the job position
        required_keywords = extract_keywords_from_position(job_position)
        
        # Extract skills from the resume text
        resume_skills = skills_extraction.skills_extractor(file_path)
        resume_keywords = [skill.lower() for skill in resume_skills]
        
        keyword_counts = Counter(resume_keywords)
        keyword_score = sum(keyword_counts[keyword] for keyword in required_keywords if keyword in keyword_counts)
        
        # Standardize section names
        section_mapping = {
            "About": "About me",
            "Education": "Educations",
            "Professional Experience": "Professional Experience",
            "Organization Experience": "Organizational Experience",
            "Committee Experience": "Organizational Experience",
            "Projects": "Project",
            "Skill": "Skills",
            "Key Competencies": "Skills",
            "Courses": "Course"
        }
        
        standardized_sections = {}
        for section in section_mapping:
            if re.search(section, resume_text, re.IGNORECASE):
                standardized_sections[section_mapping[section]] = 1
            else:
                standardized_sections[section_mapping[section]] = 0
        
        # Overall score
        total_score = sum(standardized_sections.values()) + keyword_score
        max_score = len(section_mapping) + len(required_keywords)
        grade = (total_score / max_score) * 100
        
        return standardized_sections, grade
    
    except Exception as e:
        return None, str(e)

