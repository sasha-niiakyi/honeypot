import socket
import time

from .base_out import BaseOutHandler


class SocketOutHandler(BaseOutHandler):
	def __init__(self, server_ip: str ="0.0.0.0", server_port: int = 2525):
		self.server_ip = server_ip
		self.server_port = server_port
		self.server_socket = (server_ip, server_port)

		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		for i in range(10):
			try:
				self.client_socket.connect(self.server_socket)
				break
			except:
				time.sleep(i)
		else:
			raise ConnectionRefusedError()

	def log_session_id(self, session_id: str, socket: list):
		self.notify(f'{session_id} - {socket[0]}:{socket[1]}')

	def notify(self, data: str, end: str = '\n'):
		self.client_socket.sendall(f'{data}{end}'.encode())

	def log_ip(self, ip: str, end: str = '\n'):
		self.client_socket.sendall(f'{ip}{end}'.encode())