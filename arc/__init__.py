import json


class Arc:
    def __init__(self):
        pass

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    response = await self.handle_startup()
                    await send(response)
                elif message['type'] == 'lifespan.shutdown':
                    await self.handle_shutdown()
                    await send({'type': 'lifespan.shutdown.complete'})
                    return
        elif scope['type'] == 'http':
            await self.handle_http(scope, receive, send)
        else:
            await self.handle_other(scope, receive, send)

    async def handle_startup(self):
        """Perform startup processes and return lifespan response"""

        try:
            pass  # some error prone operations
        except Exception as e:  # TODO: handle specific exceptions
            return {'type': 'lifespan.startup.failed'}
        else:
            return {'type': 'lifespan.startup.complete'}

    async def handle_shutdown(self):
        """Perform shutdown processes and return lifespan response"""

        try:
            pass  # some error prone operations
        except Exception as e:  # TODO: handle specific exceptions
            return {'type': 'lifespan.shutdown.failed'}
        else:
            return {'type': 'lifespan.shutdown.complete'}

    async def handle_http(self, scope, receive, send):
        event = await receive()
        data = {
            "key": "value"
        }
        string = json.dumps(data)
        response = string.encode()

        await send({"type": "http.response.start", "status": 200, "headers": {}, "trailers": False})
        await send({"type": "http.response.body", "body": response, "more_body": False})

    async def handle_other(self, scope, receive, send):
        """Placeholder for websockets and unknown"""

        print(f"Received Other: {scope['type']}")
