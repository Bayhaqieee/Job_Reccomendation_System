import re
from collections import Counter
import docx
import src.components.skills_extraction as skills_extraction


# Function to extract text from DOCX file
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_keywords_from_position(position, jd_df):
    position_skills = jd_df[jd_df['Position'] == position]['Skills'].values
    if position_skills:
        skills_list = position_skills[0].split(',')
        return [skill.strip() for skill in skills_list]
    return []

def review_cv(file_path, job_position, jd_df):
    try:
        # Extract text from PDF or DOCX resume
        if file_path.endswith('.pdf'):
            resume_text = skills_extraction.extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            return None, "Unsupported file format"
        
        # Extract keywords from the job position
        required_keywords = extract_keywords_from_position(job_position, jd_df)
        
        # Extract skills from resume
        resume_keywords = resume_text.split()
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

