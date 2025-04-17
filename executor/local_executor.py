import os
import pty

from .base_executor import BaseExecutor


class LocalExecutor(BaseExecutor):
	def execute(self, command: str):
		pid, fd = pty.fork()
		if pid == 0:
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