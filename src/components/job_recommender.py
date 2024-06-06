import re
from ftfy import fix_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
from nltk.corpus import stopwords

# Load the NLTK stopwords
stopw = set(stopwords.words('english'))

# Load dataset:
jd_df = pd.read_csv(r'D:/ML_Projects/Job_Reccomendation_System/src/data/jd_structured_data.csv')

# Global variable to hold skills
skills = []

def set_skills(resume_skills):
    global skills
    if resume_skills:
        skills = [' '.join(word for word in resume_skills if word.lower() not in stopw)]
    else:
        skills = []

def ngrams(string, n=3):
    string = fix_text(string)  # fix text
    string = string.encode("ascii", errors="ignore").decode()  # remove non-ascii chars
    string = string.lower()
    chars_to_remove = [")", "(", ".", "|", "[", "]", "{", "}", "'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title()  # normalize case - capitalize the start of each word
    string = re.sub(' +', ' ', string).strip()  # get rid of multiple spaces and replace with a single
    string = ' ' + string + ' '  # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD', r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)

def getNearestN(queryTFIDF_, nbrs):
    distances, indices = nbrs.kneighbors(queryTFIDF_)
    return distances, indices

def recommend_jobs(user_location):
    global skills
    
    if not skills or all(word in stopw for word in skills):
        raise ValueError("No valid skills extracted. Please check the resume content.")
    
    # Create a single document with skills for TF-IDF vectorization
    skills_doc = [' '.join(skills)]
    tfidf = vectorizer.fit_transform(skills_doc)
    
    # Filter jobs by location
    filtered_jobs = jd_df[jd_df['Location'].str.contains(user_location, case=False, na=False)]
    if filtered_jobs.empty:
        return pd.DataFrame()
    
    # Transform job descriptions
    jd_test = filtered_jobs['Processed_JD'].values.astype('U')
    jd_tfidf = vectorizer.transform(jd_test)
    
    # Fit NearestNeighbors on job descriptions
    nbrs = NearestNeighbors(n_neighbors=min(len(filtered_jobs), 5), n_jobs=-1).fit(jd_tfidf)
    
    # Find nearest neighbors to the skills vector
    distances, indices = getNearestN(tfidf, nbrs)
    
    matches = []
    for i in range(len(indices[0])):
        match_info = {
            'Match confidence': round(distances[0][i], 2),
            'Job Title': filtered_jobs.iloc[indices[0][i]]['Job Title'],
            'Company Name': filtered_jobs.iloc[indices[0][i]]['Company Name'],
            'Location': filtered_jobs.iloc[indices[0][i]]['Location'],
            'Industry': filtered_jobs.iloc[indices[0][i]]['Industry'],
            'Sector': filtered_jobs.iloc[indices[0][i]]['Sector'],
            'Average Salary': filtered_jobs.iloc[indices[0][i]]['Average Salary']
        }
        matches.append(match_info)
    
    matches_df = pd.DataFrame(matches)
    
    return matches_df.drop_duplicates().sort_values('Match confidence').head(10)