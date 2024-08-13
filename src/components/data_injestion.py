import os 
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from logger import logging
import pandas as pd
from exception import CustomException
from model_trainer import ModelTrainerConfig
from model_trainer import ModelTrainer

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from data_transformation import DataTransformation
from data_transformation import DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifact',"train.csv")
    test_data_path:str = os.path.join('artifact',"test.csv")
    raw_data_path:str = os.path.join('artifact',"raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion method or component")
        try:
            df = pd.read_csv(r'C:\Users\susha\PycharmProjects\MLproject\notebook\data\stud.csv')
            logging.info('reading the dataset')
                
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info('train and test split started')

            train_set, test_set= train_test_split(df, test_size = 0.2, random_state = 42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)        
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)        
            
            logging.info('ingestion of the data is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_tranformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))