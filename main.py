import databank_mlops
from databank_mlops.logger.logger import logger

for i in range(10000000):
    logger.debug(f"Versión del package: {databank_mlops.__version__}")
    logger.info(f"Versión del package: {databank_mlops.__version__}")
    logger.info(f"Versión del package: {databank_mlops.__version__}" + "#############################")
    logger.error(f"Versión del package: {databank_mlops.__version__}")
