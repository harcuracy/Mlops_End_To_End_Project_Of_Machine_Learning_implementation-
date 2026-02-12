import sys


from us_visa import logger
from us_visa.exception import USvisaException
from us_visa.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from us_visa.pipeline.stage_02_data_validation import DataValidationPipeline




STAGE_NAME = "Data Ingestion"


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.main()
        logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
    except Exception as e:
        raise USvisaException(e,sys)
    

STAGE_NAME = "Data Validation"


if __name__ == "__main__":

    try:
        logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
        data_validation_pipeline = DataValidationPipeline()
        data_validation_pipeline.main()
        logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
    except Exception as e:
        raise USvisaException(e,sys)



