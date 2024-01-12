import os
from pathlib import Path


list_of_files=[

    ".github/workflows/.gitkeep",
    "src/__init__.py",
    "src/DiamondPricePredictor/components/__init__.py",
    "src/DiamondPricePredictor/components/data_ingestion.py",
    "src/DiamondPricePredictor/components/data_transformation.py",
    "src/DiamondPricePredictor/components/model_trainer.py",
    "src/DiamondPricePredictor/components/model_evaluation.py",
    "src/DiamondPricePredictor/pipeline/__init__.py",
    "src/DiamondPricePredictor/pipeline/training_pipeline.py",
    "src/DiamondPricePredictor/pipeline/prediction_pipeline.py",
    "src/DiamondPricePredictor/utils/__init__.py",
    "src/DiamondPricePredictor/utils/utils.py",
    "src/DiamondPricePredictor/logger/logging.py",
    "src/DiamondPricePredictor/exception/exception.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
    "init_setup.sh",
    "requirements.txt",
    "requirements_dev.txt",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "tox.ini",
    "experiment/experiments.ipynb"

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass # create an empty file