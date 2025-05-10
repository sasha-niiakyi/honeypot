import pty
import os,sys
import select
import termios
import tty
import time

import paramiko

from .base_emul_term import BaseEmulateTerminal
from logger import BaseLogger


class BashEmulateTerminal(BaseEmulateTerminal):

	def __init__(self, logger: BaseLogger, channel: paramiko.Channel = None, color: bool = False):
		self.pwd = '/home/root'
		self.channel = channel
		self.master_fd = None
		self.logger = logger
		self.color = color
		self.buffer = ""

	def set_channel(self, new_channel: paramiko.Channel):
		self.channel = new_channel

	def send(self, data: str):
		self.channel.send(f"{data}\r")

	def clear_buffer(self):
		self.buffer = ""

	def run_term(self, pwd: str = None):
		if pwd:
			self.pwd = pwd

		pid, self.master_fd = pty.fork()

		if pid == 0:
			self._run_child()
		else:
			self._run_parent()

	def _run_child(self):
		'''slave - run commands''' 
		try:
			os.chdir(self.pwd)
		except FileNotFoundError:
			os.chdir("/home")  # fallback, если нет home

		if self.color:
			os.execvp("bash", ["bash"])

		else:
			os.environ["PS1"] = r"\u@\h:\w\$ "
			os.environ["LS_COLORS"] = ""

			os.execvp("bash", ["bash", "--norc", "--noprofile", "-i"])

	def _get_log_buffer(self, data: bytes):
		self.buffer += data.decode()
		if data == b'\r': # enter
			self.buffer += '\n'

		if data == b'\x7f' # backspace
			self.buffer = self.buffer[:-1]

		if '\n' in self.buffer:
			self.logger.update(event_type='exec_command', command=self.buffer)
			self.logger.log(f'Entered command - {self.buffer}')
			self.clear_buffer()

	def _run_parent(self):
		'''master - get and send data for slave'''
		try:
			while True:
				rlist, _, _ = select.select([self.master_fd, self.channel], [], [])

				if self.master_fd in rlist:
					try:
						output = os.read(self.master_fd, 2048)

						if not output:
							break

						self.channel.send(output)
					except OSError:
						break

				if self.channel in rlist:
					try:
						data = self.channel.recv(1024)
						self._get_log_buffer(data)

						if not data:
							break

						os.write(self.master_fd, data)
					except OSError:
						break

		finally:
			os.close(self.master_fd)
