import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset


from us_visa import logger
from us_visa.utils.common import write_yaml
from us_visa.entity.config_entity import DataValidationConfig






class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    @staticmethod
    def load_data(config: DataValidationConfig):
        train_df = pd.read_csv(config.train_data)
        test_df = pd.read_csv(config.test_data)
        return train_df, test_df
    
    def validate_number_of_columns(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        return train_df.shape[1] == test_df.shape[1]
    
    def validate_column_names_and_types(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        expected_columns = self.config.columns  # dict from schema.yml

        for col, expected_dtype in expected_columns.items():
            # Check column exists
            if col not in train_df.columns or col not in test_df.columns:
                print(f"Missing column: {col}")
                return False
            
            # Check dtype in train
            train_dtype = str(train_df[col].dtype)
            if train_dtype != expected_dtype:
                logger.warning(f"Train dtype mismatch for {col}: inside Schema {expected_dtype}, but in the raw dataset {train_dtype}")
                return False

            # Check dtype in test
            test_dtype = str(test_df[col].dtype)
            if test_dtype != expected_dtype:
                logger.warning(f"Test dtype mismatch for {col}: inside Schema {expected_dtype}, but in the raw dataset {test_dtype}")
                return False

        return True
    
    def check_data_drift(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
   
        report = Report(metrics=[DataDriftPreset()],include_tests=True)
        result = report.run(reference_data=train_df, current_data=test_df)
        
        # Save HTML report for visualization
    
        result.save_html(self.config.drift_report_path)
        success_list = result.tests_results
        is_data_clean = all(test.status.name == 'SUCCESS' for test in success_list)

        # 5. Return the result
        if is_data_clean:
            print("✅ Overall Status: SUCCESS (No Drift)")
            return True
        else:
            print("Overall Status: FAIL (Drift Detected)")
            return False
        
    
       
    def run_validation(self):
        train_df, test_df = self.load_data(self.config)

        col_count_ok = self.validate_number_of_columns(train_df, test_df)
        schema_ok = self.validate_column_names_and_types(train_df, test_df)
        check_drift =  self.check_data_drift(train_df, test_df)

        

        validation_status = col_count_ok and schema_ok and check_drift

    

        # Write YAML file
        write_yaml(
            self.config.validation_status_path,
            {"validation_status": validation_status}
        )

        return {
            "column_count_ok": col_count_ok,
            "schema_ok": schema_ok,
            "validation_status": validation_status,
            "no data_drift": check_drift
        }
     
