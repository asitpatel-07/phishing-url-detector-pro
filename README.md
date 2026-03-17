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
# 🛡️ Advanced AI Phishing URL Detection System

An advanced **AI-powered Phishing URL Detection System** built using **Python, Streamlit, Machine Learning, SQLite, HTML/CSS, and Real-Time URL Analysis**.

This project allows users to enter a **real URL manually** and instantly checks whether it is **Legitimate, Suspicious, or Phishing** using:

- Machine Learning based prediction
- Suspicious feature extraction
- Real-time domain and HTTP checks
- Blacklist validation
- Risk scoring system
- Auto-blocking for high-risk URLs
- User/Admin authentication
- Scan history tracking
- Premium colorful dashboard UI

---

## 🚀 Features

### 🔍 Real-Time URL Scanning
- User can enter a **real website URL**
- System scans and predicts whether it is:
  - **Legitimate**
  - **Suspicious**
  - **Phishing**

### 🤖 AI / Machine Learning Detection
- Uses **Random Forest Classifier**
- Extracts multiple suspicious URL features
- Predicts phishing probability and legitimate probability

### 📊 Advanced Risk Analysis
- Risk score out of **100**
- Severity levels:
  - Low Risk
  - Medium Risk
  - High Risk

### 🌐 Real-Time Security Checks
- Domain resolve check
- HTTP status code check
- URL blacklist check

### ⛔ Auto Blocking System
- If suspicious risk is **85% or above**
- URL gets **temporarily blocked for 4 hours**
- Live countdown timer shows remaining block time

### 🧾 Scan History
- Saves scanned URLs into SQLite database
- User sees only their own scan history
- Admin can view all scan history
- Reset history options included

### 🔐 Authentication System
- Admin login
- User login
- User credential reveal challenge (math-based)
- Admin password change page (requires old password)

### 🎨 Premium UI
- Colorful cyber-style Streamlit dashboard
- Risk meter
- Confidence charts
- Fixed footer branding
- HTML report export

---

## 🧠 Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Matplotlib**
- **SQLite**
- **HTML / CSS**
- **JSON**
- **Machine Learning (Random Forest)**

---

## 📁 Project Structure

```bash
phishing-url-detector/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   ├── logo.png
│   └── styles.css
│
├── auth/
│   ├── __init__.py
│   ├── login.py
│   ├── password_utils.py
│   └── users.json
│
├── data/
│   ├── raw/
│   │   └── urls.csv
│   ├── processed/
│   │   └── cleaned_urls.csv
│   └── reports/
│       └── training_report.txt
│
├── database/
│   ├── app.db
│   └── init_db.py
│
├── models/
│   ├── phishing_model.pkl
│   ├── feature_columns.pkl
│   └── model_metrics.json
│
├── pages/
│   ├── 1_User_Scanner.py
│   ├── 2_Scan_History.py
│   ├── 3_Admin_Dashboard.py
│   ├── 4_Model_Insights.py
│   └── 5_Admin_Change_Password.py
│
├── src/
│   ├── __init__.py
│   ├── feature_extractor.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── predict.py
│   ├── blacklist_checker.py
│   ├── realtime_checks.py
│   ├── report_generator.py
│   ├── utils.py
│   └── block_manager.py
│
└── templates/
    ├── dashboard.html
    ├── report_template.html
    └── login_banner.html
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
