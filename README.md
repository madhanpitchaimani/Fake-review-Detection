# Fake Review Detection

An Integrated Approach to projecting the credibility of online reviews using Machine Learning (Random Forest) and deep linguistic feature extraction.

## 🚀 Features
- **Integrated Machine Learning Approach**: Combines behavioral evidence with 6 IEEE linguistic signatures (Readability, Subjectivity, Internal Consistency, Rating Inconsistency, etc.).
- **URL Scanning**: Simulates an extraction pipeline to review products from links.
- **Explainable AI (SHAP)**: Identifies exactly *why* a review was flagged as fake or genuine.

---

## 🛠️ How to Run the Project

This project uses a **Python (FastAPI)** backend and a **React** frontend. You will need to run both in separate terminal windows.

### 1. Start the Backend API (FastAPI)

Open your first terminal and run the following commands from the root of the project:

```bash
# 1. Install all required Python dependencies
pip install -r requirements.txt

# 2. Run the FastAPI server
python api/main.py
```
*The backend API will start running at **http://localhost:8000**.*
*(Note: You can view the API documentation by visiting `http://localhost:8000/docs` in your browser).*

---

### 2. Start the Frontend Application (React)

Open a **second** new terminal and run the following commands from the root of the project:

```bash
# 1. Navigate to the frontend app directory
cd frontend-app

# 2. Install all required Node dependencies
npm install

# 3. Start the Vite development server
npm run dev
```
*The React Dashboard will open in your browser, typically at **http://localhost:5173**.*

---

## 📂 Project Structure
* `api/` - The FastAPI backend, including the model inference scripts (`main.py`)
* `data/` - Datasets and data parsing scripts 
* `models/` - Saved state dictionaries, scalers, and `.pkl` Random Forest models
* `frontend-app/` - The React Vite application containing the dashboard UI
* `scripts/` - Additional utility scripts

