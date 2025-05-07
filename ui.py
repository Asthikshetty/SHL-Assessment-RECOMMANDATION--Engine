import streamlit as st
import requests
import os
import json
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="📋",
    layout="wide"
)

# Define API URL - try to get from environment or use default
API_URL = os.environ.get('API_URL', 'http://localhost:5000')

# App title and description
st.title("SHL Assessment Recommender")
st.markdown("""
This application recommends SHL assessments based on job roles and required skills.
Enter your job role and skills below to get personalized assessment recommendations.
""")

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    job_role = st.text_input("Job Role (e.g., Data Scientist)", "")

with col2:
    skills = st.text_input("Required Skills (comma-separated)", "")

# Create a button to trigger recommendations
if st.button("Get Assessment Recommendations", type="primary"):
    if job_role:
        # Show spinner while loading
        with st.spinner("Finding the best assessments for you..."):
            try:
                # Prepare the request payload
                payload = {
                    "job_role": job_role,
                    "skills": [s.strip() for s in skills.split(",")] if skills else []
                }
                
                # Log the request for debugging (using st.write with expander instead of debug)
                with st.expander("Debug Info", expanded=False):
                    st.write(f"Sending request to {API_URL}/recommend")
                    st.write(f"Payload: {json.dumps(payload)}")
                
                # Send request to API
                response = requests.post(
                    f"{API_URL}/recommend",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    recommendations = response.json()
                    
                    if recommendations:
                        # Display recommendations as a dataframe with styling
                        st.subheader("Recommended Assessments")
                        df = pd.DataFrame(recommendations)
                        
                        # Rename columns for better display
                        df.columns = ["Assessment ID", "Assessment Name", "Difficulty Level"]
                        
                        # Apply styling based on difficulty
                        def style_difficulty(val):
                            color = {
                                'Easy': 'lightgreen',
                                'Medium': 'lightblue',
                                'Hard': 'lightsalmon'
                            }.get(val, 'white')
                            return f'background-color: {color}'
                        
                        # Display styled dataframe
                        st.dataframe(df.style.applymap(style_difficulty, subset=['Difficulty Level']), use_container_width=True)
                    else:
                        st.warning("No matching assessments found. Try different job role or skills.")
                else:
                    st.error(f"Error: API returned status code {response.status_code}")
                    st.error(f"Response: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error(f"Connection error: Could not connect to API at {API_URL}")
                st.info("Make sure the API server is running and accessible.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a job role")

# Add info about the API status
st.sidebar.title("Application Info")
try:
    health_check = requests.get(f"{API_URL}/health", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("API Status: Online")
    else:
        st.sidebar.warning("API Status: Issues Detected")
except:
    st.sidebar.error("API Status: Offline")

# Add some helpful information
st.sidebar.markdown("""
### About This App
This app uses machine learning to recommend assessments based on job roles and skills. 
The recommendations are powered by a TF-IDF vectorizer and cosine similarity algorithm.

### How It Works
1. Enter your job role
2. Add skills (optional)
3. Click "Get Assessment Recommendations"
4. Review the recommended assessments
""")
