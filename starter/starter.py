import socket
import threading

from .base_starter import BaseStarter
from server import BaseServer
from logger import logger


class Starter(BaseStarter):
	def __init__(self, server: BaseServer, host="0.0.0.0", port=2222):
		self.host = host
		self.port = port
		self.socket = (host, port)
		self.server = server

	def start_server(self, listen_number: int = 100):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(self.socket)
		server_socket.listen(listen_number)

		logger.debug(f"Server {self.server.get_name()} running at {self.host}:{self.port}")
		
		while True:
			client, addr = server_socket.accept()
			logger.warning(f"New connection: {addr[0]}:{addr[1]}, client - {client}")
			threading.Thread(target=self.server.handle_client, args=(client,)).start()