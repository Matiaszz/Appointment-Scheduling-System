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
