# app/utils.py
import random
import json
from typing import List
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
import logging
import os

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'sms_logs.txt')
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/sms_logs.txt')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def get_daily_quote() -> str:
    """
    Returns a random daily health quote from data/daily_quotes.json.
    """
    try:
        with open('data/daily_quotes.json', encoding='utf-8') as f:
            quotes = json.load(f)
        if not quotes:
            return "Stay healthy and take care of yourself!"
        return random.choice(quotes)
    except Exception as e:
        print("Error loading daily quotes:", e)
        return "Stay healthy and take care of yourself!"

def send_sms(to_number: str, message: str) -> None:
    """
    Sends an SMS using Twilio and logs the result.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        logger.info(f"SMS sent to {to_number}, SID: {msg.sid}")
    except Exception as e:
        logger.error(f"Failed to send SMS to {to_number}: {str(e)}")

def get_advice(symptoms_list: List[str]) -> List[str]:
    """
    Returns advice messages based on a list of symptoms.
    """
    try:
        with open('data/knowledge_base.json', encoding='utf-8') as f:
            knowledge = json.load(f)

        advice_messages = []

        # Normalize input symptoms to lowercase for comparison
        symptoms_lower = [s.lower().strip() for s in symptoms_list]

        for item in knowledge:
            item_symptoms = [s.lower().strip() for s in item.get("symptoms", [])]
            if all(symptom in symptoms_lower for symptom in item_symptoms):
                advice_messages.append(item.get("message", "No advice available."))

        if not advice_messages:
            return ["No specific advice found. Please consult a doctor."]
        return advice_messages

    except Exception as e:
        print("Error loading knowledge base:", e)
        return ["Error loading knowledge base. Please try again."]


