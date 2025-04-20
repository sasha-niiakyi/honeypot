import yaml


class DataConfig:
	def __init__(self, *args, **kwargs):
		for key, value in kwargs.items():
			if isinstance(value, dict):
				setattr(self, key, DataConfig(**value))
			else:
				setattr(self, key, value)

	def to_dict(self):
		return self.__dict__

	def __str__(self):
		return f"{self.__dict__}"

	def __repr__(self):
		return f"{self.__dict__}"


class Config:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, config_path: str = 'config/config.yaml'):
		self.config_path = config_path
		temp_dict_data = self._load_config()
		self.data = self._dict_to_attrs(temp_dict_data)

	def _load_config(self) -> dict:
		with open(self.config_path) as file:
			return yaml.safe_load(file)

	def _dict_to_attrs(self, dict_attrs: dict):
		return DataConfig(**dict_attrs)


config = Config()