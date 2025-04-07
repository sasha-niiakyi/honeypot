from abc import ABC, abstractmethod


class BaseOutHandler(ABC):
	
	@abstractmethod
	def notify(self, data: str, end: str = '\n'):
		pass

	@abstractmethod
	def log_ip(self, ip: str, end: str = '\n'):
		pass