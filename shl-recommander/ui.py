import streamlit as st
import requests

st.title("SHL Assessment Recommender")

job_role = st.text_input("Job Role (e.g., Data Scientist)", "")
skills = st.text_input("Required Skills (comma-separated)", "")

if st.button("Recommend"):
    if job_role:
        response = requests.post(
            "http://localhost:5000/recommend",
            json={"job_role": job_role, "skills": skills}
        )
        if response.status_code == 200:
            recommendations = response.json()
            st.table(recommendations)
        else:
            st.error("Error fetching recommendations")
    else:
        st.warning("Please enter a job role")