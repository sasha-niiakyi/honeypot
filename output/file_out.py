import sys, os

from .base_out import BaseOutHandler


class FileOutHandler(BaseOutHandler):
	def __init__(self, path: str = 'output/out.txt'):
		self.path = os.path.join(sys.path[0], path)

	def _write(self, text: str, end: str = '\n'):
		with open(self.path, 'a') as file:
			file.write(f"{text}{end}")

	def notify(self, data: str, end: str = '\n'):
		self._write(data, end)

	def log_ip(self, ip: str, end: str = '\n'):
		self._write(ip, end)