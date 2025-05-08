from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


@dataclass
class DataLog:
	ip: str
	port: int
	event_type: str
	command: Optional[str] = None
	session_id: Optional[str] = None
	timestamp: str = datetime.utcnow().isoformat()

	def to_dict(self):
		return asdict(self)

	def __str__(self):
		return f'''{self.timestamp} | {self.event_type} from {self.ip}:{self.port} 
		| session: {self.session_id} | command: {self.command}'''.replace('\n', '').replace('\t', '')