from typing import Optional, Union

from .db_logger import DataBaseLogger
from .file_logger import FileLogger
from .base_logger import BaseLogger
from .data_log import DataLog


class DataBaseFileLogger(BaseLogger):
	def __init__(self, datalog: Optional[DataLog] = None, db_path: str = 'logger/database/honey.db', name_table: str = 'honey'):
		self.db_logger = DataBaseLogger(datalog, db_path, name_table)
		self.file_logger = FileLogger(datalog)
		self.datalog = datalog

	def set_datalog(self, datalog: DataLog):
		self.db_logger.set_datalog(datalog)
		self.file_logger.set_datalog(datalog)
		self.datalog = datalog

	def log(self, message: Optional[str], data: Optional[Union[DataLog, dict]] = None, level: Optional[str] = 'INFO'):
		self.db_logger.log(message, data, level)
		self.file_logger.log(message, data, level)

	def update(self, **kwargs):
		self.db_logger.update(**kwargs)
		self.file_logger.update(**kwargs)

		if self.datalog:
			self.datalog.update(**kwargs)

	def get_session_id(self) -> str:
		return self.file_logger.get_session_id()
