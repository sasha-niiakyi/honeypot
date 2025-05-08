from typing import Optional
import sqlite3

from .base_logger import BaseLogger
from .data_log import DataLog


class DataBaseLogger(BaseLogger):

	def __init__(self, db_path: str = 'logger/database/honey.db', name_table: str = 'honey'):
		self.name_table = name_table
		self.conn = sqlite3.connect(db_path)
		self._create_table()

	def _create_table(self):
		self.conn.execute(f'''
			CREATE TABLE IF NOT EXISTS {self.name_table} (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp DATETIME,
				event_type TEXT,
				ip TEXT,
				port INTEGER,
				message TEXT,
				level TEXT,
				command TEXT,
				session_id TEXT
			)
		''')
		self.conn.commit()

	def _add_log(self, message:Optional[str], data:Optional[DataLog | dict], level: str):
		if isinstance(data, DataLog):
			data = data.to_dict()

		self.conn.execute(f'''
			INSERT INTO {self.name_table} (
				timestamp, event_type, ip, port, message, level, command, session_id
			) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
		''', (
			data.get("timestamp"),
			data.get("event_type"),
			data.get("ip"),
			data.get("port"),
			message,
			level,
			data.get("command"),
			data.get("session_id")
		))
		self.conn.commit()

	def log(self, message:Optional[str], data:Optional[DataLog | dict], level:Optional[str] = 'INFO'):
		self._add_log(message, data, level)