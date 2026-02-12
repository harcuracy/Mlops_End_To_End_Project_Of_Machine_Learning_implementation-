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



@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    train_data: str
    test_data: str
    drift_report_path: str
    validation_status_path: str
    columns: dict
    numerical_columns: list[str]
    categorical_columns: list[str]