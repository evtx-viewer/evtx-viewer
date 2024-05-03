import sys
from evtx import PyEvtxParser


class EvtxData(object):
    """
    docstring
    """

    def __init__(self, data: list) -> None:
        self.data = data

    def print_all(self) -> None:
        for record in self.data:
            text = (
                f'Event Record ID: {record["event_record_id"]}\n'
                f'Event Timestamp: {record["timestamp"]}\n'
                f'{record["data"]}\n'
                "------------------------------------------\n"
            )
            sys.stdout.write(text)

    def print_one(self) -> None:
        pass

    def get_all(self) -> list:
        return self.data

    def get_one(self) -> dict:
        pass


class Parser(object):
    """
    docstring
    """

    def __call__(self, input_path: str) -> EvtxData:
        parser = PyEvtxParser("Security.evtx")
        return EvtxData(parser.records_json())


parse_records = Parser()
