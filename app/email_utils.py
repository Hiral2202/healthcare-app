# email_utils.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get environment variables
MAIL_USERNAME = os.getenv("EMAIL_USER")
MAIL_PASSWORD = os.getenv("EMAIL_PASS")

if not MAIL_USERNAME or not MAIL_PASSWORD:
    raise ValueError("EMAIL_USER and EMAIL_PASS must be set in .env")

MAIL_FROM = MAIL_USERNAME

# Configure FastAPI-Mail (Pydantic v2 compliant)
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,    # correct field
    MAIL_SSL_TLS=False,    # correct field
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(subject: str, recipient_email: str, body: str):
    """
    Send an email using FastAPI-Mail.

    Args:
        subject (str): Email subject
        recipient_email (str): Recipient email
        body (str): Email body (HTML)
    """
    message = MessageSchema(
        subject=subject,
        recipients=[recipient_email],
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

# Optional: helper function to generate email body
def generate_appointment_email(details: dict):
    return f"""
    <h3>Appointment Confirmation</h3>
    <p>Hello {details['patient_name']},</p>
    <p>Your appointment is confirmed with Dr. {details['doctor_name']} ({details['department']}) at {details['appointment_time']}.</p>
    <p>Contact Number: {details['contact_number']}</p>
    """
