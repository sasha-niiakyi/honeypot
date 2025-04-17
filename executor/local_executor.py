import subprocess

from .base_executor import BaseExecutor


class LocalExecutor(BaseExecutor):
	def execute(self, command: str):
		try:
			result = subprocess.run(
				command, shell=True, check=True,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE
			)
			return result.stdout.decode() + result.stderr.decode()
		except subprocess.CalledProcessError as e:
			return e.stdout.decode() + e.stderr.decode()