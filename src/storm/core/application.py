import json
from storm.core.router import Router
from storm.core.middleware_pipeline import MiddlewarePipeline


class StormApplication:
    """
    The main application class responsible for bootstrapping the Storm framework.

    Attributes:
        - root_module: The root module of the application
        - modules: A dictionary to store loaded modules
        - router: An instance of the Router class to handle route management
        - middleware_pipeline: The pipeline that handles middleware execution
    """

    def __init__(self, root_module):
        self.root_module = root_module
        self.modules = {}
        self.router = Router()
        self.middleware_pipeline = MiddlewarePipeline([])
        self._load_modules()
        self._initialize_services()

    def _load_modules(self):
        """
        Load the modules defined in the root module's imports.
        """
        for module in self.root_module.imports:
            self.modules[module.__name__] = module

    def _initialize_services(self):
        """
        Initializes the services defined in each loaded module.
        """
        for module in self.modules.values():
            for provider in module.providers:
                pass  # Initialize providers if necessary

    async def handle_request(self, method, path, **request_kwargs):
        """
        Handles incoming HTTP requests by resolving routes and executing middleware.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path
        :param request_kwargs: Additional request parameters
        :return: A tuple containing the response and status code
        """
        try:
            handler, params = self.router.resolve(method, path)
            response = await handler(**params)
            return response, 200
        except ValueError as e:
            # Return a 404 error if the route is not found
            return {"error": str(e)}, 404

    def add_middleware(self, middleware_cls):
        """
        Adds global middleware to the application.

        :param middleware_cls: The middleware class to be added
        """
        self.middleware_pipeline.middleware_list.append(middleware_cls())

    def run(self, host='127.0.0.1', port=8000):
        """
        Starts the application server using Uvicorn.

        :param host: The host address (default is '127.0.0.1')
        :param port: The port number (default is 8000)
        """
        import uvicorn
        uvicorn.run(self, host=host, port=port)

    async def __call__(self, scope, receive, send):
        """
        ASGI application entry point.

        :param scope: The scope of the ASGI connection
        :param receive: The receive channel
        :param send: The send channel
        """
        if scope['type'] == 'http':
            method = scope['method']
            path = scope['path']
            request_kwargs = {}
            response, status_code = await self.handle_request(method, path, **request_kwargs)
            await send({
                'type': 'http.response.start',
                'status': status_code,
                'headers': [(b'content-type', b'application/json')],
            })
            await send({
                'type': 'http.response.body',
                'body': bytes(json.dumps(response), 'utf-8'),
            })
