import pandas as pd
import numpy as np
from DiamondPricePredictor.logger.logging import logging
from DiamondPricePredictor.exception.exception import CustomException
import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts/raw.csv")
    train_data_path: str = os.path.join("artifacts/train.csv")
    test_data_path: str = os.path.join("artifacts/test.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestin Started")
        try:
            data = pd.read_csv('artifacts/raw.csv')     ## can place a link also to read data from that 
            logging.info("Reading the Dataframe")

            os.makedirs(os.path.dirname(os.path.join(self.data_ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.data_ingestion_config.raw_data_path,index=False)
            logging.info("saved the raw data to artifacts_folder")

            train_data,test_data = train_test_split(data, test_size=0.3,random_state=7)
            logging.info('Performed train test split')

            train_data.to_csv(self.data_ingestion_config.train_data_path)
            test_data.to_csv(self.data_ingestion_config.test_data_path)

            logging.info("Data Ingestion Completed")

            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info(e)
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()