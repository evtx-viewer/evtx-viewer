from evtx import PyEvtxParser


class EvtxData(object):
    """
    docstring
    """

    def __init__(self, data: list) -> None:
        self.data = data

    def get_all_str(self) -> str:
        result_string: str = ""
        for record in self.data:
            result_string += (
                f'Event Record ID: {record["event_record_id"]}\n'
                f'Event Timestamp: {record["timestamp"]}\n'
                f'{record["data"]}\n'
                "------------------------------------------\n"
            )
        return result_string

    def get_one_str(self) -> None:
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
        parser = PyEvtxParser(input_path)
        return EvtxData(parser.records_json())


parse_records = Parser()
