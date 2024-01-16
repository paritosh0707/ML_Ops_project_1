import pandas as pd
import numpy as np
from DiamondPricePredictor.logger.logging import logging
from DiamondPricePredictor.exception.exception import CustomException
from DiamondPricePredictor.utils.utils import save_object
import os
import sys
from dataclassees import dataclass
from pathlib import Path

from sklearn.compose import CloumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.Pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScalar

@dataclass(frozen=True)
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation(self):
        logging.info('Data Transformation initiated')
            
        # Define which columns should be ordinal-encoded and which should be scaled
        categorical_cols = ['cut', 'color','clarity']
        numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
        
        # Define the custom ranking for each ordinal variable
        cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
        color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
        clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
        
        logging.info('Pipeline Initiated')

        ## Numerical Pipeline
        num_pipeline= Pipeline(
            steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScalar())
            ]
        )

        ## Categorical Pipeline
        cat_pipeline=Pipeline(
            steps=[
                ('imputer',SimpleImputer(strategy='mode')),
                ('ordinalencoder', OrdinalEncoder(categories=[cut_categories,color_categories, clarity_categories])),
                ('scaler',StandardScalar())
            ]
        )

        preprocessor = CloumnTransformer(
            [
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols)
            ]
        )

        return preprocessor



    def initiate_data_transfromation(self,train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Reading Train and Test data completed")
            logging.info(f"Train DataFrame head : \n{train_df.head().to_string()}")
            logging.info(f"Test DataFrame head : \n{test_df.head().to_string()}")

            preprocessor_obj = self.get_data_transformation()
            target_column_name = "price"
            drop_columns = [target_column_name,'id']

            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.fit_transform(input_feature_test_df)
            logging.info("Applied preprocessor objecton training and testing data")

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            logging.info("Preprocessor object saved in pickle file")

            return (
                train_arr,
                test_arr
            )
        except Exception as e:
            logging.info(e)
            raise CustomException(e,sys)