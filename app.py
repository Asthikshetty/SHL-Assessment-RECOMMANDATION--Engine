import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import model
import os

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        app.logger.info(f"Received request data: {data}")  # Log input
        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        job_role = data.get('job_role')
        skills = data.get('skills', '')
        
        if not job_role:
            return jsonify({"error": "job_role is required"}), 400
        
        # Convert skills to list
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
        
        app.logger.info(f"Processing job_role={job_role}, skills={skills}")
        
        # Add error handling for model
        try:
            recommendations = model.recommend_assessments(job_role, skills)
        except Exception as model_error:
            app.logger.error(f"Model error: {str(model_error)}")
            return jsonify({"error": "Model processing failed"}), 500
            
        return jsonify(recommendations.to_dict(orient='records'))
    
    except Exception as e:
        app.logger.error(f"API error: {str(e)}", exc_info=True)  # Log full traceback
        return jsonify({"error": "Internal server error"}), 500
