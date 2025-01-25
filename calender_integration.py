import re
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import streamlit as st
from transformers import pipeline

# Define symptom and disease keywords
SYMPTOMS_KEYWORDS = [
    "fever", "cough", "dyspnea", "difficulty breathing", "fatigue", "headache", "nausea", "vomiting", "diarrhea", "abdominal pain",
    "chest pain", "shortness of breath", "sore throat", "muscle aches", "loss of taste or smell", "rash", "swelling", "joint pain"
]
DISEASES_KEYWORDS = [
    "COVID-19", "ARDS", "heart disease", "diabetes", "hypertension", "asthma", "malaria", "tuberculosis", "pneumonia", "flu",
    "kidney disease", "liver disease", "stroke", "depression", "anxiety", "cancer", "arthritis", "diarrhea", "gastritis", "IBS"
]

# Load a pre-trained sentiment-analysis pipeline for demonstration
nlp = pipeline("sentiment-analysis")

# Function to calculate risk using NLP
def calculate_risk(conversation):
    analysis = nlp(conversation)
    sentiment = analysis[0]["label"].lower()
    
    if "negative" in sentiment:
        return "High"
    elif "neutral" in sentiment:
        return "Moderate"
    else:
        return "Low"

# Extract diseases and symptoms from the conversation
def extract_diseases_and_symptoms(conversation):
    symptoms = [word for word in SYMPTOMS_KEYWORDS if word.lower() in conversation.lower()]
    diseases = [word for word in DISEASES_KEYWORDS if word.lower() in conversation.lower()]
    return symptoms, diseases

# Function to schedule a follow-up meeting
def schedule_meeting(risk_level, conversation_summary, description):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    # Load credentials or initiate authorization flow
    try:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Define meeting details based on risk level
    summary = f"Follow-up Meeting for {risk_level}-Risk Patient"
    if risk_level == "High":
        start_time = datetime.now() + timedelta(days=1)
    elif risk_level == "Moderate":
        start_time = datetime.now() + timedelta(days=3)
    else:
        start_time = datetime.now() + timedelta(days=7)

    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result.get('htmlLink')

# Streamlit UI
st.title("Patient Risk Assessment and Follow-Up Scheduler")

conversation = st.text_area("Enter the patient-doctor conversation:")

if st.button("Analyze Risk and Extract Details"):
    if conversation:
        risk_level = calculate_risk(conversation)
        symptoms, diseases = extract_diseases_and_symptoms(conversation)

        st.write(f"### Predicted Risk Level: {risk_level}")
        st.write(f"### Symptoms Identified: {', '.join(symptoms) if symptoms else 'None'}")
        st.write(f"### Diseases Identified: {', '.join(diseases) if diseases else 'None'}")

        description = f"Symptoms: {', '.join(symptoms)}\nDiseases: {', '.join(diseases)}\nConversation Summary: {conversation[:200]}"

        # Automatically schedule the meeting after analysis
        try:
            meeting_link = schedule_meeting(risk_level, conversation_summary=conversation[:200], description=description)
            st.success(f"Meeting scheduled successfully! [View Meeting]({meeting_link})")
        except Exception as e:
            st.error(f"An error occurred while scheduling the meeting: {e}")
    else:
        st.error("Please enter a conversation to analyze.")