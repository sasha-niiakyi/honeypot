from typing import Optional

from loguru import logger

from .base_logger import BaseLogger
from .data_log import DataLog


class FileLogger(BaseLogger):

	def log(self, message:Optional[str], data:Optional[DataLog | dict], level:Optional[str] = 'INFO'):
		logger.log(level, f"message: {message}, data: [ {data} ]")