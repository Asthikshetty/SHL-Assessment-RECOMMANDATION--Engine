from flask import Flask, request, jsonify
import model

app = Flask(__name__)
@app.route('/')
def home():
    return "SHL Assessment Recommender API is running!", 200

@app.route('/recommend', methods=['POST'])

def recommend():
    data = request.json
    job_role = data.get('job_role')
    skills = data.get('skills', '')
    
    if not job_role:
        return jsonify({"error": "job_role is required"}), 400
    
    recommendations = model.recommend_assessments(job_role, skills)
    return jsonify(recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
