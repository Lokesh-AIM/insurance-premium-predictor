from fastapi import FastAPI, Path, HTTPException, Query;
from pydantic import BaseModel, field_validator, computed_field, Field;
from fastapi.responses import JSONResponse;
from typing import Annotated, Literal, Optional;
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=['Hari'])]
    age: Annotated[int, Field(..., gt=0, lt=150, description="Age of the patient", examples=['32'])]
    city: Annotated[str, Field(..., description="City of the patient", examples=['Pune'])]
    gender: Annotated[Literal['male','female', 'Other'], Field(...,  description="Gender of the patient", examples=['male','female'])]
    height: Annotated[float, Field(...,gt=0, description="Height of the patient in meter", examples=['1.53'])]
    weight: Annotated[float, Field(...,gt=0, description="Weight of the patient in kg", examples=['43.7'])]
   


class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female", 'Other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

    @computed_field
    @property
    def bmi(self)-> float:
        if self.weight is None or self.height is None:
            return None
        return round(self.weight/(self.height**2),2);

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.0:
            return "Underweight"
        elif self.bmi <= 25.0:
            return "Healthy"
        else:
            return "Overweight"

    
# adding data into JSON file
def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f, indent=4)

# Getting data form JSON
def load_data():
    try:    
        with open('patient.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return{};


@app.get("/")
def hello():
    return {'message': "Patient Manager"}

@app.get("/about")
def about():
    return {'message': "A fully functional app to manage patient records"}

@app.get('/view')
def view():
    allPatientData = load_data()
    return allPatientData


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="ID of the patient is required", examples=["P001"])):
    allPatientData = load_data()

    if(patient_id in allPatientData):
        return allPatientData[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found");

@app.get('/sort')
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of age, height, or weight"
), order: str = Query('asc', description="Sort in Asc or Desc order")):
    valid_fields =['age', 'height', 'weight'];

    if(sort_by not in valid_fields):
        raise HTTPException(status_code=400, detail= f'Invalid Field select from {valid_fields}')
    
    valid_order = ['asc', 'desc'];

    if (order not in valid_order):
        raise HTTPException(status_code=400, detail= f'Invalid way of sorting select from {valid_order}')
    

    allPatientdata = load_data()

    sorted_order = order == 'desc';

    sorted_data = sorted(allPatientdata.values(), key=lambda x: x.get(sort_by, 0), reverse=sorted_order)
    
    return sorted_data;


@app.post('/create')
def create(patient: Patient):
    # simply load data
    data = load_data()
    
    # if already patient exist
    if(patient.id in data):
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # add data
    data[patient.id] = patient.model_dump(exclude={'id'})

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully!'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate ):
    data = load_data()

    if(patient_id not in data):
         raise HTTPException(status_code=404, detail="Patient not found!")
     
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset = True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value;

    existing_patient_info['id'] = patient_id
    pydantic_patient_object = Patient(**existing_patient_info)
    
    existing_patient_info = pydantic_patient_object.model_dump(exclude='id')

    data[patient_id] = existing_patient_info;  

    save_data(data)

    return JSONResponse(status_code=200, content={'message':"Successfully Updated"})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if(patient_id not in data):
        raise HTTPException(status_code=404, detail="Patient not found!")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient Deleted successfully'})