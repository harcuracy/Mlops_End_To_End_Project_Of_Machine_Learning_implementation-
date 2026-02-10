import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

CONFIG_FILE_PATH = Path("config/config.yaml")
SCHEMA_FILe_PATH = Path("config/schema.yaml")

CONNECTION_URL = os.environ.get("MONGO_URI")


