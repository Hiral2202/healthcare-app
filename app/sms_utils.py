from twilio.rest import Client

account_sid = "YACfddaae1813500e1aaaa626a6ab05ce6f"
auth_token = "8a2a0ac4494ec15965f41573b50d95eb"
twilio_number = "+17154578845"

def send_sms(phone_number, message):
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=phone_number
    )
