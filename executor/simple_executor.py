from .base_executor import BaseExecutor


class SimpleExecutor(BaseExecutor):
	def execute(self, command: str) -> str:
		return f'executed {command}'