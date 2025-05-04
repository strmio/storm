import inspect
from functools import wraps
from rich import print
from storm.common.enums.content_type import ContentType
from storm.common.enums.http_headers import HttpHeaders
from storm.common.enums.http_method import HttpMethod
from storm.common.enums.http_status import HttpStatus
from storm.common.enums.versioning_type import VersioningType
from storm.common.exceptions.exception import StormHttpException
from storm.common.exceptions.http import (
    InternalServerErrorException,
    NotFoundException,
    PreconditionFailedException,
)
from storm.core.adapters.http_request import HttpRequest
from storm.core.adapters.http_response import HttpResponse
from storm.core.appliction_config import ApplicationConfig
from storm.core.exceptions.exception_handler import ExceptionHandler
from storm.core.exceptions.traceback_handler import TracebackHandler
from storm.core.helpers.helpers import strip_etag_quotes
from storm.core.interceptor_pipeline import InterceptorPipeline
from storm.core.interfaces.version_options_interface import VersioningOptions
from storm.core.middleware_pipeline import MiddlewarePipeline
from storm.core.repl.repl_manager import ReplManager
from storm.core.resolvers.route_resolver import RouteExplorer, RouteResolver
from storm.core.router import Router
from storm.common.services.logger import Logger
from storm.common.execution_context import execution_context
from storm.core.services.system_monitor import SystemMonitor
from storm.core.settings import AppSettings as Settings, get_settings
from storm.core.context import AppContext


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

    def __init__(self, root_module, settings: Settings = get_settings()):
        """
        Initialize the StormApplication with the given root module.

        :param root_module: The root module containing controllers, providers, and imports.
        :param app_config: Optional dictionary for application configuration.
        """
        AppContext.set_settings(settings)
        self.app_config = ApplicationConfig()
        self._exception_handler = ExceptionHandler()
        self._traceback_handler = TracebackHandler()
        self.middleware_pipeline = MiddlewarePipeline()
        self.interceptor_pipeline = InterceptorPipeline(global_interceptors=[])
        self.router = Router(self.app_config)
        self._logger = Logger(self.__class__.__name__)
        self.root_module = root_module
        self.settings = settings
        self.modules = {root_module.__name__: root_module}
        self._print_banner()
        self._logger.info("Starting up Storm application.")
        if self.settings.sys_monitoring_enabled:
            self.system_monitor = SystemMonitor(self.settings.sys_monitoring_interval)
            self.system_monitor.start()
        else:
            self.system_monitor = None

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

    def enable_versioning(
        self, verioning_options: VersioningOptions = {type: VersioningType.URI}
    ):
        """
        Enables versioning for the application with the specified options.


        :verioning_options (VersioningOptions, optional): Configuration options for versioning.
                Defaults to { type: VersioningType.URI }.
        """
        self.app_config.enable_versioning(verioning_options)

    def setGlobalPrefix(self, prefix: str):
        """
        Set a global prefix for all routes in the application.

        :param prefix: The prefix to be added to all routes.
        """
        self.app_config.set_global_prefix(self.router.normalize_path(prefix))

    def _load_modules(self):
        """
        Load and initialize modules from the root module.
        """

        self._logger.info(f"{self.root_module.__name__} dependencies initialized")
        self._initialize_module(self.root_module)
        for module in self.root_module.imports:
            self.modules[module.__name__] = module
            self._logger.info(f"{module.__name__} dependencies initialized")
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
        if hasattr(service, "__annotations__"):
            for attr_name, dependency in service.__annotations__.items():
                if hasattr(dependency, "__injectable__") and dependency.__injectable__:
                    if dependency.__name__ in module.providers.keys():
                        setattr(
                            service, attr_name, module.providers[dependency.__name__]
                        )

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
                and hasattr(dependency_type, "__injectable__")
                and dependency_type.__injectable__
            ):
                if dependency_type.__name__ in module.providers.keys():
                    setattr(
                        service_class,
                        param_name,
                        module.providers[dependency_type.__name__],
                    )
                    default_kwargs[param_name] = module.providers[
                        dependency_type.__name__
                    ]
                else:
                    raise ValueError(
                        f"Dependency {dependency_type.__name__} not found in module providers."
                    )

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

        if hasattr(controller, "on_module_init"):
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
            handler, params = self.router.resolve(method, path, request=request)
            if not handler:
                raise NotFoundException()

            request.set_params(params)

            execution_context.set({"request": request, "response": response})

            await self.middleware_pipeline.execute(request_kwargs, lambda req: req)
            content = await self.interceptor_pipeline.execute(handler)

            response.update_content(content)
            return response, response.status_code

        except ValueError:
            raise NotFoundException(message=f"Cannot {method} {path}")
        except StormHttpException as e:
            raise e
        except Exception as e:
            self._exception_handler.handle_exception(e)
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
        if scope["type"] == "http":
            try:
                request = HttpRequest(scope, receive, send)
                await request.parse_body()

                method, path, request_kwargs = request.get_request_info()
                response = HttpResponse.from_request(request=request)

                response, _ = await self.handle_request(
                    method, path, request, response, **request_kwargs
                )

                current_etag = response.set_etag()

                if request.method in (
                    HttpMethod.PUT,
                    HttpMethod.PATCH,
                    HttpMethod.DELETE,
                ):
                    client_etag = request.get_if_match()
                    if client_etag and strip_etag_quotes(
                        client_etag
                    ) != strip_etag_quotes(current_etag):
                        raise PreconditionFailedException()

                # If-None-Match (for cache validation on GET)
                elif request.method == HttpMethod.GET:
                    client_etag = request.get_if_none_match()
                    if client_etag and strip_etag_quotes(
                        client_etag
                    ) == strip_etag_quotes(current_etag):
                        response.update_status_code(HttpStatus.NOT_MODIFIED)
                        response.update_content(None)  # No body for 304
                        response.update_headers(
                            {HttpHeaders.CONTENT_TYPE: ContentType.PLAIN}
                        )

            except StormHttpException as exc:
                # self.__exception_handler.handle_exception(exc)
                if exc.status_code == HttpStatus.INTERNAL_SERVER_ERROR:
                    self._traceback_handler.handle_exception(exc, exc.__traceback__)
                response = HttpResponse.from_error(exc)
            except Exception as exc:
                self._exception_handler.handle_exception(InternalServerErrorException())
                self._traceback_handler.handle_exception(
                    exc, exc.__traceback__, InternalServerErrorException
                )
                response = HttpResponse.from_error(InternalServerErrorException())
            finally:
                if response:
                    await response.send(send)
        elif scope["type"] == "lifespan":
            # Handle startup and shutdown events
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    self.shutdown()
                    await send({"type": "lifespan.shutdown.complete"})
                    break

    def run(self, host="127.0.0.1", port=8000):
        """
        Start the application server using Uvicorn.

        :param host: The host address to bind the server (default is '127.0.0.1').
        :param port: The port number to bind the server (default is 8000).
        """
        import uvicorn
        import signal

        def handle_shutdown(signal_number, frame):
            self._logger.info(f"Received shutdown signal: {signal_number}")
            self.shutdown()

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, handle_shutdown)  # Handle Ctrl+C
        # Handle termination signals
        signal.signal(signal.SIGTERM, handle_shutdown)

        try:
            self._initialize_application()
            uvicorn.run(
                self,
                host=host,
                port=port,
                log_level="error",
                server_header=False,
                date_header=False,
            )
        except Exception as e:
            self._exception_handler.handle_exception(
                f"Error while running the server: {e}"
            )
            self._traceback_handler.handle_exception(
                e, e.__traceback__, InternalServerErrorException
            )
        finally:
            self.shutdown()

    def _initialize_application(self):
        """
        Initializes the Storm application by loading necessary modules and controllers,
        setting up the REPL manager if enabled, and marking the application as started.

        This method performs the following steps:
        1. Loads application modules.
        2. Loads application controllers.
        3. Initializes the REPL (Read-Eval-Print Loop) manager if REPL is enabled in settings.
        4. Logs the successful startup of the application.

        Attributes:
            self._shutdown_called (bool): Indicates whether the application shutdown has been called.
            self.repl_manager (ReplManager or None): The REPL manager instance if enabled, otherwise None.

        Raises:
            Any exceptions raised during module or controller loading will propagate.
        """
        self._load_modules()
        self._load_controllers()
        self._shutdown_called = False

        # Initialize REPL Manager
        if self.settings.repl_enabled:
            self.repl_manager = ReplManager(self, self.system_monitor)
            self.repl_manager.start()
        else:
            self.repl_manager = None
        self._logger.info("Storm application succefully started")

    def _handle_shutdown(self, signal_number, frame):
        """
        Handle shutdown signals like SIGINT and SIGTERM.
        """
        self._logger.info(f"Received shutdown signal: {signal_number}")
        self.shutdown()

    def shutdown(self, shutdown_number=None, frame=None):
        """
        Perform shutdown tasks for the application, including stopping the REPL manager.
        """
        if self._shutdown_called:
            return
        self._shutdown_called = True
        self._logger.info("Shutting down Storm application.")
        for module_name, module in self.modules.items():
            if hasattr(module, "onDestroy") and callable(module.onDestroy):
                try:
                    self._logger.info(
                        f"Executing onDestroy hook for module: {module_name}"
                    )
                    module.onDestroy()
                except Exception as e:
                    self._logger.error(
                        f"Error during onDestroy of module {module_name}: {e}"
                    )

        # Stop the REPL manager

        if self.repl_manager:
            self._logger.info("Stopping REPL manager.")
            self.repl_manager.shutdown()

        if self.system_monitor:
            self._logger.info("Stopping system monitor.")
            self.system_monitor.shutdown()

        self._logger.info("Storm application shutdown complete.\n")

    @staticmethod
    def _get_version(package: str) -> str:
        try:
            import importlib.metadata

            return importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            return "Not installed"

    def info(self):
        """
        Displays system and Storm CLI environment information.
        """
        import platform

        print("[bold yellow][System Information][/bold yellow]")
        print(f"OS Version         : {platform.system()} {platform.release()}")
        print(f"Python Version     : {platform.python_version()}")

        print("\n[bold yellow][Storm][/bold yellow]")
        print(f"Storm Version  : {self._get_version('storm')}\n")

    # banner printing

    def _print_banner(self):
        """
        Print the application banner.
        """
        if self.settings.banner_enabled:
            try:
                with open(self.settings.banner_file, "r") as f:
                    print()
                    banner = f.read()
                    print(f"[bold red]{banner}[/bold red]")

            except FileNotFoundError:
                self._logger.warning(
                    f"Banner file {self.settings.banner_file} not found. Skipping banner display."
                )

        if self.settings.sys_info_enabled:
            self.info()
