import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


URL = os.getenv('URL')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
COOKIES_FILE_NAME = 'cookies.pkl'
