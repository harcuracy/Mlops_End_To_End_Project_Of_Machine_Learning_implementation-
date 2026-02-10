from us_visa.constants import *
from us_visa.utils.common import read_yaml, create_directories
from us_visa.entity.config_entity import DataIngestionConfig


class ConfigurationManager:

    ''' 
    This class is responsible for reading the config file and creating the necessary directories
        1. read the config file and return the config object
        2. create the necessary directories
        3. return the data ingestion config object
        4. return the data validation config object
        5. return the data transformation config object
        6. return the model trainer config object
        7. return the model evaluation config object
        8. return the model pusher config object
        9. return the training pipeline config object
    
        Note: The config file is in yaml format and is located at CONFIG_FILE_PATH

    '''
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            DB_NAME=config.DB_NAME,
            train_file_name=config.train_file_name,
            test_file_name=config.test_file_name,
            local_data_file=config.local_data_file,
            COLLECTION_NAME=config.COLLECTION_NAME,
            CONNECTION_URL= CONNECTION_URL
        )
        return data_ingestion_config