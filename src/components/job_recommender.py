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
    skills = [' '.join(word for word in resume_skills)]

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

nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1)

def getNearestN(query):
    queryTFIDF_ = vectorizer.transform(query)
    distances, indices = nbrs.kneighbors(queryTFIDF_)
    return distances, indices

def recommend_jobs():
    global skills
    tfidf = vectorizer.fit_transform(skills)
    nbrs.fit(tfidf)
    jd_test = jd_df['Processed_JD'].values.astype('U')
    
    distances, indices = getNearestN(jd_test)
    matches = [{'Match confidence': round(distances[i][0], 2)} for i in range(len(indices))]
    matches = pd.DataFrame(matches)
    
    # Following recommends Top 5 Jobs based on candidate resume:
    jd_df['match'] = matches['Match confidence']
    
    return jd_df.head(10).sort_values('match')
