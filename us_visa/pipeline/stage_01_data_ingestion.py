import sys
from us_visa import logger
from us_visa.exception import USvisaException
from us_visa.config.configuration import ConfigurationManager
from us_visa.components.data_ingestion import DataIngestion


class DataIngestionPipeline:
    def __init__(self):
        pass
    
    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data = data_ingestion.load_data()
            data = data_ingestion.save_data(data=data)
            data_ingestion.split_data(data=data)
        except Exception as e:
            raise USvisaException(e,sys)
        

if __name__ == "__main__":
    try:
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.main()
    except Exception as e:
        raise USvisaException(e,sys)