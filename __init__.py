import streamlit as st
import os
from src.components.job_recommender import set_skills, recommend_jobs
import src.components.skills_extraction as skills_extraction

# Function to process the resume and recommend jobs
def process_resume(file_path):
    # Extract text from PDF resume
    resume_skills = skills_extraction.skills_extractor(file_path)
    
    # Set the skills in job_recommender
    set_skills(resume_skills)
    
    # Recommend jobs based on resume skills
    df_jobs = recommend_jobs()
    
    return df_jobs

# Streamlit app
def main():
    st.title("Job Recommendation App")
    st.write("Selamat datang di Aplikasi Rekomendasi Pekerjaan kami. Di sini, Anda dapat mengunggah resume Anda dalam format PDF dan kami akan mencocokkan keterampilan Anda dengan pekerjaan yang paling sesuai.")
    
    # File uploader
    uploaded_file = st.file_uploader("Pilih file resume Anda (format PDF):", type=['pdf'])
    
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        # Save the uploaded file to the uploads directory
        file_path = os.path.join("CVData", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process resume and recommend jobs
        df_jobs = process_resume(file_path)
        
        # Display recommended jobs as DataFrame
        st.write("### Pekerjaan yang Direkomendasikan:")
        st.dataframe(df_jobs[['Job Title', 'Company Name', 'Location', 'Industry', 'Sector', 'Average Salary (in Million)']])

# Run the Streamlit app
if __name__ == '__main__':
    main()
