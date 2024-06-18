import streamlit as st
import os
from src.components.job_recommender import set_skills, recommend_jobs
import src.components.skills_extraction as skills_extraction
import pandas as pd

# Load dataset
jd_df = pd.read_csv('D:/ML_Projects/Job_Reccomendation_System/src/data/jd_structured_data.csv')

# Function to process the resume and recommend jobs
def process_resume(file_path, user_location):
    # Extract text from PDF resume
    resume_skills = skills_extraction.skills_extractor(file_path)
    
    # Set the skills in job_recommender
    set_skills(resume_skills)
    
    # Recommend jobs based on resume skills and location
    df_jobs = recommend_jobs(user_location)
    
    return df_jobs

# Streamlit app
def main():
    st.title("Job Recommendation App")
    st.write("Upload Your CV to be analyzed!")
    
    # File uploader
    uploaded_file = st.file_uploader("Pilih file resume Anda (format PDF):", type=['pdf'])
    st.write("Pastiin formatmu dokumenmu PDF dan Text-Based yaa!")
    
    # Extract unique locations
    location = jd_df['Location'].unique().tolist()
    
    # Address input using multiselect
    user_location = st.multiselect("Pilih lokasi pekerjaan (Anda bisa memilih lebih dari satu):", location)
    
    if uploaded_file is not None and user_location:
        # Create uploads directory if it doesn't exist
        if not os.path.exists("Resume"):
            os.makedirs("Resume")
        
        # Save the uploaded file to the uploads directory
        file_path = os.path.join("Resume", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            st.write("Dokumen berhasil diunggah!")
        
        # Process resume and recommend jobs
        df_jobs = process_resume(file_path, user_location)
        
        if df_jobs.empty:
            st.warning("Tidak ada pekerjaan yang ditemukan untuk lokasi yang ditentukan.")
        else:
            # Display recommended jobs as DataFrame
            st.write("### Pekerjaan yang Direkomendasikan:")
            st.dataframe(df_jobs[['Job Title', 'Company Name', 'Location', 'Industry', 'Sector', 'Average Salary']])

# Run the Streamlit app
if __name__ == '__main__':
    main()

