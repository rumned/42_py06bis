#!/usr/bin/env python3
import abc
import typing

NOT_VALIDATED = object()


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.rank: int = 0
        self.order: list[int] = []
        self.stored: list[str] = []
        self.validated: typing.Any = NOT_VALIDATED

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
            result = len(data) > 0 and all(
                isinstance(i, (int, float)) for i in data
            )
        else:
            result = isinstance(data, (int, float))
        self.validated = data if result else NOT_VALIDATED
        return result

    def ingest(self, data: int | float | list[int | float]) -> None:
        if data is not self.validated:
            raise Exception("Improper numeric data")
        self.validated = NOT_VALIDATED
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
            result = len(data) > 0 and all(isinstance(i, str) for i in data)
        else:
            result = isinstance(data, str)
        self.validated = data if result else NOT_VALIDATED
        return result

    def ingest(self, data: list[str] | str) -> None:
        if data is not self.validated:
            raise Exception("Improper text data")
        self.validated = NOT_VALIDATED
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
        result = False
        if isinstance(data, list):
            result = len(data) > 0 and all(
                isinstance(i, dict)
                and len(i) > 0
                and all(isinstance(k, str) and isinstance(v, str)
                        for k, v in i.items())
                for i in data
            )
        elif isinstance(data, dict):
            result = len(data) > 0 and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items())
        self.validated = data if result else NOT_VALIDATED
        return result

    def ingest(self, data: list[dict[str, str]] | dict[str, str]) -> None:
        if data is not self.validated:
            raise Exception("Improper log data")
        self.validated = NOT_VALIDATED
        if isinstance(data, list):
            for i in data:
                self.order.append(self.rank)
                self.stored.append(": ".join(i.values()))
                self.rank += 1
        else:
            self.order.append(self.rank)
            self.stored.append(": ".join(data.values()))
            self.rank += 1


def run_case(processor, ingest_data, validate_data=NOT_VALIDATED):
    try:
        if validate_data is not NOT_VALIDATED:
            print(f" validate({repr(validate_data)}): "
                  f"{processor.validate(validate_data)}")
        processor.ingest(ingest_data)
        print(f" ingest({repr(ingest_data)}): OK")
        for i in range(len(processor.stored)):
            print(f" output(): {processor.output()}")
    except Exception as e:
        print(f" ingest({repr(ingest_data)}) got exception: {e}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    num = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print("\nTesting Numeric Processor...")
    run_case(num, 42, 42)
    run_case(num, '42', '42')
    run_case(num, [1,2,3,4,5], [1,2,3,4,5])
    run_case(num, ['1','2','3','4',5], ['1','2','3','4',5])
    lst = [1,2,3,4,5]
    run_case(num, lst, lst)
    str_lst = ['1','2','3','4','5'],
    run_case(num, str_lst, str_lst)
    run_case(num, 12, 10)
    run_case(num, 10)
    print("\nTesting Text Processor...")
    run_case(text, 42, 42)
    run_case(text, '42', '42')
    run_case(text, ['1','2','3','4',5], ['1','2','3','4',5])
    lst = [1,2,3,4,5]
    run_case(text, lst, lst)
    str_lst = ['1','2','3','4','5']
    run_case(text, str_lst, str_lst)
    run_case(text, '12', '10')
    run_case(text, '10')