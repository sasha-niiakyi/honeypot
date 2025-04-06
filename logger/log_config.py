import sys
import os

from loguru import logger


log_path = os.path.join(sys.path[0], 'logger/logs/debug.log')

logger.add(
	log_path, 
	format='{time} | {level} | {name}:{function}:{line} - {message}',
	rotation='100 MB', compression='zip')
