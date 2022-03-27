import os
from .utils.logger import apuestas_logger as logger

if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__),'data/'))):
    logger.info("Creando la parpeta: "+os.path.abspath(os.path.join(os.path.dirname(__file__),'data/')))
    os.mkdir(os.path.abspath(os.path.join(os.path.dirname(__file__),'data/')))