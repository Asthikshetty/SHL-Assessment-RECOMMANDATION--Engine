import streamlit as st
import requests

st.title("SHL Assessment Recommender")

# Define API URL at the top
API_URL = "https://shl-assessment-recommandation-engine-2.onrender.com"

job_role = st.text_input("Job Role (e.g., Data Scientist)", "")
skills = st.text_input("Required Skills (comma-separated)", "")

if st.button("Recommend"):
    if job_role:
        try:
            # Send request to your Render API
            response = requests.post(
                f"{API_URL}/recommend",
                json={
                    "job_role": job_role,
                    "skills": [s.strip() for s in skills.split(",")] if skills else []
                }
            )
            response.raise_for_status()  # Raise exception for 4xx/5xx errors
            
            recommendations = response.json()
            st.table(recommendations)
            
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
    else:
        st.warning("Please enter a job role")
