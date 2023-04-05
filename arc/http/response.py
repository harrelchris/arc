class Response:
    def __init__(self):
        self.headers = []
        self.body = b''
        self.status = 200

    def append_header(self, key: str, value: str):
        self.headers.append((key.encode(), value.encode()))
