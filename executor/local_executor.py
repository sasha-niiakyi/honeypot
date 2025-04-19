import os
import pty

from .base_executor import BaseExecutor


class LocalExecutor(BaseExecutor):
	def execute(self, command: str, pwd: str):
		pid, fd = pty.fork()
		if pid == 0:
			try:
				os.chdir(pwd)
			except FileNotFoundError:
				os.chdir("/tmp")  # fallback, если нет home

			os.execvp("bash", ["bash", "-c", command])
		else:
			output = b""
			while True:
				try:
					data = os.read(fd, 1024)
					if not data:
						break
					output += data
				except OSError:
					break
			return output.decode()