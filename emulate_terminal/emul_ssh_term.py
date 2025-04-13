import paramiko

from .base_emul_term import BaseEmulateTerminal


class EmulateSSHTerminal(BaseEmulateTerminal):

	def __init__(self, channel: paramiko.Channel = None):
		self.channel = channel
		self.buffer = ''

	def set_channel(self, new_channel: paramiko.Channel):
		self.channel = new_channel

	def send(self, data: str):
		self.channel.send(f"{data}\n{self.get_ps1()}")

	def clear_buffer(self):
		self.buffer = ""

	def recv_command(self, value: int):
		command = ''

		while True:
			data = self.channel.recv(value)

			if data == b'\x7f':
				self.buffer = self.buffer[:-1]
				self.channel.send('\b \b')
				continue

			if data == b'\r':
				self.channel.send(f'\n{self.get_ps1()}')
				break

			self.channel.send(data)

			self.buffer += data.decode()

		command = self.buffer
		self.clear_buffer()

		return command