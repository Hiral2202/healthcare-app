from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    slots = relationship("Slot", back_populates="doctor")

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    datetime = Column(DateTime, nullable=False)
    is_booked = Column(Integer, default=0)  # 0 = available, 1 = booked
    doctor = relationship("Doctor", back_populates="slots")
    appointments = relationship("Appointment", back_populates="slot")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    patient_email = Column(String, nullable=False)
    patient_phone = Column(String, nullable=False)   # <-- ADD THIS LINE
    slot_id = Column(Integer, ForeignKey("slots.id"))
    booked_at = Column(DateTime, default=datetime.datetime.utcnow)
    slot = relationship("Slot", back_populates="appointments")
