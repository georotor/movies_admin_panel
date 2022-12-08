import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
INTERNAL_IPS = ["127.0.0.1"]

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

include('components/*.py')
