import socket
import paramiko
import threading
import uuid

from .ssh_interface import SSHServerInterface
from emulate_terminal import BaseEmulateTerminal
from executor import BaseExecutor
from output import BaseOutHandler
from server import BaseServer
from logger import BaseLogger


class SSHServer(BaseServer):
	def __init__(self, 
		path_key: str, 
		emul_term: BaseEmulateTerminal, 
		executor: BaseExecutor, 
		out: BaseOutHandler,
		logger: BaseLogger,
		login: str = '',
		password: str = ''
	):
		self.emul_term = emul_term
		self.executor = executor
		self.out = out
		self.logger = logger
		self.host_key = paramiko.RSAKey(filename=path_key)
		self.server_interface = SSHServerInterface(logger, login=login, password=password)
		self.name = 'SSH'
		self.server_banner = "Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\n"
		self.protocol_banner = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.5"

	def get_name(self):
		return self.name

	def set_protocol_banner(self, new_banner: str):
		self.protocol_banner = new_banner

	def get_protocol_banner(self):
		return protocol_banner

	def set_server_banner(self, new_banner: str):
		self.server_banner = new_banner

	def get_server_banner(self):
		return self.server_banner

	def _setup_transport(self, client: socket.socket):
		transport = paramiko.Transport(client)
		transport.add_server_key(self.host_key)
		transport.local_version = self.protocol_banner

		return transport

	def _start_server_interface(self, transport: paramiko.Transport):
		transport.start_server(server=self.server_interface)

		return self.server_interface

	def _accept_channel(self, transport: paramiko.Transport, seconds_wait: int = 20) -> paramiko.Channel:
		# wait client
		return transport.accept(seconds_wait) 

	def _wait_shell(self, server_interface: SSHServerInterface, timeout: int):
		server_interface.event.wait(timeout)
		return server_interface.event.is_set()

	def gen_log(self, session_id: str, data: str) -> str:
		return f"Client: {session_id}, data: {data}"

	# # create another class Session
	# def generate_session_id(self, socket: list):
	# 	return uuid.uuid5(uuid.NAMESPACE_DNS, f'{socket[0]}:{socket[1]}')

	def handle_client(self, client: socket.socket, seconds_wait: int = 20):
		socket = client.getpeername()
		self.out.log_ip(socket[0])
		session_id = self.logger.get_session_id()
		self.out.log_session_id(session_id, socket)

		transport = self._setup_transport(client)
		server_interface = self._start_server_interface(transport)

		channel = self._accept_channel(transport, seconds_wait)
		if channel is None:
			return

		if not self._wait_shell(server_interface, seconds_wait):
			return

		self.emul_term.set_channel(channel)
		self.emul_term.send(self.server_banner)
		self.emul_term.run_term(pwd='/home/{server_interface.login}')

		self.logger.update(event_type='SSH disconnect', command=None)
		self.logger.log(f'Bot disconnected')

		channel.close()
		transport.close()
