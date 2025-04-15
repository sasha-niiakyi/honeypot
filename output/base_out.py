from abc import ABC, abstractmethod
import socket


class BaseOutHandler(ABC):
	
	@abstractmethod
	def notify(self, data: str, end: str = '\n'):
		pass

	@abstractmethod
	def log_ip(self, ip: str, end: str = '\n'):
		pass

	@abstractmethod
	def log_session_id(self, session_id: str, client: socket.socket):
		pass