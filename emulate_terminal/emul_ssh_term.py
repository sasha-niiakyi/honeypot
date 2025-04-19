import os

import paramiko

from .base_emul_term import BaseEmulateTerminal


class EmulateSSHTerminal(BaseEmulateTerminal):

	def __init__(self, channel: paramiko.Channel = None):
		self.channel = channel
		self.buffer = ''

	def set_channel(self, new_channel: paramiko.Channel):
		self.channel = new_channel

	def send(self, data: str):
		self.channel.send(f"\r{data}{self.get_ps1()}")

	def clear_buffer(self):
		self.buffer = ""

	def set_ps1(self, user: str = 'root', host: str = "127.0.0.1", end: str = '$ '):
		self.user = user
		self.host = host 
		self.pwd = f"/home/{user}"
		self.end = end
		if user == 'root':
			self.end = '# '

	def _change_dir(self, new_dir: str):
		self.pwd = os.path.abspath(os.path.join(self.pwd, new_dir))

	def get_pwd(self):
		return self.pwd

	def get_ps1(self):
		'''PS1 environment variable emulation'''
		ps1 = f"\r{self.user}@{self.host}:{self.pwd}{self.end}"
		return ps1

	def recv_command(self, value: int):
		command = ''

		while True:
			data = self.channel.recv(value)

			if data == b'\x7f': # backspace
				self.buffer = self.buffer[:-1]
				self.channel.send('\b \b')
				continue

			if data == b'\r': # enter
				self.channel.send('\n')
				break

			self.channel.send(data)

			self.buffer += data.decode()

		command = self.buffer
		self.clear_buffer()

		if 'cd ' in command:
			self._change_dir(command[3:])

		return command