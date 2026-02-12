import sys

from dataclasses_json import config
from us_visa import logger
from us_visa.exception import USvisaException
from us_visa.config.configuration import ConfigurationManager
from us_visa.components.data_validation import DataValidation



class DataValidationPipeline:

    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation.run_validation()
        except Exception as e:
            raise USvisaException(e,sys)
        
if __name__ == "__main__":

    try:
        data_validation_pipeline = DataValidationPipeline()
        data_validation_pipeline.main()
        logger.info ("data validation completed")

    except Exception as e:
        raise USvisaException(e,sys)