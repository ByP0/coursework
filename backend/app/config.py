from pathlib import Path
from dotenv import load_dotenv
import os



env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

db_url = os.getenv('DATABASE_URL')

admin_login = os.getenv('ADMIN_LOGIN')
admin_password = os.getenv('ADMIN_PASSWORD')

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')