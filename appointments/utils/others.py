from dotenv import load_dotenv
from pathlib import Path


def get_env() -> bool:
    """Get evironments file

    Returns:
        bool -> True if has dotenv, False if doesn't
    """
    ROOT = Path(__file__).parent.parent.parent
    return load_dotenv(ROOT / 'env' / '.env')
