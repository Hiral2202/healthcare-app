from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models
import datetime

def get_available_slots(db: Session, specialty: str = None, date: str = None):
    query = db.query(models.Slot).join(models.Doctor).filter(models.Slot.is_booked == 0)

    if specialty:
        query = query.filter(models.Doctor.specialty.ilike(f"%{specialty}%"))

    if date:
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(
                models.Slot.datetime.between(
                    datetime.datetime.combine(date_obj, datetime.time.min),
                    datetime.datetime.combine(date_obj, datetime.time.max)
                )
            )
        except ValueError:
            pass  # ignore invalid date

    return query.all()


def book_appointment(db: Session, patient_name: str, patient_email: str, patient_phone: str, slot_id: int):
    """
    Book an appointment for a patient, storing name, email, and phone number.
    """
    # Check if the slot is available
    slot = db.query(models.Slot).filter(
        models.Slot.id == slot_id, models.Slot.is_booked == 0
    ).first()
    if not slot:
        return None

    # Mark slot as booked
    slot.is_booked = 1

    # Create appointment record with phone number
    appointment = models.Appointment(
        patient_name=patient_name,
        patient_email=patient_email,
        patient_phone=patient_phone,  # <-- store phone
        slot_id=slot_id
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment
