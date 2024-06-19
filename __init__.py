import streamlit as st
import os
import pandas as pd
from src.components.job_recommender import set_skills, recommend_jobs
import src.components.skills_extraction as skills_extraction
from src.components.cv_review import review_cv


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
    uploaded_file = st.file_uploader("Upload your resume (PDF Format):", type=['pdf'])
    st.write("Make sure it's already in PDF and Text-Based file!")
    
    # Option to choose work preference
    work_preference = st.selectbox("Choose your work preference:", ["Work from Home", "Work from Office"])
    
    # Multiselect for office locations if 'Work from Office' is chosen
    if work_preference == "Work from Office":
        # Extract unique locations from the dataset
        user_location = st.multiselect("Pilih lokasi pekerjaan (Anda bisa memilih lebih dari satu):", jd_df['Location'].unique().tolist())
    else:
        user_location = ["Remote"]
    
    # Select job position for CV review
    job_position = st.selectbox("Pilih posisi pekerjaan yang Anda inginkan:", jd_df['Job Title'].unique().tolist())
    
    # Initialize location_specific_jobs to avoid UnboundLocalError
    location_specific_jobs = {}
    
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        if not os.path.exists("Resume"):
            os.makedirs("Resume")
        
        # Save the uploaded file to the uploads directory
        file_path = os.path.join("Resume", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            st.write("Dokumen berhasil diunggah!")
            
        # Review and grade the CV
        result = review_cv(file_path, job_position, jd_df)
        if result:
            section_scores, grade, missing_skills, required_keywords = result
            st.write("### CV Review:")
            # Display section scores as a list
            st.write(f"Sections found: {[key for key, value in section_scores.items() if value == 1]}")
            st.write(f"CV Grade: {grade:.2f}%")
            if missing_skills:
                st.write("### Skills you may want to pursue:")
                checkboxes = {}
                for skill in missing_skills:
                    checkboxes[skill] = st.checkbox(skill)

                # If any checkboxes are checked, increase the grade
                for skill, is_checked in checkboxes.items():
                    if is_checked:
                        grade += (1 / len(required_keywords)) * 100

                st.write(f"Updated CV Grade: {grade:.2f}%")
        else:
            st.warning("Tidak ada bagian yang ditemukan atau format CV tidak didukung.")
        
        # Process resume and recommend jobs
        if user_location:
            location_specific_jobs = process_resume(file_path, user_location)
        
        if not location_specific_jobs:
            st.warning("Tidak ada pekerjaan yang ditemukan untuk lokasi yang ditentukan.")
        else:
            # Display recommended jobs for each location
            for location, df_jobs in location_specific_jobs.items():
                st.write(f"#### Pekerjaan yang Direkomendasikan di {location}:")
                if df_jobs.empty:
                    st.write("Tidak ada pekerjaan yang ditemukan untuk lokasi ini.")
                else:
                    st.dataframe(df_jobs[['Job Title', 'Company Name', 'Location', 'Industry', 'Sector', 'Average Salary']])
        

# Run the Streamlit app
if __name__ == '__main__':
    main()

