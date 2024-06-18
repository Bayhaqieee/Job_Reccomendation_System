import streamlit as st
import os
from src.components.job_recommender import set_skills, recommend_jobs
import src.components.skills_extraction as skills_extraction
import pandas as pd

# Load dataset
jd_df = pd.read_csv('D:/ML_Projects/Job_Reccomendation_System/src/data/jd_structured_data.csv')

# Function to process the resume and recommend jobs
def process_resume(file_path, user_locations):
    if not file_path:
        return {}

    # Extract text from PDF resume
    resume_skills = skills_extraction.skills_extractor(file_path)
    
    if not resume_skills:
        st.warning("No skills extracted from the resume. Please check the document.")
        return {}
    
    # Set the skills in job_recommender
    set_skills(resume_skills)
    
    # Recommend jobs based on resume skills and locations
    location_specific_jobs = {}
    for location in user_locations:
        df_jobs = recommend_jobs(location)
        location_specific_jobs[location] = df_jobs
    
    return location_specific_jobs

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
    
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        if not os.path.exists("Resume"):
            os.makedirs("Resume")
        
        # Save the uploaded file to the uploads directory
        file_path = os.path.join("Resume", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            st.write("Dokumen berhasil diunggah!")
        
        # Process resume and recommend jobs
        location_specific_jobs = process_resume(file_path, user_location)
        
        if not location_specific_jobs:
            st.warning("Yuk tambahin lagi kemungkinan lokasi kerjamu! Soalnya ngga ada pekerjaan yang ditemukan untuk lokasi yang ditentukan.")
        else:
            # Display recommended jobs for each location
            for location, df_jobs in location_specific_jobs.items():
                st.write(f"### Pekerjaan yang Direkomendasikan di {location}:")
                if df_jobs.empty:
                    st.write("Tidak ada pekerjaan yang ditemukan untuk lokasi ini.")
                else:
                    st.dataframe(df_jobs[['Job Title', 'Company Name', 'Location', 'Industry', 'Sector', 'Average Salary']])
        

# Run the Streamlit app
if __name__ == '__main__':
    main()

