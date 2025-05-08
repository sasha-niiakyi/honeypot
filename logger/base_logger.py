from typing import Optional, Union
from abc import ABC, abstractmethod

from .data_log import DataLog


class BaseLogger(ABC):

	@abstractmethod
	def log(self, message:Optional[str], data:Optional[Union[DataLog, dict]] = None, level:Optional[str] = 'INFO'):
		pass

	@abstractmethod
	def update(self, **kwargs):
		'''Update DataLog'''
		pass

