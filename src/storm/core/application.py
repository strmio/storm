import json
from storm.core.interceptor_pipeline import InterceptorPipeline
from storm.core.middleware_pipeline import MiddlewarePipeline
from storm.core.router import Router
from storm.common.services.logger import Logger

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
        self.logger = Logger()
        self.middleware_pipeline = MiddlewarePipeline()
        self.interceptor_pipeline = InterceptorPipeline(global_interceptors=[])
        self._load_modules()


    def add_global_interceptor(self, interceptor_cls):
        """
        Registers a global interceptor to be applied across all requests.

        :param interceptor_cls: The interceptor class to be added as a global interceptor.
        """
        self.interceptor_pipeline.add_global_interceptor(interceptor_cls)

    def add_global_middleware(self, middleware_cls):
        """
        Registers a global middleware to be applied across all routes.

        :param middleware_cls: The middleware class to be added as global middleware.
        """
        self.middleware_pipeline.add_global_middleware(middleware_cls)

    def _load_modules(self):
        """ Load modules and log the process. """
        self.logger.info(f"Loading modules from: {self.root_module.__name__}")
        for module in self.root_module.imports:
            self.modules[module.__name__] = module
            self.logger.info(f"Loaded module: {module.__name__}")
            self._initialize_module(module)


    def _inject_dependencies(self, service, module):
        """
        Inject dependencies into a service, resolving them from the module's providers.

        :param service: The service instance to inject dependencies into.
        :param module: The module providing the dependencies.
        """
        for attr_name, dependency in service.__annotations__.items():
            if dependency in module.providers:
                setattr(service, attr_name, module.providers[dependency.__name__])

    def _initialize_services(self, module):
        """
        Initialize services for a given module, resolving dependencies and ensuring
        that each service is ready to be used.

        :param module:  The module whose services need to be initialized.
        """
        for provider in module.providers:
            service_instance = provider()
            self._inject_dependencies(service_instance, module)
            module.providers[provider.__name__] = service_instance

    async def handle_request(self, method, path, **request_kwargs):
        """
        Handles incoming HTTP requests by resolving routes and executing middleware and interceptors.

        :param method: The HTTP method (GET, POST, etc.)
        :param path: The URL path
        :param request_kwargs: Additional request parameters
        :return: A tuple containing the response and status code
        """
        try:
            handler, params = self.router.resolve(method, path)
            request_kwargs.update(params)

            # Execute middleware first, which may modify the request
            modified_request = await self.middleware_pipeline.execute(request_kwargs, lambda req: req)

            # Execute interceptors after middleware, passing the modified request and getting the response
            response = await self.interceptor_pipeline.execute(modified_request, handler)
            
            return response, 200
        except ValueError as e:
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

    def _initialize_module(self, module):
        """ Initialize module and register controllers """
        for controller in module.controllers:
            self.logger.info(f"Registering controller: {controller.__name__}")
            # Register the routes of the controller with the router
            for route in controller.routes:
                self.logger.info(f"Registering route: {route['method']} {route['path']}")
                self.router.add_route(route["method"], route["path"], route["handler"])


    def shutdown(self):
        """
        Perform shutdown tasks, calling any onDestroy hooks in the modules.
        """
        for module in self.modules.values():
            if hasattr(module, 'onDestroy') and callable(module.onDestroy):
                module.onDestroy()
