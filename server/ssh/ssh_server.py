import socket
import paramiko
import threading

from .ssh_interface import SSHServerInterface
from emulate_terminal import BaseEmulateTerminal
from executor import BaseExecutor
from output import BaseOutHandler
from server import BaseServer
from logger import logger


class SSHServer(BaseServer):
	def __init__(self, 
		path_key: str, 
		emul_term: BaseEmulateTerminal, 
		executor: BaseExecutor, 
		out: BaseOutHandler
	):
		self.emul_term = emul_term
		self.executor = executor
		self.out = out
		self.host_key = paramiko.RSAKey(filename=path_key)

	def get_name(self):
		return 'SSH'

	def _setup_transport(self, client: socket.socket):
		transport = paramiko.Transport(client)
		transport.add_server_key(self.host_key)

		return transport

	def _start_server_interface(self, transport: paramiko.Transport):
		server_interface = SSHServerInterface()
		transport.start_server(server=server_interface)

		return server_interface

	def _accept_channel(self, transport: paramiko.Transport, seconds_wait: int = 20) -> paramiko.Channel:
		# wait client
		return transport.accept(seconds_wait) 

	def _wait_shell(self, server_interface: SSHServerInterface, timeout: int):
		server_interface.event.wait(timeout)
		return server_interface.event.is_set()

	def handle_client(self, client: socket.socket, seconds_wait: int = 20):
		transport = self._setup_transport(client)
		server_interface = self._start_server_interface(transport)

		channel = self._accept_channel(transport, seconds_wait)
		if channel is None:
			return

		if not self._wait_shell(server_interface, seconds_wait):
			return

		self.emul_term.set_channel(channel)

		self.emul_term.send("Добро пожаловать в фальшивую систему!\n")

		while True:
			command = self.emul_term.recv_command(1024)
			request = self.executor.execute(command)
			self.emul_term.send(request)

			# print(request)
			# print(command)

		channel.close()
