# HealthAI: Clinical Decision Support System

A machine learning-based clinical decision support system for depression and suicide risk detection using Naive Bayes classification.

## Features

- **Flask REST API** - Backend prediction service on port 5000
- **Streamlit Web Interface** - User-friendly clinical notes analyzer on port 8501
- **Docker Containerization** - Easy deployment and reproducibility
- **Model Metrics** - Accuracy and F1 scores displayed during training
- **Safety Checks** - Minimum input length validation for clinical rigor

## Project Structure

```
backend/
├── main.py              # Flask API server
├── app.py               # Streamlit web interface
├── train.py             # Model training script
├── preprocess.py        # Data preprocessing
├── requirements.txt     # Python dependencies
├── DockerFile          # Docker container configuration
└── docker-compose.yml   # Docker compose setup

data/
├── Suicide_Detection.csv  # Dataset (download required)

tests/
└── tests_dependability.py # Unit tests
```

## Setup & Installation

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional)
- Git

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/SOUAH/HealthAI_Project.git
cd HealthAI_Project
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

4. **Download the Dataset**
   - Download `Suicide_Detection.csv` from [Kaggle](https://www.kaggle.com/datasets/nikhilesharma/suicide-watch)
   - Place it in the `data/` folder

5. Train the model:
```bash
python backend/train.py
```
Output will show: **Accuracy** and **F1 Score**

6. Run the Flask API:
```bash
python backend/main.py
```
API available at: `http://localhost:5000/predict`

7. Run Streamlit UI (in another terminal):
```bash
streamlit run backend/app.py
```
Web interface available at: `http://localhost:8501`

## Docker Setup

Build and run with Docker:
```bash
docker build -f backend/DockerFile -t healthai:latest .
docker run -d -p 5000:5000 --name healthai-container healthai:latest
```

Test the API:
```powershell
python -c "import requests; response = requests.post('http://localhost:5000/predict', json={'text': 'I have been feeling very depressed lately and struggling with my mental health...'}); print(response.json())"
```

## API Usage

**Endpoint:** `POST /predict`

**Request:**
```json
{
  "text": "I have been feeling very depressed lately and struggling with my mental health. I do not know how to cope with these overwhelming emotions anymore."
}
```

**Response:**
```json
{
  "status": "Success",
  "risk_label": "High Risk",
  "probability_score": 0.98,
  "disclaimer": "This is a decision signal for clinicians only. Not a diagnosis."
}
```

## Model Performance

- **Algorithm:** Multinomial Naive Bayes
- **Vectorizer:** TF-IDF (5000 features)
- **Train/Test Split:** 80/20

## Safety & Disclaimer

⚠️ **This tool is for clinical decision support only. It is NOT a substitute for professional medical diagnosis or treatment. Always consult qualified healthcare providers.**

## File Size Note

The dataset file (`data/Suicide_Detection.csv`) is 159 MB and is not included in the repository due to GitHub's file size limits. Download it separately and place it in the `data/` folder before training.

## Future Improvements

- [ ] Add more evaluation metrics (Precision, Recall, ROC-AUC)
- [ ] Implement cross-validation
- [ ] Add more clinical features
- [ ] Deploy to AWS/GCP
- [ ] Add authentication for healthcare settings

## License

This project is for educational and research purposes.

## Author

Souha Aouididi
