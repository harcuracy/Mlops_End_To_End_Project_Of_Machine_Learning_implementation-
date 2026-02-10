import sys
from us_visa import logger
from us_visa.exception import USvisaException
from us_visa.config.configuration import ConfigurationManager
from us_visa.components.data_ingestion import DataIngestion


class DataIngestionTrainingPipeline:
    def __init__(self):
        self.config = ConfigurationManager()
    
    def main(self):
        try:
            data_ingestion_config = self.config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data = data_ingestion.load_data()
            data = data_ingestion.save_data(data=data)
            data_ingestion.split_data(data=data)
        except Exception as e:
            raise USvisaException(e,sys)
        

if __name__ == "__main__":
    try:
        data_ingestion_training_pipeline = DataIngestionTrainingPipeline()
        data_ingestion_training_pipeline.main()
    except Exception as e:
        raise USvisaException(e,sys)