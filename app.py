import logging
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import model

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Root endpoint to check if API is running"""
    return jsonify({
        "status": "online",
        "message": "SHL Assessment Recommendation API is running",
        "endpoints": {
            "/recommend": "POST - Get assessment recommendations"
        }
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    """Endpoint to get assessment recommendations"""
    try:
        # Get and validate request data
        data = request.json
        logger.info(f"Received request data: {data}")
        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        # Extract parameters from request
        job_role = data.get('job_role')
        skills = data.get('skills', '')
        
        if not job_role:
            return jsonify({"error": "job_role is required"}), 400
        
        # Process request and get recommendations
        try:
            recommendations = model.recommend_assessments(job_role, skills)
            return jsonify(recommendations.to_dict(orient='records'))
        except Exception as model_error:
            logger.error(f"Model error: {str(model_error)}")
            return jsonify({"error": "Model processing failed", "details": str(model_error)}), 500
            
    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port)
