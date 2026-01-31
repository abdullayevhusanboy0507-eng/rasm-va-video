from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from models_9_dars_uy import *
from schemas_9_dars_uy import * 
from fastapi import UploadFile
from pathlib import Path
import shutil
from database_9_dars_uy import Media_dir
async def create_doctor(doctor : DoctorCreate , db : AsyncSession) -> DoctorResponse:
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    return DoctorResponse.model_validate(db_doctor)
    
async def reads_doctor(db : AsyncSession) -> list[DoctorResponse]:
    db_doctor = await db.execute(select(Doctor))
    return [DoctorResponse.model_validate(Doctor) for doctor in db_doctor.scalars().all()]

async def read_doctor(doctor_id : int , db: AsyncSession) -> DoctorResponse:
    db_doctor = await db.get(Doctor, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404 , detail="Doctor not faund")
    return DoctorResponse.model_validate(db_doctor)

async def update_doctor(doctor_id : int , doctor : DoctorCreate , db:AsyncSession) -> DoctorResponse:
    db_doctor = await db.get(Doctor, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404 , detail="Doctor not faund")
    for key , value in doctor:
        setattr(db_doctor , key , value)
    
    await db.commit()
    await db.refresh(db_doctor)
    return DoctorResponse.model_validate(db_doctor)

async def delete_doctor(doctor_id : int , db : AsyncSession) -> dict:
    db_doctor = await db.get(Doctor, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404 , detail="Doctor not faund")
    
    await db.delete(db_doctor)
    await db.commit()
    return {"message": "Doctor deleted successful"}


async def create_patient(patient : PatientCreate , db : AsyncSession, image: UploadFile = None ,video : UploadFile = None) -> PatientResponse:
    if image:
        image_extension = image.filename.lower().split(".")[-1]
        if image_extension not in ["jpg","jpeg","png"]:
            raise HTTPException(status_code=400 , detail="JPG  PNG yuklang")
    if video:
        video_extension = video.filename.lower().split(".")[-1]
        if video_extension not in ["mp4"]:
            raise HTTPException(status_code=400 , detail="mp4 yuklang")

    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    
    if image:
        image_path = Path(Media_dir) / f"patient_{db_patient.id}_image.{image_extension}"
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file , buffer)
        db_patient.image = str(image_path)
    
    if video:
        video_path = Path(Media_dir) / f"patient_{db_patient.id}_video.{video_extension}"
        with video_path.open("wb") as buffer:
            shutil.copyfileobj(video.file , buffer)
        db_patient.video = str(video_path)
    
    await db.commit()
    await db.refresh(db_patient)   
    return PatientResponse.model_validate(db_patient)
    
    
async def reads_patient(db : AsyncSession) -> list[PatientResponse]:
    db_patient = await db.execute(select(Patient))
    return [PatientResponse.model_validate(Patient) for patient in db_patient.scalars().all()]

