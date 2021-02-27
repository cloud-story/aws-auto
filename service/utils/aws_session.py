import uuid

class AWSSession:

    def __init__(self, *kw):
        self.session_id = None
        self.uri_info = None
        self.operation = None
        self.request_path = None
        self.request_start_time = None
        

    def get_session_id(self) -> str:
        if self.session_id is None:
            self.generate_session_id()
        return self.session_id

    def set_session_id(self, session_id: str) -> None:
        self.session_id = session_id

    def get_uri_info(self) -> str:
        return self.uri_info

    def set_uri_info(self, uri_info: str) -> None:
        self.uri_info = uri_info

    def get_operation(self) -> str:
        return self.operation

    def set_operation(self, operation: str) -> None:
        self.operation = operation

    def get_request_path(self) -> str:
        return self.request_path

    def get_request_start_time(self) -> str:
        return self.request_start_time

    def set_request_start_time(self, request_start_time: str) -> None:
        self.request_start_time = request_start_time

    def generate_session_id(self) -> str:
        self.session_id = str(uuid.uuid4()).replace("-", "")

   