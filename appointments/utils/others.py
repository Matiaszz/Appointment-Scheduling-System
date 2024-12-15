from dotenv import load_dotenv
from pathlib import Path


def get_env():
    ROOT = Path(__file__).parent
    return load_dotenv(ROOT / 'env' / '.env')
