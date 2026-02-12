import sys

from us_visa import logger
from us_visa.constants import VALIDATION_STATUS
from us_visa.utils.common import read_yaml
from us_visa.exception import USvisaException
from us_visa.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from us_visa.pipeline.stage_02_data_validation import DataValidationPipeline
from us_visa.pipeline.stage_03_data_transformation import DataTransformationPipeline


def run_data_ingestion():
    stage_name = "Data Ingestion"
    logger.info(f">>>>>>> Stage {stage_name} started <<<<<<<")
    pipeline = DataIngestionPipeline()
    pipeline.main()
    logger.info(f">>>>>>> Stage {stage_name} completed <<<<<<<\n\nx==========x")


def run_data_validation():
    stage_name = "Data Validation"
    logger.info(f">>>>>>> Stage {stage_name} started <<<<<<<")
    pipeline = DataValidationPipeline()
    pipeline.main()
    logger.info(f">>>>>>> Stage {stage_name} completed <<<<<<<\n\nx==========x")


def run_data_transformation():
    stage_name = "Data Transformation"
    logger.info(f">>>>>>> Stage {stage_name} started <<<<<<<")
    pipeline = DataTransformationPipeline()
    pipeline.main()
    logger.info(f">>>>>>> Stage {stage_name} completed <<<<<<<\n\nx==========x")


if __name__ == "__main__":
    try:
        run_data_ingestion()
        run_data_validation()

        status = read_yaml(VALIDATION_STATUS)
        if status.validation_status is True:
            run_data_transformation()
        else:
            logger.info("Validation failed. Skipping Data Transformation stage.")

    except Exception as e:
        raise USvisaException(e, sys)
