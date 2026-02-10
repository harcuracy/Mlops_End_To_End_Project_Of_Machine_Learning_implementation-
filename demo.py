import sys
from us_visa.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from us_visa import logger
from us_visa.exception import USvisaException



STAGE_NAME = "Data Ingestion Stage"


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
        data_ingestion_training_pipeline = DataIngestionTrainingPipeline()
        data_ingestion_training_pipeline.main()
        logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
    except Exception as e:
        raise USvisaException(e,sys)
