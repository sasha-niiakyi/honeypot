from abc import ABC, abstractmethod


class BaseExecutor:

	@abstractmethod
	def execute(self, command: str):
		pass