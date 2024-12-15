# on finish project, i will do tests with django

from google_calendar_service import get_calendar_service
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_FILE = Path(__file__).parent.parent
load_dotenv(ROOT_FILE / 'env' / '.env')

calendar_id = os.getenv('CALENDAR_ID')


def test_google_calendar():
    service = get_calendar_service()

    event = {
        'summary': 'Evento de Teste',
        'description': 'Verificando integração com Google Calendar.',
        'start': {
            'dateTime': (datetime.now() + timedelta(minutes=5)).isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': (datetime.now() + timedelta(minutes=65)).isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
    }

    try:
        created_event = service.events().insert(
            calendarId=calendar_id, body=event
        ).execute()

        print(
            f"Evento criado com sucesso! Link: {created_event.get('htmlLink')}"
        )
    except Exception as e:
        print(f"Erro ao criar evento: {e}")


if __name__ == "__main__":
    test_google_calendar()
