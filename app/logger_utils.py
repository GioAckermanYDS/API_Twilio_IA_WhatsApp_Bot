import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('logtest')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(asctime)s pid/%(process)d [%(filename)s:%(lineno)d] %(message)s')

# Manejador de archivos
file_handler = RotatingFileHandler('./logs/logtest.log', maxBytes=1024 * 1024, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Manipulador de consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)