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
    """
    Retrieves the Google Calendar service using the service account
    credentials.

    Returns:
        googleapiclient.discovery.Resource: The calendar service instance.
    """
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=credentials)


def insert_into_calendar(
        summary: str, start: datetime, end: datetime, description: str):
    """
    Inserts an event into the Google Calendar.

    Args:
        summary (str): The title of the event.
        start (datetime): The start date and time of the event.
        end (datetime): The end date and time of the event.
        description (str): A description for the event.

    Returns:
        dict: The created event object if successful, None if failed.
    """
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
            calendarId=CALENDAR_ID, body=event).execute()
        return created_event

    except Exception as e:
        print(f"Erro ao criar evento: {e}")
        return


def delete_from_calendar(event_id):
    """
    Deletes an event from the Google Calendar using its event ID.

    Args:
        event_id (str): The ID of the event to be deleted.

    Returns:
        None: Prints a success or error message.
    """
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId=CALENDAR_ID, eventId=event_id).execute()

        print(f"{event_id} event has been deleted successfully.")
    except Exception as e:
        print(f"Error in delete operation: {e}")
