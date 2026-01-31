from pydantic import BaseModel
from typing import Optional

class DoctorCreate(BaseModel):
    full_name: str
    phone_number: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True

class PatientCreate(BaseModel):
    full_name : str
    tashxis : str
    adres : str
    doctor_id : int
    image : Optional[str] = None
    video: Optional[str] = None
 
class PatientResponse(PatientCreate):
    id: int

    class Config:
        from_attributes = True
