#!/usr/bin/env python3
import abc
import typing

class DataProcessor(abc.ABC):
	def __init__(self) -> None:
		self.order: list[int] = []
		self.stored: list[str] = []


	@abc.abstractmethod
	def validate(self, data: typing.Any) -> bool:
		pass


	@abc.abstractmethod
	def ingest(self, data: typing.Any) -> None:
		pass


	def output(self) -> tuple[int, str]:
		try:
			return (self.order[0], self.stored[0])
		except Exception as e:
			return(-1, f"{e}")


class NumericProcessor(DataProcessor):
	def validate(self, data: int | float | list[int | float]) -> bool:
		self.valid = False
		self.checked = False
		self.type = ""
		if isinstance (data, list):
			for i in data:
				if not isinstance(data[i], (int, float)):
					self.valid = False
					break
				else:
					self.valid = True
			self.checked = True

		elif isinstance (data, (int, float)):
			self.valid = True
			self.checked = True


	def ingest(self, data: int | float | list[int | float]) -> None:
		try:
			if data.checked is False:
				raise Exception("Improper numeric data")
			elif data.valid is False:
				raise Exception("Data is not numeric")
		except Exception as e:
			print(e)
		else:
			if 

# class TextProcessor(DataProcessor):