from typing import Optional, Union
import sqlite3

from .base_logger import BaseLogger
from .data_log import DataLog


class DataBaseLogger(BaseLogger):

	def __init__(
		self, 
		datalog: Optional[DataLog] = None, 
		db_path: str = 'logger/database/honey.db', 
		name_table: str = 'honey', 
		wal: bool = True
	):
		self.datalog = datalog
		self.name_table = name_table
		self.conn = sqlite3.connect(db_path, check_same_thread=False)
		
		if wal:
			self.conn.execute("PRAGMA journal_mode=WAL;")
			self.conn.commit()

		self._create_table()

	def set_datalog(self, datalog: DataLog):
		self.datalog = datalog

	def update(self, **kwargs):
		if self.datalog:
			self.datalog.update(**kwargs)

	def get_session_id(self) -> str:
		return self.datalog.get_session_id()

	def close(self):
		self.conn.close()

	def _create_table(self):
		self.conn.execute(f'''
			CREATE TABLE IF NOT EXISTS {self.name_table} (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp DATETIME,
				session_id UUID,
				ip TEXT,
				port INTEGER,
				event_type TEXT,
				message TEXT,
				command TEXT,
				level TEXT
			)
		''')
		self.conn.commit()

	def _add_log(self, message:Optional[str], data:Optional[Union[DataLog, dict]], level: str):
		if data is None:
			data = self.datalog
		if isinstance(data, DataLog):
			data = data.to_dict()

		self.conn.execute(f'''
			INSERT INTO {self.name_table} (
				timestamp, session_id, ip, port, event_type, message, command, level
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		''', (
			data.get("timestamp", ""),
			data.get("session_id", ""),
			data.get("ip", ""),
			data.get("port", 0),
			data.get("event_type", ""),
			message,
			data.get("command", ""),
			level
		))
		self.conn.commit()

	def log(self, message:Optional[str], data:Optional[Union[DataLog, dict]] = None, level:Optional[str] = 'INFO'):
		self._add_log(message, data, level)