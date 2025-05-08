from typing import Optional, Union

from loguru import logger

from .base_logger import BaseLogger
from .data_log import DataLog


class FileLogger(BaseLogger):

	def __init__(self, datalog: Optional[DataLog] = None):
		self.datalog = datalog

	def set_datalog(self, datalog: DataLog):
		self.datalog = datalog

	def log(self, message: Optional[str], data: Optional[Union[DataLog, dict]] = None, level: Optional[str] = 'INFO'):
		if data is None:
			data = self.datalog
		if isinstance(data, DataLog):
			data = data.to_dict()

		logger.log(level, f"message: {message}, data: [ {data} ]")

	def update(self, **kwargs):
		if self.datalog:
			self.datalog.update(**kwargs)

	def get_session_id(self) -> str:
		return self.datalog.get_session_id()