First of all, this System will not be created without the help from Abbas Behrainwala!
[Original Repo](github.com/abbas99-hub/Job-Recommendation-System/tree/main)

# What is the Difference?

- My version simply implements a local server system using streamlit, but additional development will be accomplished soon!
- The dataset employed is being modified to my focus, since I found the latest repo that the dataset URL for web scraping is no longer working and the structure of the Glassdoor websites has been entirely changed, so I am changing the whole dataset to be able to be created with a generator within our demanded parameters. Currently, I am generating jobs dataset on Indonesian cities and Indonesian companies. (Indonesia Mentioned KRRRRAAAAHHHHHH 🇮🇩🇮🇩🇮🇩🦅🦅🦅🦅🔥🔥🔥)
- This system not only gives you recommendations based on your CV, but it will also advise positions depending on where you are now living; the system will require where city you are in / the closest you are to.
- I've added the streamlit styling folder (.streamlit), which you can freely change.
- Removing the web scrapping capability, as my current goal is to develop a job recommendation system as efficient and precise as possible.
- Fixing the Upload system, on Abbas repo, I discovered that the Upload system on the interface is not working and that the system needs to change the CV Path on a regular basis to read my CV, thus by adjusting the CV uploading system, the system can receive and read the cv without changing the system path.
- Removing some Unnecessary Folder needed for my system

## Additional Notes
- Please change the File Datapath on the Components or Double check your auto path changer by checking all file path
- You can change the dataset by utilizing the job dataset generator on components folder

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

## Machine Learning Techniques:
For providing personalized job recommendations, we use the TF-IDF (Term Frequency-Inverse Document Frequency) vectorization approach. This method relies heavily on the "job_recommender.py" component. It uses the scikit-learn library's TF-IDF vectorizer to convert job descriptions and user preferences into numerical feature vectors. These vectors capture the significance of each word in the papers, allowing the system to identify similar job prospects depending on user preferences. The Nearest Neighbors algorithm is then used to select the most appropriate job recommendations.

The skill extractor segment includes functions and utilities for extracting skills from PDF files using the Spacy library, as well as text processing and matching activities. These extracted skills can be analyzed and processed in the job suggestion system.

## Streamlit Application
To make the job recommendation system more accessible and user-friendly, we created the Streamlit application. Streamlit offers a simple web interface for users to upload their resumes. The program accepts user input, uses machine learning models, and provides the top-recommended jobs based on the user's preferences and previous data.

## Usage
To use the job recommendation system, follow the instructions below:

- Clone this repository: git clone <repository-url>
- Install the required dependencies: pip install -r requirements.txt
- Run the command: streamlit run __init__.py ( For Local Server )