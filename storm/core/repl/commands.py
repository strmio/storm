from storm.core.repl.repl_logger import ReplLogger
import time
import os

logger = ReplLogger()

def help():
    """
    Lists available commands in the Storm REPL.
    """
    commands = {
        'help()': 'Show this help message',
        'list_services()': 'List all registered services in the application',
        'list_controllers()': 'List all registered controllers in the application',
    }
    logger.info("Displaying help commands.")
    for command, description in commands.items():
        print(f"{command}: {description}")


def list_services(app):
    """
    Lists all services registered in the application.
    """
    logger.info("Listing services.")
    print("Registered Services:")
    for service in app.modules.values():
        for provider in service.providers:
            print(f" - {provider.__class__.__name__}")


def list_controllers(app):
    """
    Lists all controllers registered in the application.
    """
    logger.info("Listing controllers.")
    print("Registered Controllers:")
    for controller in app.modules.values():
        for ctrl in controller.controllers:
            print(f" - {ctrl.__class__.__name__}")


def reload(app):
    """
    Reloads the application’s modules and services.
    """
    logger.info("Reloading the application.")
    print("Reloading application...")
    app._load_modules()
    print("Application reloaded.")


def show_routes(app):
    """
    Displays all registered routes in the application.
    """
    logger.info("Displaying registered routes.")
    print("Registered Routes:")
    for route in app.router.routes:
        print(f" - {route.method} {route.path}")


def clear():
    """
    Clears the REPL screen.
    """
    logger.info("Clearing screen.")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Screen cleared.")


def eval_code(code, context):
    """
    Evaluates and executes arbitrary Python code within the REPL.
    """
    logger.info(f"Evaluating code: {code}")
    try:
        exec(code, context)
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        print(f"Error executing code: {e}")


def get_service(app, service_name):
    """
    Retrieves a specific service by name from the application context.
    """
    logger.info(f"Retrieving service: {service_name}")
    service = next(
        (provider for module in app.modules.values()
         for provider in module.providers if provider.__class__.__name__ == service_name),
        None
    )
    if service:
        logger.info(f"Service '{service_name}' retrieved successfully.")
        print(f"Service '{service_name}' retrieved successfully.")
        return service
    else:
        logger.warning(f"Service '{service_name}' not found.")
        print(f"Service '{service_name}' not found.")
        return None


def inspect_route(app, path):
    """
    Inspects a specific route by its path, showing handlers and middleware.
    """
    logger.info(f"Inspecting route: {path}")
    route = next(
        (route for route in app.router.routes if route.path == path), None)
    if not route:
        logger.warning(f"No route found for path: {path}")
        print(f"No route found for path: {path}")
        return

    print(f"Inspecting Route: {path}")
    print(f"Method: {route.method}")
    print(f"Handler: {route.handler.__name__}")
    if route.middleware:
        print("Middleware:")
        for mw in route.middleware:
            print(f" - {mw.__class__.__name__}")


def benchmark(command, context):
    """
    Runs a command and displays the execution time for performance analysis.
    """
    logger.info(f"Benchmarking command: {command}")
    start_time = time.time()
    exec(command, context)
    end_time = time.time()
    logger.info(f"Execution time: {end_time - start_time:.4f} seconds")
    print(f"Execution time: {end_time - start_time:.4f} seconds")


def list_modules(app):
    """
    Lists all modules registered in the application.
    """
    logger.info("Listing registered modules.")
    print("Registered Modules:")
    for module in app.imports.values():
        print(f" - {module.__class__.__name__}")
