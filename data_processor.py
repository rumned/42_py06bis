#!/usr/bin/env python3
import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.rank: int = 0
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
            return (self.order.pop(0), self.stored.pop(0))
        except Exception as e:
            return (-1, f"{e}")


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            for i in data:
                if not isinstance(i, (int, float)):
                    return False
            return True
        return isinstance(data, (int, float))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        if isinstance(data, list):
            for i in data:
                self.order.append(self.rank)
                self.stored.append(str(i))
                self.rank += 1
        else:
            self.order.append(self.rank)
            self.stored.append(str(data))
            self.rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            for i in data:
                if not isinstance(i, str):
                    return False
            return True
        return isinstance(data, str)

    def ingest(self, data: list[str] | str) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, list):
            for i in data:
                self.order.append(self.rank)
                self.stored.append(i)
                self.rank += 1
        else:
            self.order.append(self.rank)
            self.stored.append(data)
            self.rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            for i in data:
                if not isinstance(i, dict):
                    return False
                for k in i:
                    if not isinstance(k, str) or not isinstance(i[k], str):
                        return False
            return True
        if isinstance(data, dict):
            for k in data:
                if not isinstance(k, str) or not isinstance(data[k], str):
                    return False
            return True
        return False

    def ingest(self, data: list[dict[str, str]] | dict[str, str]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, list):
            for i in data:
                self.order.append(self.rank)
                self.stored.append(": ".join(i.values()))
                self.rank += 1
        else:
            self.order.append(self.rank)
            self.stored.append(": ".join(data.values()))
            self.rank += 1

if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")
    print("\nTesting Numeric Processor...")
    num = NumericProcessor()
    print(f" Trying to validate input '42': {num.validate(42)}")
    print(f" Trying to validate input 'Hello': {num.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")
    except Exception as e:
        print(f" Got exception: {e}")
    print(" Test invalid ingestion of number '69' without prior validation:")
    try:
        num.ingest(69)
    except Exception as e:
        print(f" Got exception: {e}")
    
    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {data}")
    num.ingest(data)
    print(" Extracting 3 values...")
    for i in data:
        rank, value = num.output()
        print(f" Numeric value {rank}: {value}")

    text = TextProcessor()
    print('\nTesting Text Processor...')
    print(f" Trying to validate input '42': {text.validate(42)}")
    words: list[str] = ["Hello", "Nexus", "World"]
    print(f" Processing data: {words}")
    text.ingest(words)
    print(" Extracting 1 value...")
    rank, value = text.output()
    print(f" Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f" Trying to validate input 'Hello': {log.validate('Hello')}")
    logs: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f" Processing data: {logs}")
    log.ingest(logs)
    print(" Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f" Log entry {rank}: {value}")
