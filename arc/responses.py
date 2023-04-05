import json


class Response:
    def __init__(self, body: dict, headers: dict = None, status: int = 200):
        self.headers = self.format_headers_dict(headers)
        self.body = json.dumps(body).encode()
        self.status = status

    def format_headers_dict(self, headers: dict) -> list:
        formatted = []
        if headers:
            for key, value in headers.items():
                formatted.append((key.encode(), value.encode()))
        return formatted
