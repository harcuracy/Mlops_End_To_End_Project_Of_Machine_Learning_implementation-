import pandas as pd
import numpy as np
from joblib import dump
from sklearn.preprocessing import OneHotEncoder, StandardScaler,OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek, SMOTEENN


from us_visa import logger
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.constants import CURRENT_YEAR,VALIDATION_STATUS


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    
    @staticmethod
    def load_data(file_path: str):
        return pd.read_csv(file_path)

        

    def data_analysis_and_transformation(self):
        '''
        This function performs data analysis and initial transformation

        '''

        # load data
        loaded_train_data = self.load_data(self.config.train_data)
        loaded_test_data = self.load_data(self.config.test_data)

        # check missing values
        train_features_with_na=[features for features in loaded_train_data.columns if loaded_train_data[features].isnull().sum()>=1]
        test_features_with_na=[features for features in loaded_test_data.columns if loaded_test_data[features].isnull().sum()>=1]
        logger.info(f"columns with missing values: {train_features_with_na}")
        logger.info(f"columns with missing values: {test_features_with_na}")

        # check duplicate values
        train_duplicates = loaded_train_data.duplicated().sum()
        test_duplicates = loaded_test_data.duplicated().sum()
        logger.info(f"number of duplicate rows in train data: {train_duplicates}")
        logger.info(f"number of duplicate rows in test data: {test_duplicates}")


        # Adding "company_age" column
        loaded_train_data["company_age"] = CURRENT_YEAR - loaded_train_data["yr_of_estab"]
        loaded_test_data["company_age"] = CURRENT_YEAR - loaded_test_data["yr_of_estab"]
        logger.info("Added company_age column to train and test data")

        # Drop columns
        drop_columns = self.config.drop_columns
        loaded_train_data = loaded_train_data.drop(columns=drop_columns, errors='ignore')
        loaded_test_data = loaded_test_data.drop(columns=drop_columns, errors='ignore')
        logger.info(f"Dropped columns: {drop_columns}")

        # X and y separation
        train_X = loaded_train_data.drop(self.config.target_column, axis=1)
        train_y = loaded_train_data[self.config.target_column]

        test_X = loaded_test_data.drop(self.config.target_column, axis=1)
        test_y = loaded_test_data[self.config.target_column]
        logger.info("Separated features and target variable")

        # Encoding labels manually
        train_y_encoded = np.where(train_y=="Certified", 1, 0)
        test_y_encoded = np.where(test_y=="Certified", 1, 0)
        logger.info("Encoded target variable")


        return train_X, train_y_encoded, test_X, test_y_encoded

    def transform(self):
        ''' 
        This function performs data transformation including scaling and encoding 
        '''
        # preprocessing
        train_X, train_y,test_X, test_y = self.data_analysis_and_transformation()

        # Define transformers for different types of features
        numeric_transformer = StandardScaler()
        oh_transformer = OneHotEncoder()
        ordinal_encoder = OrdinalEncoder()

        # initializing all the columns for transformation
        or_columns = self.config.or_columns
        oh_columns = self.config.oh_columns
        transform_columns = self.config.transform_columns
        num_features = self.config.num_features

        transform_pipe = Pipeline(steps=[
    ('transformer', PowerTransformer(method='yeo-johnson'))])
        preprocessor = ColumnTransformer(
    [
        ("OneHotEncoder", oh_transformer, oh_columns),
        ("Ordinal_Encoder", ordinal_encoder, or_columns),
       ("Transformer", transform_pipe, transform_columns),
        ("StandardScaler", numeric_transformer, num_features)
    ]
)
        # Fit and transform the training data, transform the testing data
        X_train_transformed = preprocessor.fit_transform(train_X)
        X_test_transformed = preprocessor.transform(test_X)

        # save the preprocessor
        dump(preprocessor,self.config.preprocessor)

        
        logger.info("Transformed training and testing data")

        return X_train_transformed, train_y, X_test_transformed, test_y
    
    def handle_imbalanced_data(self):
        '''
        This function handles imbalanced data using SMOTETomek
        '''
        X_train_transformed, train_y, X_test_transformed, test_y = self.transform()

        smt = SMOTETomek(random_state=42)
        X_train_res, y_train_res = smt.fit_resample(X_train_transformed, train_y)
        logger.info("Resampled training data")

        return X_train_res, y_train_res, X_test_transformed, test_y

    def save_as_npz(self, X_train, y_train, X_test, y_test):
        np.savez(self.config.transformed_train_data, X=X_train, y=y_train)
        np.savez(self.config.transformed_test_data, X=X_test, y=y_test)
        logger.info(f"Saved transformed data to {self.config.transformed_train_data} and {self.config.transformed_test_data}")







