from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    DB_NAME: str
    train_file_name: str
    test_file_name: str
    local_data_file: Path
    COLLECTION_NAME: str
    CONNECTION_URL: str