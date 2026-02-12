import os
from datetime import date
from dotenv import load_dotenv
from pathlib import Path



load_dotenv()

CONFIG_FILE_PATH = Path("config/config.yaml")

SCHEMA_FILe_PATH = Path("config/schema.yaml")

VALIDATION_STATUS = Path("artifacts/data_validation/validation_status.yml")

CONNECTION_URL = os.environ.get("MONGO_URI")

CURRENT_YEAR = date.today().year




