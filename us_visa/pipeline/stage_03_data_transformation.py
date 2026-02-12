import sys


from us_visa import logger
from us_visa.constants import VALIDATION_STATUS
from us_visa.utils.common import read_yaml
from us_visa.exception import USvisaException
from us_visa.config.configuration import ConfigurationManager
from us_visa.components.data_transformation import DataTransformation



class DataTransformationPipeline:

    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            X_train_res, y_train_res, X_test_res, y_test_res = data_transformation.handle_imbalanced_data()
            data_transformation.save_as_npz(X_train_res, y_train_res, X_test_res, y_test_res)

        except Exception as e:
          raise USvisaException(e,sys)
        


    if __name__ == "__main__":
        try:
            data_validation_pipeline = DataTransformationPipeline()
            data_validation_pipeline.main()
            logger.info ("data validation completed")

        except Exception as e:
            raise USvisaException(e,sys)



