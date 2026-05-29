# Insurance Premium Predictor

A Machine Learning-powered web application that predicts a user's insurance premium category based on health, lifestyle, and demographic information.

The project uses:

* FastAPI for backend APIs
* Streamlit for frontend UI
* Scikit-Learn Machine Learning model
* Pydantic for request validation and feature engineering

---

## Project Overview

Insurance companies determine premium categories based on several risk factors. This project automates that process using a trained Machine Learning model.

The application accepts user information such as:

* Age
* Height
* Weight
* Income
* Occupation
* Smoking Status
* City

and predicts the insurance premium category.

---

## Features

### User-Friendly Frontend

Built using Streamlit with an interactive form for collecting user information.

### FastAPI Backend

Provides REST APIs for prediction requests.

### Automated Feature Engineering

The backend automatically calculates:

* BMI (Body Mass Index)
* Lifestyle Risk
* Age Group
* City Tier

before sending data to the ML model.

### Data Validation

Uses Pydantic models to ensure valid user input.

### Machine Learning Prediction

Predicts the insurance premium category using a trained Scikit-Learn model.

---

## Tech Stack

| Technology   | Purpose              |
| ------------ | -------------------- |
| Python       | Programming Language |
| FastAPI      | Backend API          |
| Streamlit    | Frontend UI          |
| Scikit-Learn | Machine Learning     |
| Pandas       | Data Processing      |
| Pydantic     | Data Validation      |
| Uvicorn      | ASGI Server          |

---

## Project Structure

```text
insurance-premium-predictor/
│
├── app.py                 # FastAPI backend
├── frontend.py            # Streamlit frontend
├── model.pkl              # Trained ML model
├── requirements.txt       # Dependencies
│
├── patient.json           # Sample JSON data
├── pydantic_test.py       # Pydantic validation examples
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/insurance-premium-predictor.git

cd insurance-premium-predictor
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn app:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Run Frontend

Open another terminal:

```bash
streamlit run frontend.py
```

---

## Sample Input

```json
{
  "age": 30,
  "weight": 75,
  "height": 1.75,
  "income_lpa": 12,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

---

## Feature Engineering

The application automatically derives:

### BMI

```text
BMI = Weight / Height²
```

### Lifestyle Risk

* High Risk

  * Smoker
  * BMI > 30

* Medium Risk

  * Smoker OR BMI > 27

* Low Risk

  * Non-Smoker and Healthy BMI

### Age Groups

* Young
* Adult
* Middle
* Senior

### City Tier Classification

* Tier 1
* Tier 2
* Tier 3

---

## API Endpoint

### Predict Insurance Premium

```http
POST /predict
```

Request Body:

```json
{
  "age": 30,
  "weight": 75,
  "height": 1.75,
  "income_lpa": 12,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

Response:

```json
{
  "predicted_category": "Medium"
}
```

---

## Future Improvements

* Docker Support
* Cloud Deployment (AWS/GCP/Azure)
* User Authentication
* Prediction Probability Scores
* Model Monitoring Dashboard
* Database Integration

---

## Author

Lokesh

Built as a Machine Learning + FastAPI + Streamlit learning project.
