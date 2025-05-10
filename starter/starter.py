import socket
import threading

from .base_starter import BaseStarter
from server import BaseServer
from logger import BaseLogger, DataLog


class Starter(BaseStarter):
	def __init__(self, server: BaseServer, logger: BaseLogger, host="0.0.0.0", port=2222):
		self.host = host
		self.port = port
		self.socket = (host, port)
		self.server = server
		self.logger = logger

		self.session_lock = threading.Semaphore(1)

	def start_server(self, listen_number: int = 100):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(self.socket)
		server_socket.listen(listen_number)

		#self.logger.log(f"Server {self.server.get_name()} running at {self.host}:{self.port}", level='DEBUG')
		
		while True:
			client, addr = server_socket.accept()

			#logging
			datalog = DataLog(ip=addr[0], port=addr[1], event_type='SSH connect')
			self.logger.set_datalog(datalog)
			self.logger.log(f"New connection: {addr[0]}:{addr[1]}, client - {client}", level='WARNING')

			threading.Thread(
				target=self._handle_with_lock,
				args=(client,)
			).start()

	def _handle_with_lock(self, client):
		with self.session_lock:
			self.server.handle_client(client)