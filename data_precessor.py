#!/usr/bin/env python3
import abc
import typing

class DataProcessor(abc.ABC):

	@abc.abstractmethod
	def validate(self, data: typing.Any) -> bool:
		pass


	@abc.abstractmethod
	def ingest(self, data: typing.Any) -> None:
		pass


	def output(self) -> tuple[int, str]:
		return (self.order, self.data)