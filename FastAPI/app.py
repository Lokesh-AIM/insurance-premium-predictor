from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
from typing import Literal, Annotated
import pickle 
import pandas as pd


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


app = FastAPI()

class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=150, description="Age of the user", examples=['32'])]
    city: Annotated[str, Field(..., description="City of the user", examples=['Pune'])]
    height: Annotated[float, Field(...,gt=0, description="Height of the user in meter", examples=['1.53'])]
    weight: Annotated[float, Field(...,gt=0, description="Weight of the user in kg", examples=['43.7'])]
    income_lpa: Annotated[float, Field(..., gt=0, description='Income of user')]
    smoker: Annotated[bool, Field(..., description='Is the user smoker ot not?')]

    occupation: Annotated[Literal['retired',
    'freelancer',
    'student',
    'government_job',
    'business_owner',
    'unemployed', 
    'private_job'], Field(..., description='Occupation of the user')]
    


    @computed_field
    @property
    def bmi(self)-> float:
        if(self.height is None or self.weight is None):
            return None
        return self.weight/(self.height**2);

    @computed_field
    @property
    def lifestyle_risk(self)-> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return 'low'
        
    @computed_field
    @property
    def age_group(self) -> str:
        if(self.age < 25):
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle'
        else: 
            return 'senior'
        
    @computed_field
    @property
    def city_tier(self) -> int:
        tier_1_cities = [
            "Mumbai", "Delhi", "Bangalore", "Chennai",
            "Kolkata", "Hyderabad", "Pune"
        ]

        tier_2_cities = [
            "Jaipur", "Bhopal", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi",
            "Visakhapatnam", "Coimbatore", "Nagpur", "Vadodara", "Surat", "Rajkot",
            "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore",
            "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
            "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem",
            "Vijayawada", "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad",
            "Bareilly", "Aligarh", "Kozhikode", "Warangal", "Kolhapur",
            "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
        ]

        city = self.city.strip().title(); #handle spaace and case issue

        if city in tier_1_cities:
            return 1
        elif city in tier_2_cities:
            return 2
        else: 
            return 3

@app.post('/predict')
def predict_premium(data: UserInput):
        
        input_df = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_group,
            'income_lpa': data.income_lpa,
            'city_tier': data.city_tier,
            'occupation': data.occupation,
            'lifestyle_risk': data.lifestyle_risk
        }])
        

        prediction = model.predict(input_df)[0]


        return JSONResponse(status_code=200, content={'predicted_category': prediction})




