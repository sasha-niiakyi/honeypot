from dataclasses import dataclass, asdict, field
from typing import Optional
from datetime import datetime
import uuid


@dataclass
class DataLog:
	ip: str
	port: int
	session_id: uuid.UUID = field(default_factory=uuid.uuid4)
	event_type: Optional[str] = None
	command: Optional[str] = None
	timestamp: str = datetime.utcnow().isoformat()

	def update(self, event_type: Optional[str] = None, command: Optional[str] = None):
		self.event_type = event_type or self.event_type
		self.command = command or self.command
		self.timestamp = datetime.utcnow().isoformat()

	def to_dict(self):
		return {
			**asdict(self),
			"session_id": str(self.session_id)
		}

	def __str__(self):
		return f'''{self.timestamp} | {self.event_type} from {self.ip}:{self.port} 
		| session: {self.session_id} | command: {self.command}'''.replace('\n', '').replace('\t', '')