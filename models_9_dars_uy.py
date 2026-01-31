from typing import Optional
from sqlalchemy import String , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship
from database_9_dars_uy import Base

class Doctor(Base):
    __tablename__ = "doctor"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    full_name : Mapped[str] = mapped_column(String(50))
    phone_number : Mapped[Optional[str]] = mapped_column(String(13) , nullable=True)
    patient : Mapped[list["Patient"]] = relationship(back_populates="doctor")
        
class Patient(Base):
    __tablename__ = "patient"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    full_name : Mapped[str] = mapped_column(String(155))
    tashxis : Mapped[str] = mapped_column(String(255))
    adres : Mapped[Optional[str]] = mapped_column(nullable= True)
    doctor_id : Mapped[int] = mapped_column(ForeignKey("doctor.id"))
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    video: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    doctor : Mapped["Doctor"] = relationship(back_populates="patient")
    