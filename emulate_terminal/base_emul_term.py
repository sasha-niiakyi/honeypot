from abc import ABC, abstractmethod


class BaseEmulateTerminal(ABC):
	@abstractmethod
	def send(self, data: str):
		pass

	@abstractmethod
	def run_term(self, pwd: str):
		pass

	# @abstractmethod
	# def recv_command(self, value: int):
	# 	pass

	# @abstractmethod
	# def get_ps1(self):
	# 	'''PS1 environment variable emulation'''
	# 	pass