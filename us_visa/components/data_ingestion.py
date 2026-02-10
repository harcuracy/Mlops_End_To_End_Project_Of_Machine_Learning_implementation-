import os
import sys
import pymongo
import pandas as pd

from us_visa import logger
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import DataIngestionConfig


class DataIngestion:

    '''
    This class is responsible for data ingestion from mongodb and saving it to local file.
     1. load data from mongodb and return as pandas dataframe
     2. drop _id column and save data to local file
     3. split data into train and test file and save it to local file

    '''

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    # load data from mongodb and return as pandas dataframe

    def load_data(self) -> pd.DataFrame:
        try:
            client = pymongo.MongoClient(self.config.CONNECTION_URL)
            db = client[self.config.DB_NAME]
            collection = db[self.config.COLLECTION_NAME]
            data = list(collection.find())
            data = pd.DataFrame(data)
        except Exception as e:
            raise USvisaException(e,sys)
        return data
    
    # drop _id column and save data to local file

    def save_data(self, data: pd.DataFrame) ->pd.DataFrame:
        try:
            data.drop(columns=["_id"], inplace=True)
            data.to_csv(self.config.local_data_file, index=False)
            logger.info(f"Data saved successfully at {self.config.local_data_file}")
            logger.info(f"Data shape: {data.shape}")
        except Exception as e:
            raise USvisaException(e, sys)
        return data

    # split data into train and test file
    def split_data(self, data: pd.DataFrame) -> None:
        
        # split data into train and test file
        try:
            train_df = data.sample(frac=0.8, random_state=42)
            test_df = data.drop(train_df.index)
            # save train and test data to local file
            train_df.to_csv(os.path.join(self.config.root_dir, self.config.train_file_name), index=False)
            test_df.to_csv(os.path.join(self.config.root_dir, self.config.test_file_name), index=False)
            logger.info(f"Train and test data saved successfully at {self.config.root_dir}")
            logger.info(f"Train data shape: {train_df.shape}")
            logger.info(f"Test data shape: {test_df.shape}")
        except Exception as e:
            raise USvisaException(e,sys)  

        