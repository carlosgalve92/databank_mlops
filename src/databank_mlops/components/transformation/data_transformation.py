from databank_mlops.logger.logger import logger
from databank_mlops.utils.common import save_bin
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from databank_mlops.entity.config_entity import DataTransformationConfig
import pandas as pd
import numpy as np
import pathlib


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def read_file_data(self, local_data_file):
        """ """
        self.data = pd.read_csv(local_data_file)
        self.data.columns = self.data.columns.str.upper()

    def transform_target(self, target_column: str, category: str):
        self.data[target_column] = np.where(
            (self.data[target_column].str.upper() == category.upper()), 1, 0
        )

    def train_test_splitting(
        self, test_size, stratify_col, shuffle=True, random_state=202502
    ):
        """ """
        # Split the data into training and test sets. (0.75, 0.25) split.
        self.train, self.test = train_test_split(
            self.data,
            test_size=test_size,
            random_state=random_state,
            shuffle=shuffle,
            stratify=self.data[stratify_col],
        )

        self.train.to_csv(
            pathlib.Path(self.config.root_dir).joinpath("train.csv"), index=False
        )
        self.test.to_csv(
            pathlib.Path(self.config.root_dir).joinpath("test.csv"), index=False
        )

        logger.info("Splited data into training and test sets")
        logger.info(f"Dimensiones train {self.train.shape}")
        logger.info(f"Dimensiones test {self.test.shape}")

    def build_preprocess_ct(self, dict_steps):
        steps_preprocess = []

        for group_name, group_info in dict_steps.items():
            columns = group_info.columns
            steps_pipe = []

            for step in group_info.steps:
                class_name = step.name
                params = step.get("params", {})

                transform = globals().get(class_name)
                transform = transform(**params)

                steps_pipe.append((class_name, transform))

            steps_preprocess.append((group_name, Pipeline(steps_pipe), columns))

        self.pl_preprocess = ColumnTransformer(
            steps_preprocess,
            force_int_remainder_cols=False,
        )

        save_bin(
            self.pl_preprocess,
            pathlib.Path(self.config.root_dir).joinpath("pl_preprocess.joblib"),
        )
