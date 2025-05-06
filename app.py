from flask import Flask, request, jsonify
import model
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "SHL Assessment Recommender API is running!", 200

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        job_role = data.get('job_role')
        skills = data.get('skills', '')
        
        if not job_role:
            return jsonify({"error": "job_role is required"}), 400
        
        # Convert comma-separated string to list if needed
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
            
        recommendations = model.recommend_assessments(job_role, skills)
        return jsonify(recommendations.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render-compatible port
    app.run(host='0.0.0.0', port=port, debug=False)  # Disable debug in production
