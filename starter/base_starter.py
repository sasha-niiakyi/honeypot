from abc import ABC, abstractmethod


class BaseStarter:

	@abstractmethod
	def start_server(self):
		pass