import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

# Page title
st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    max_value=300.0,
    value=65.0
)

height = st.number_input(
    "Height (m)",
    min_value=0.5,
    max_value=2.5,
    value=1.70
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    max_value=1000.0,
    value=10.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    options=[True, False]
)

city = st.text_input(
    "City",
    value="Mumbai"
)

occupation = st.selectbox(
    "Occupation",
    options=[
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)

# Prediction button
if st.button("Predict Premium Category"):

    # Prepare request payload
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        # API request
        response = requests.post(API_URL, json=input_data)

        # Convert response to JSON
        result = response.json()

        # Success case
        if response.status_code == 200:
            prediction = result["predicted_category"]

            st.success(
                f"Predicted Insurance Premium Category: **{prediction}**"
            )

            # Optional extra details
            bmi = weight / (height ** 2)
            st.info(f"Calculated BMI: **{bmi:.2f}**")

        # API error case
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    # Server connection issue
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Could not connect to the FastAPI server. Make sure the server is running."
        )

    # Invalid JSON / bad response
    except ValueError:
        st.error("❌ Received invalid response from server.")

    # Any other issue
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")