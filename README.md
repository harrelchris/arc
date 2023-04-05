# ARC

ASGI web server framework

## Usage

1. Create an application

    ```python
    # app.py
    from arc import Arc, Response
    
    app = Arc()
    
    def index(request):
        body = {
            "endpoint": "index",
            "path": request.path,
        }
        return Response(body=body, headers={}, status=200)
    
    app.add_route(path="/", view=index, methods=["GET"])
    ```

1. Install a web server, like uvicorn

    ```shell
    pip install uvicorn
    ```

1. Serve the application

    ```shell
    uvicorn app:app
    ```

1. Open http://127.0.0.1:8000 in a browser or send a request with Postman
