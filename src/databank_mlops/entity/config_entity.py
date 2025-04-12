from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    steps: list[dict]


@dataclass
class DataValidationConfig:
    root_dir: Path
    steps: list[dict]
