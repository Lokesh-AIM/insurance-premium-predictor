from pydantic import BaseModel, EmailStr, AnyUrl, field_validator;
from typing import List, Dict, Optional;

class Patient(BaseModel):
    name: str
    age: int
    url: AnyUrl
    email: EmailStr
    weight: float
    married: Optional[bool] = False;
    contact: Dict[str, str]
    allergies: Optional[List[str]] = None

    @field_validator('email')
    @classmethod
    def valid_email(cls, value):
        valid_domain = ['hdfc.com', 'sbi.com', 'icici.com', 'scaler.com']
        domain_name = value.split('@')[-1]

        if(domain_name not in valid_domain):
            raise ValueError("Email not found!")
        
        return value;

    @field_validator('name')
    @classmethod
    def capital_name(cls, value):
        return value.upper();
        


    


def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.contact)
    print(patient.allergies)
    print("Inserted")


def update(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.contact)
    print(patient.allergies)
    print("Updated")


patient_info = {"name": "somu", "age": 32, "weight": 43, 'allergies': ['Peanut', 'Rose'], 'contact': {'phone': '3862302379652'}}

patient1 = Patient(**patient_info)

insert(patient1)

print(".            .")

update(patient1)