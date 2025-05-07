# SHL Assessment Recommendation Engine

A recommendation system that suggests SHL assessments based on job roles and required skills.

## Overview

This application uses machine learning techniques (TF-IDF vectorization and cosine similarity) to recommend appropriate SHL assessments for specific job roles and skills. It consists of:

- A Flask backend API that processes recommendation requests
- A Streamlit frontend for user interaction
- A machine learning model built with scikit-learn

## Features

- Job role-based assessment recommendations
- Skill-based filtering and enhancement
- Interactive user interface
- RESTful API for integration with other systems

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Asthikshetty/SHL-Assessment-RECOMMANDATION--Engine.git
   cd SHL-Assessment-RECOMMANDATION--Engine
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running Locally

1. Start the Flask API:
   ```
   python app.py
   ```

2. In a separate terminal, start the Streamlit UI:
   ```
   streamlit run ui.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

### Running with Combined Dispatcher

Alternatively, you can use the dispatcher script to run both components:

```
python dispatcher.py
```

## API Endpoints

### `POST /recommend`

Recommends assessments based on job role and skills.

**Request Body:**
```json
{
  "job_role": "Data Scientist",
  "skills": ["Python", "Machine Learning", "Statistics"]
}
```

**Response:**
```json
[
  {
    "assessment_id": "A1",
    "assessment_name": "SHL Verbal Reasoning",
    "difficulty": "Medium"
  },
  ...
]
```

## Deployment

This application can be deployed on Render.com. See the [Deployment Guide](deployment_guide.md) for detailed instructions.

## Dataset

The application uses a CSV dataset with the following structure:

- `job_role`: Target job position
- `required_skills`: Skills needed for the job
- `assessment_id`: Unique identifier for the assessment
- `assessment_name`: Name of the SHL assessment
- `difficulty`: Difficulty level (Easy, Medium, Hard)

## Model

The recommendation engine uses:

- TF-IDF Vectorization to convert text features into numerical vectors
- Cosine Similarity to measure the similarity between job descriptions and assessments

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SHL for providing assessment frameworks
- scikit-learn for machine learning tools
- Streamlit for the interactive web interface
- ![image](https://github.com/user-attachments/assets/2db5358c-4f1e-40e5-a681-5c4a4af748fa)

