from .base_executor import BaseExecutor


class SimpleExecutor(BaseExecutor):
	def execute(self) -> str:
		return 'executed'