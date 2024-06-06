First of all, this System will not be created without the help from Abbas Behrainwala!
Visit his Original Repo Here!

github.com/abbas99-hub/Job-Recommendation-System/tree/main

# What is the Difference?

- My version simply implements a local server system using streamlit, but additional development will be accomplished soon!
- The dataset employed is being modified to my focus, since I found the latest repo that the dataset URL for web scraping is no longer working and the structure of the Glassdoor websites has been entirely changed, so I am changing the whole dataset to be able to be created with a generator within our demanded parameters. Currently, I am generating jobs dataset on Indonesian cities and Indonesian companies. (Indonesia Mentioned KRRRRAAAAHHHHHH 🇮🇩🇮🇩🇮🇩🦅🦅🦅🦅🔥🔥🔥)
- This system not only gives you recommendations based on your CV, but it will also advise positions depending on where you are now living; the system will require where city you are in / the closest you are to.
- I've added the streamlit styling folder (.streamlit), which you can freely change.
- Removing the web scrapping capability, as my current goal is to develop a job recommendation system as efficient and precise as possible.
- Fixing the Upload system, on Abbas repo, I discovered that the Upload system on the interface is not working and that the system needs to change the CV Path on a regular basis to read my CV, thus by adjusting the CV uploading system, the system can receive and read the cv without changing the system path.
- Removing some Unnecessary Folder needed for my system

## Job Recommendation System using Machine Learning
This repository contains the code and instructions to build a job recommendation system using machine learning. The system is designed to provide personalized job recommendations based on user preferences and historical job data.

## Business Understanding
The goal of this project is to develop a job recommendation system that helps users find relevant job opportunities based on their preferences and historical data. By leveraging machine learning techniques, we aim to provide personalized recommendations that align with the user's skills, interests, and career goals. The system will take into account various factors such as job title, salary estimate, company rating, location, industry, and more to generate accurate recommendations.

## Data Generating
To collect the necessary data for training our recommendation system, we will generate some job-related information from Library (can be integrated with Data Scraping Later). The following columns will be extracted:

- Job Title
- Estimated Salary
- Job Description
- Rating
- Company Name
- Location
- Headquarters
- Size
- Founded
- Type of Ownership
- Industry
- Sector
- Revenue
- Competitors