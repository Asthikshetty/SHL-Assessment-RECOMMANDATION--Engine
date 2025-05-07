import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data.csv')

def load_model():
    try:
        # Load data and clean NaN values
        df = pd.read_csv(data_path)
        df = df.fillna('')  # Replace NaN with empty strings
        
        # Combine features safely
        df['features'] = df['job_role'] + ' ' + df['required_skills'] + ' ' + df['difficulty']
        
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['features'])
        
        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        return df, tfidf, tfidf_matrix, cosine_sim
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

# Load model components on module import
df, tfidf, tfidf_matrix, cosine_sim = load_model()

def recommend_assessments(job_role, skills=None, top_n=5):
    """
    Recommend assessments based on job role and skills
    
    Parameters:
    job_role (str): The job role to recommend assessments for
    skills (list or str): Skills required for the job
    top_n (int): Number of recommendations to return
    
    Returns:
    DataFrame: Top N recommended assessments
    """
    try:
        # Convert skills to string if it's a list
        if isinstance(skills, list):
            skills = ", ".join(skills)
        elif skills is None:
            skills = ""
            
        # Create query from job role and skills
        query = job_role + ' ' + skills
        logger.info(f"Processing query: {query}")
        
        # Transform query using TF-IDF
        query_vec = tfidf.transform([query])
        
        # Calculate similarity scores
        sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        # Get top-N indices
        top_indices = sim_scores.argsort()[-top_n:][::-1]
        
        # Return recommended assessments
        recommendations = df.iloc[top_indices][['assessment_id', 'assessment_name', 'difficulty']]
        logger.info(f"Found {len(recommendations)} recommendations")
        
        return recommendations
    except Exception as e:
        logger.error(f"Error in recommendation: {str(e)}")
        raise
