import os
import sys
from dataclasses import dataclass


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformation_object(self):
        logging.info("Getting preprocessor object from file")
        
        try:
            num_columns = ["writing score", "reading score"]
            cat_columns = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
            
            
            num_trans_pipe=Pipeline(
                steps=[
               ("imputer", SimpleImputer(strategy="median", fill_value='missing',missing_values=np.nan)),
               ("scaler", StandardScaler(with_mean=False))
                ]
            )
            
            cat_tarns_pipe = Pipeline(
                
                  steps=[
                      ("imputer", SimpleImputer(strategy="most_frequent", fill_value='missing',missing_values=np.nan)),
                      ("OneHotEncoder", OneHotEncoder(drop='if_binary')),
                      ("scaler", StandardScaler(with_mean=False))
                      
                  ]
            )
            
            logging.info("Numerical standard scale has been completed")
            logging.info("Categorical one hot encoding has been completed")
            
            preprocessor = ColumnTransformer(
                 transformers= [
                     ("Numerical", num_trans_pipe, num_columns ),
                     ("Categorical", cat_tarns_pipe, cat_columns)
                 ]
            )
            return preprocessor
        
        
        
        except Exception as e:
            raise CustomException(e, sys)
    
    
    def initiate_data_transformation(self, train_path, test_path):
        
        try:
            train_df =pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data frame")
            logging.info("Obtaining preprocessor object")
            
            preprocessor_obj = self.get_data_transformation_object()
            
            target_column_name="math score"
            numerical_columns = ["writing score", "reading score"]
            
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            logging.info(f"Applying preprocessing object on training data frame and testing data frame.")
            
            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info(f"Saved preprocessing object.")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj)
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path)

            
        except Exception as e:
            raise CustomException(e, sys)