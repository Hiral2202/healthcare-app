from fastapi import FastAPI, Depends, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database, crud
from .email_utils import send_email, generate_appointment_email
from .sms_utils import send_sms

# Initialize app
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def show_slots(request: Request, specialty: str = None, date: str = None, db: Session = Depends(get_db)):
    slots = crud.get_available_slots(db, specialty, date)
    return templates.TemplateResponse(
        "slots.html",
        {"request": request, "slots": slots, "specialty": specialty or "", "date": date or ""}
    )

@app.post("/book", response_class=HTMLResponse)
def book_appointment(
    request: Request,
    background_tasks: BackgroundTasks,
    patient_name: str = Form(...),
    patient_email: str = Form(...),
    patient_phone: str = Form(...),  # <- Added phone input
    slot_id: int = Form(...),
    db: Session = Depends(get_db)
):
    if not patient_phone.startswith("+"):
        patient_phone = "+91" + patient_phone  # prepend India country code
    # Book appointment in the database with phone number
    appointment = crud.book_appointment(db, patient_name, patient_email, patient_phone, slot_id)

    if appointment:
        message = f"Appointment booked successfully for {patient_name}"

        # Prepare email content
        email_body = generate_appointment_email({
            "patient_name": patient_name,
            "contact_number": patient_phone,
            "appointment_time": appointment.slot.datetime,  # get actual slot time
            "doctor_name": appointment.slot.doctor.name,    # get doctor name from slot relationship
            "department": appointment.slot.doctor.specialty  # get department/specialty
        })

        # Send Email in background
        background_tasks.add_task(
            send_email,
            "Appointment Confirmation",
            patient_email,
            email_body
        )

        # Send SMS in background
        sms_text = f"Hello {patient_name}, your appointment is confirmed for {appointment.slot.datetime} with {appointment.slot.doctor.name}."
        background_tasks.add_task(
            send_sms,
            patient_phone,
            sms_text
        )

    else:
        message = "Slot already booked or invalid"

    slots = crud.get_available_slots(db)
    return templates.TemplateResponse(
        "slots.html",
        {"request": request, "slots": slots, "message": message}
    )
