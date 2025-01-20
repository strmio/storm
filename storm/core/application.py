import inspect
from functools import wraps
import traceback
from storm.common.exceptions.exception import StormHttpException
from storm.common.exceptions.http import InternalServerErrorException, NotFoundException
from storm.core.adapters.http_request import HttpRequest
from storm.core.adapters.http_response import HttpResponse
from storm.core.interceptor_pipeline import InterceptorPipeline
from storm.core.middleware_pipeline import MiddlewarePipeline
from storm.core.resolvers.route_resolver import RouteExplorer, RouteResolver
from storm.core.router import Router
from storm.common.services.logger import Logger
from storm.common.execution_context import execution_context

class StormApplication:
    """
    The main application class responsible for bootstrapping the Storm framework.

    Attributes:
        - root_module: The root module of the application.
        - modules: A dictionary to store loaded modules.
        - router: An instance of the Router class to handle route management.
        - logger: A Logger instance for application-level logging.
        - middleware_pipeline: The pipeline that handles middleware execution.
        - interceptor_pipeline: The pipeline that handles interceptor execution.
    """

    def __init__(self, root_module):
        """
        Initialize the StormApplication with the given root module.

        :param root_module: The root module containing controllers, providers, and imports.
        """
        self.root_module = root_module
        self.modules = {}
        self.router = Router()
        self.logger = Logger("StormApplication")
        self.middleware_pipeline = MiddlewarePipeline()
        self.interceptor_pipeline = InterceptorPipeline(global_interceptors=[])
        self._load_modules()
        self._load_controllers()
        self.logger.info(f"Storm application succefully started")

    def add_global_interceptor(self, interceptor_cls):
        """
        Add a global interceptor to the application.

        :param interceptor_cls: The interceptor class to be added as a global interceptor.
        """
        self.interceptor_pipeline.add_global_interceptor(interceptor_cls)

    def add_global_middleware(self, middleware_cls):
        """
        Add global middleware to the application.

        :param middleware_cls: The middleware class to be added as global middleware.
        """
        self.middleware_pipeline.add_global_middleware(middleware_cls)

    def _load_modules(self):
        """
        Load and initialize modules from the root module.
        """
        self.logger.info(f"{self.root_module.__name__} dependencies initialized")
        for module in self.root_module.imports:
            self.modules[module.__name__] = module
            self.logger.info(f"{module.__name__} dependencies initialized")
            self._initialize_module(module)

    def _load_controllers(self):
        """
        Load and register controllers from the root module.
        """
        for module in self.modules.values():
            for controller in module.controllers.values():
                self._register_controller(controller, module)

    def _initialize_module(self, module):
        """
        Initialize a module by setting up its services and controllers.

        :param module: The module to initialize.
        """
        self._initialize_services(module)
        self._initialize_controllers(module)


    def _initialize_controllers(self, module):
        """
        Initialize services within a module by injecting dependencies.

        :param module: The module whose services need initialization.
        """
        for name, controller in module.controllers.items():
            self._inject_init_dependencies(controller, module)
            controller_instance = controller()
            self._inject_dependencies(controller_instance, module)
            module.controllers[name] = controller_instance

    def _initialize_services(self, module):
        """
        Initialize services within a module by injecting dependencies.

        :param module: The module whose services need initialization.
        """
        for name, provider in module.providers.items():
            self._inject_init_dependencies(provider, module)
            service_instance = provider()
            module.providers[name] = service_instance
        
        for name, provider in module.providers.items():
            self._inject_dependencies(provider, module)

    def _inject_dependencies(self, service, module):
        """
        Inject dependencies into a service based on the module's providers.

        :param service: The service instance to inject dependencies into.
        :param module: The module providing the dependencies.
        """
        if hasattr(service, '__annotations__'):
            for attr_name, dependency in service.__annotations__.items():
                if hasattr(dependency, '__injectable__') and dependency.__injectable__:
                    if dependency.__name__ in module.providers.keys():
                        setattr(service, attr_name, module.providers[dependency.__name__])

    def _inject_init_dependencies(self, service_class, module):
        """
        Modify the service class's __init__ method to inject default dependencies from the module.

        :param service_class: The class of the service.
        :param module: The module providing the dependencies.
        """
        # Get the original __init__ method
        original_init = service_class.__init__
        signature = inspect.signature(original_init)
        default_kwargs = {}

        # Collect dependencies for __init__ parameters
        for param_name, param in signature.parameters.items():
            if param_name == "self":  # Skip 'self' parameter
                continue
            dependency_type = param.annotation
            if (
                dependency_type
                and hasattr(dependency_type, '__injectable__')
                and dependency_type.__injectable__
            ):
                
                if dependency_type.__name__ in module.providers.keys():
                    default_kwargs[param_name] = module.providers[dependency_type.__name__]
                else:
                    raise ValueError(f"Dependency {dependency_type.__name__} not found in module providers.")

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            # Merge provided arguments with defaults
            merged_kwargs = {**default_kwargs, **kwargs}
            original_init(self, *args, **merged_kwargs)

        # Replace the __init__ method of the class
        service_class.__init__ = new_init
    
    def _register_controller(self, controller, module):
        """
        Register a controller's routes with the application router.

        :param controller: The controller class to register.
        :param module: The module containing the controller.
        """

        if hasattr(controller, 'on_module_init'):
            controller.on_module_init()
        
        resolver = RouteResolver(self.router)
        explorer = RouteExplorer()
        
        resolver.register_routes(controller, controller.__base_path__, explorer)
        
    async def handle_request(self, method, path, request, response, **request_kwargs):
        """
        Handle an incoming HTTP request by resolving the route and executing middleware and interceptors.

        :param method: The HTTP method (e.g., GET, POST).
        :param path: The URL path of the request.
        :param request: The HttpRequest object representing the incoming request.
        :param response: The HttpResponse object to build the response.
        :param request_kwargs: Additional request parameters.
        :return: A tuple containing the response and its status code.
        """
        try:
            handler, params = self.router.resolve(method, path)
            if not handler:
                raise NotFoundException()
            request_kwargs["params"] = params
            execution_context.set({"request": request_kwargs, "req": request, "response": response})

            modified_request = await self.middleware_pipeline.execute(request_kwargs, lambda req: req)
            content = await self.interceptor_pipeline.execute(modified_request, handler)

            response.update_content(content)
            return response, response.status_code

        except ValueError:
            raise NotFoundException(message=f"Cannot {method} {path}")
        except StormHttpException as e:
            raise e
        except Exception as e:
            self.logger.error(e)
            raise InternalServerErrorException() from e

        finally:
            execution_context.clear()

    async def __call__(self, scope, receive, send):
        """
        ASGI application entry point to handle incoming connections.

        :param scope: The ASGI scope dictionary containing connection information.
        :param receive: The receive callable for the connection.
        :param send: The send callable for the connection.
        """
        if scope['type'] == 'http':
            try:
                request = HttpRequest(scope, receive, send)
                await request.parse_body()

                method, path, request_kwargs = request.get_request_info()
                response = HttpResponse.from_request(request=request, status_code=200)

                response, _ = await self.handle_request(method, path, request, response, **request_kwargs)
            except StormHttpException as exc:
                self.logger.error(exc)
                if exc.status_code == 500:
                    tb = traceback.format_exc()
                    self.logger.error(tb)
                response = HttpResponse.from_error(exc)
            except Exception as exc:
                tb = traceback.format_exc()
                self.logger.error(tb)
                response = HttpResponse.from_error(InternalServerErrorException())
            finally:
                await response.send(send)

    def run(self, host='127.0.0.1', port=8000):
        """
        Start the application server using Uvicorn.

        :param host: The host address to bind the server (default is '127.0.0.1').
        :param port: The port number to bind the server (default is 8000).
        """
        import uvicorn
        uvicorn.run(self, host=host, port=port, log_level='error')

    def shutdown(self):
        """
        Perform shutdown tasks for the application, invoking any onDestroy hooks in modules.
        """
        for module in self.modules.values():
            if hasattr(module, 'onDestroy') and callable(module.onDestroy):
                module.onDestroy()
