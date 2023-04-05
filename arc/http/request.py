class Request:
    def __init__(self, scope: dict) -> None:
        self.headers: dict = self.format_headers(scope.get('headers'))
        self.server: str = self.format_address(scope.get('server'))
        self.client: str = self.format_address(scope.get('client'))
        self.scheme: str = scope.get('scheme')
        self.method: str = scope.get('method')
        self.path: str = scope.get('path')
        self.query_string: str = scope.get('query_string').decode()
        self.body: bytes = b''

    async def read_body(self, receive):
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return body

    def format_headers(self, headers: list) -> dict:
        """Convert raw headers list to a dict of strings

        Example Input:
            [
                (b'user-agent', b'PostmanRuntime/7.31.3'),
                (b'accept', b'*/*'),
                (b'postman-token', b'4f809440-d111-489d-b0ef-ccce55dfbfb8'),
                (b'host', b'127.0.0.1:8000'),
                (b'accept-encoding', b'gzip, deflate, br'),
                (b'connection', b'keep-alive')
            ]

        Example Output:
            {
                'user-agent': 'PostmanRuntime/7.31.3',
                'accept': '*/*',
                'host': '127.0.0.1:8000',
                'accept-encoding': 'gzip, deflate, br',
                'connection': 'keep-alive'
            }
        """
        h = {}
        for header in headers:
            k, v = header
            h[k.decode()] = v.decode()
        return h

    def format_address(self, address: tuple) -> str:
        """Convert raw client/server address tuple to a string

        Example Input:
            ('127.0.0.1', 8000)

        Example Output:
            '127.0.0.1:8000'
        """

        return f'{address[0]}:{address[1]}'
