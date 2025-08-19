from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database, crud

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
def book_appointment(request: Request, patient_name: str = Form(...), patient_email: str = Form(...), slot_id: int = Form(...), db: Session = Depends(get_db)):
    appointment = crud.book_appointment(db, patient_name, patient_email, slot_id)
    if appointment:
        message = f"Appointment booked successfully for {patient_name}"
    else:
        message = "Slot already booked or invalid"
    slots = crud.get_available_slots(db)
    return templates.TemplateResponse("slots.html", {"request": request, "slots": slots, "message": message})
