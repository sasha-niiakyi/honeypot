from typing import Optional, Union

from loguru import logger

from .base_logger import BaseLogger
from .data_log import DataLog


class FileLogger(BaseLogger):

	def __init__(self, datalog: DataLog):
		self.datalog = datalog

	def log(self, message: Optional[str], data: Optional[Union[DataLog, dict]] = None, level: Optional[str] = 'INFO'):
		if data is None:
			data = self.datalog
		if isinstance(data, DataLog):
			data = data.to_dict()

		logger.log(level, f"message: {message}, data: [ {data} ]")

	def update(self, **kwargs):
		self.datalog.update(**kwargs)