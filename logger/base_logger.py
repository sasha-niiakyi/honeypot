from typing import Optional
from abc import ABC, abstractmethod

from .data_log import DataLog


class BaseLogger(ABC):

	@abstractmethod
	def log(self, message:Optional[str], data:Optional[DataLog | dict], level:Optional[str] = 'INFO'):
		pass