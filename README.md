# AI Phishing URL Detection System

This project detects whether a user-entered URL is phishing or legitimate using Machine Learning.

## Features
- Real URL input
- AI-based phishing prediction
- Confidence score
- URL lexical feature extraction
- Streamlit web interface

## Project Structure
- app.py -> Streamlit frontend
- src/feature_extractor.py -> extracts URL features
- src/train_model.py -> trains ML model
- src/predict.py -> prediction logic
- dataset/urls.csv -> training dataset
- models/ -> saved model files

## Run Steps

### 1. Create virtual environment
python -m venv venv

### 2. Activate environment
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Train model
python src/train_model.py

### 5. Run app
streamlit run app.py