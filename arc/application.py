from .requests import Request


class UnsupportedRequestTypeError(Exception):
    """Exception for unsupported request types."""

    def __init__(self, scope_type):
        self.scope_type = scope_type

    def __str__(self):
        return f"{self.scope_type} is an unsupported request type."


class Arc:
    def __init__(self):
        self.routes = {}

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            await self.lifespan(scope, receive, send)
        elif scope['type'] == 'http':
            await self.http(scope, receive, send)
        else:
            raise UnsupportedRequestTypeError(scope.get('type'))

    async def lifespan(self, scope, receive, send):
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await self.startup(scope, receive, send)
            elif message['type'] == 'lifespan.shutdown':
                await self.shutdown(scope, receive, send)
                return

    async def startup(self, scope, receive, send):
        """Perform startup processes and return lifespan response"""

        try:
            pass  # some error prone operations
        except Exception as e:  # TODO: handle specific exceptions
            response = {'type': 'lifespan.startup.failed', 'message': e}
        else:
            response = {'type': 'lifespan.startup.complete'}
        await send(response)

    async def shutdown(self, scope, receive, send):
        """Perform shutdown processes and return lifespan response"""

        try:
            pass  # some error prone operations
        except Exception as e:  # TODO: handle specific exceptions
            response = {'type': 'lifespan.startup.failed', 'message': e}
        else:
            response = {'type': 'lifespan.shutdown.complete'}
        await send(response)

    async def http(self, scope, receive, send):
        request = Request(scope)
        request.body = await request.read_body(receive)
        view = self.routes[request.path]["view"]
        response = view(request)
        await send({
            "type": "http.response.start",
            "status": response.status,
            "headers": response.headers,
            "trailers": False
        })
        await send({
            "type": "http.response.body",
            "body": response.body,
            "more_body": False
        })

    def add_route(self, path, view, methods=None):
        self.routes[path] = {
            "view": view,
            "methods": methods or ["GET"],
        }
