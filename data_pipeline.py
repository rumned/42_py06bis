#!/usr/bin/env python3
import abc
import typing

NOT_VALIDATED = object()


class ExportPlugin(typing.Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.rank: int = 0
        self.order: list[int] = []
        self.stored: list[str] = []
        self.validated: typing.Any = NOT_VALIDATED
        self.count: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            result = (self.order.pop(0), self.stored.pop(0))
            self.count -= 1
            return result
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


def run_case(proc: DataProcessor,
             i_data: typing.Any,
             v_data: typing.Any = NOT_VALIDATED) -> None:
    try:
        if v_data is not NOT_VALIDATED:
            print(f"validate({repr(v_data)}): "
                  f"{proc.validate(v_data)}\n")
        proc.ingest(i_data)
        print(f"ingest({repr(i_data)}): OK\n")
        for i in range(len(proc.stored)):
            print(f"output(): {proc.output()}\n")
    except Exception as e:
        print(f"ingest({repr(i_data)}) got exception: {e}\n")


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value[1] for value in data))
        print()


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        items = [f'"item_{rank}": "{value}"' for rank, value in data]
        print("JSON Output:")
        print("{" + ", ".join(items) + "}")
        print()


class DataStream():
    def __init__(self) -> None:
        self.registered: list[DataProcessor] = []
        self.received: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        try:
            if proc not in self.registered:
                self.registered.append(proc)
                self.received[proc] = 0
            else:
                return
        except Exception as e:
            print(e)

    def process_stream(self, stream: list[typing.Any]) -> None:
        try:
            for element in stream:
                for proc in self.registered:
                    if proc.validate(element):
                        proc.ingest(element)
                        amount = (len(element)
                                  if isinstance(element, list) else 1)
                        proc.count += amount
                        self.received[proc] += amount
                        break
                else:
                    print("DataStream error - Can't process element in "
                          f"stream: {element}")
        except Exception as e:
            print(e)

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self.registered:
            print("No processor found, no data")
            return
        for proc in self.registered:
            name = type(proc).__name__
            print(f"{name}: total {self.received[proc]} items processed, "
                  f"remaining {proc.count} on processor")
        print()

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.registered:
            data: list[tuple[int, str]] = []
            for i in range(nb):
                if not proc.stored:
                    break
                data.append(proc.output())
            plugin.process_output(data)


if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    text = TextProcessor()
    log = LogProcessor()
    numeric = NumericProcessor()
    stream.print_processors_stats()

    batch = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO", "log_message": "User is connected"}],
        42,
        ["Hi", "five"],
    ]

    batch_2 = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [{'log_level': 'ERROR', 'log_message': '500 server crash'},
            {'log_level': 'NOTICE', 'log_message': 'Cert expires in 10 days'}],
        [32, 42, 64, 84, 128, 168],
        'World hello'
        ]

    print("Registering data processors")
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    # print("Send the same batch again")
    # stream.process_stream(batch)
    # stream.print_processors_stats()
    # print("Send the same batch again again")
    # stream.process_stream(batch)
    # stream.print_processors_stats()

    print("Send 3 processed data from each processor to CSV plugin")
    stream.output_pipeline(3, CSVExportPlugin())
    stream.print_processors_stats()

    print("Send different batch")
    stream.process_stream(batch_2)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to JSON plugin")
    stream.output_pipeline(5, JSONExportPlugin())
    stream.print_processors_stats()
