from abc import ABC, abstractmethod


class BaseEmulateTerminal(ABC):
	@abstractmethod
	def send(self, data: str):
		pass

	@abstractmethod
	def recv_command(self, value: int):
		pass

	def get_ps1(
		self, 
		user: str = 'root', 
		host: str = "127.0.0.1", 
		cwd: str = "/home/root", 
		end: str = "# "
	):
		'''PS1 environment variable emulation'''
		ps1 = f"\r{user}@{host}:{cwd}{end}"
		return ps1