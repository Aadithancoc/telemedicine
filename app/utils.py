import json
import random
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

def send_sms(to_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_number
    )
    return msg.sid

def get_daily_quote():
    try:
        with open('data/daily_quotes.json') as f:
            quotes = json.load(f)
        if not quotes:
            return "Stay healthy and take care of yourself!"
        return random.choice(quotes)
    except Exception as e:
        return "Stay healthy and take care of yourself!"

def get_advice(symptoms):
    key = symptoms.lower().replace(" ", "")
    with open('data/knowledge_base.json') as f:
        knowledge_base = json.load(f)
    return knowledge_base.get(key, "No match found. Please consult a doctor.")
