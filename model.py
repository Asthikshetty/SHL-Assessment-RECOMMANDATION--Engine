import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.model_selection import train_test_split

# Load moimport pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data and clean NaN values
df = pd.read_csv('data.csv')
df = df.fillna('')  # Replace NaN with empty strings

# Combine features safely
df['features'] = df['job_role'] + ' ' + df['required_skills'] + ' ' + df['difficulty']

# Proceed with TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])

# Rest of your code...

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_assessments(job_role, required_skills, top_n=5):
    query = job_role + ' ' + required_skills
    query_vec = tfidf.transform([query])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    # Get top-N indices
    top_indices = sim_scores.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][['assessment_id', 'assessment_name', 'difficulty']]



# Split data into train/test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

def evaluate_model():
    precision_scores = []
    for _, row in test_df.iterrows():
        recommendations = recommend_assessments(row['job_role'], row['required_skills'])
        recommended_ids = recommendations['assessment_id'].tolist()
        true_id = row['assessment_id']
        precision = 1 if true_id in recommended_ids else 0
        precision_scores.append(precision)
    
    avg_precision = sum(precision_scores) / len(precision_scores)
    return avg_precision

print(f"Precision@5: {evaluate_model():.2f}")