from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models, database

def seed_data():
    db: Session = next(database.get_db())

    # Check if doctors already exist
    if db.query(models.Doctor).first():
        print("Data already exists. Skipping seeding.")
        return

    # 1️⃣ Add doctors
    doctors = [
        models.Doctor(name="Dr. Alice Smith", specialty="Cardiology"),
        models.Doctor(name="Dr. Bob Johnson", specialty="Neurology"),
        models.Doctor(name="Dr. Clara Lee", specialty="Dermatology")
    ]
    db.add_all(doctors)
    db.commit()

    # 2️⃣ Add slots for each doctor (next 5 days, 2 slots per day)
    for doctor in doctors:
        for day in range(1, 6):  # next 5 days
            for hour in [10, 15]:  # 10 AM and 3 PM
                slot_time = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=day)
                slot = models.Slot(doctor_id=doctor.id, datetime=slot_time)
                db.add(slot)
    db.commit()
    print("Doctors and slots seeded successfully.")

if __name__ == "__main__":
    seed_data()
