from abc import ABC, abstractmethod
import socket


class BaseServer(ABC):

	@abstractmethod
	def handle_client(self, client: socket.socket):
		pass

	@abstractmethod
	def get_name(self) -> str:
		pass 