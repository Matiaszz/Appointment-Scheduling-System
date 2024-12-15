from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path
from dotenv import load_dotenv
import os


ROOT_FILE = Path(__file__).parent.parent.parent
load_dotenv(ROOT_FILE / 'env' / '.env')

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = ROOT_FILE / 'secrets' / 'barber_service.json'
CALENDAR_ID = os.getenv('CALENDAR_ID')


def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=credentials)


def insert_into_calendar(
        summary: str, start: datetime, end: datetime, description: str

):
    service = get_calendar_service()

    event = {
        'summary': f'Serviço agendado - {summary}',
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }

    try:
        created_event = service.events().insert(
            calendarId=CALENDAR_ID, body=event
        ).execute()

        print(
            f"Evento criado com sucesso! Link: {created_event.get('htmlLink')}"
        )
        return True

    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        return False
