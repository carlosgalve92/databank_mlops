from databank_mlops.constants import CONFIG_FILE_PATH
from databank_mlops.utils.common import read_yaml, create_directories

from databank_mlops.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
)


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir, steps=config.steps
        )
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir, steps=config.steps
        )

        return data_validation_config
