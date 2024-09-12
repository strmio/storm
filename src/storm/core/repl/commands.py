import os

def help():
    """
    Lists available commands in the Storm REPL.
    """
    commands = {
        'help()': 'Show this help message',
        'list_services()': 'List all registered services in the application',
        'list_controllers()': 'List all registered controllers in the application',
    }
    for command, description in commands.items():
        print(f"{command}: {description}")

def list_services(app):
    """
    Lists all services registered in the application.
    
    :param app: The Storm application instance.
    """
    print("Registered Services:")
    for service in app.modules.values():
        for provider in service.providers:
            print(f" - {provider.__class__.__name__}")

def list_controllers(app):
    """
    Lists all controllers registered in the application.
    
    :param app: The Storm application instance.
    """
    print("Registered Controllers:")
    for controller in app.modules.values():
        for ctrl in controller.controllers:
            print(f" - {ctrl.__class__.__name__}")

def reload(app):
    """
    Reloads the application’s modules and services.
    
    :param app: The Storm application instance.
    """
    print("Reloading application...")
    app._load_modules()
    print("Application reloaded.")

def show_routes(app):
    """
    Displays all registered routes in the application.

    :param app: The Storm application instance.
    """
    print("Registered Routes:")
    for route in app.router.routes:
        print(f" - {route.method} {route.path}")

def clear():
    """
    Clears the REPL screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Screen cleared.")


def eval_code(code, context):
    """
    Evaluates and executes arbitrary Python code within the REPL.

    :param code: The Python code to evaluate.
    :param context: The REPL context, usually a dictionary with available variables.
    """
    try:
        exec(code, context)
    except Exception as e:
        print(f"Error executing code: {e}")


def get_service(app, service_name):
    """
    Retrieves a specific service by name from the application context.

    :param app: The Storm application instance.
    :param service_name: The name of the service to retrieve.
    :return: The service instance or a message if not found.
    """
    service = next(
        (provider for module in app.modules.values() for provider in module.providers if provider.__class__.__name__ == service_name),
        None
    )
    if service:
        print(f"Service '{service_name}' retrieved successfully.")
        return service
    else:
        print(f"Service '{service_name}' not found.")
        return None


def inspect_route(app, path):
    """
    Inspects a specific route by its path, showing handlers and middleware.
    
    :param app: The Storm application instance.
    :param path: The route path to inspect.
    """
    route = next((route for route in app.router.routes if route.path == path), None)
    if not route:
        print(f"No route found for path: {path}")
        return

    print(f"Inspecting Route: {path}")
    print(f"Method: {route.method}")
    print(f"Handler: {route.handler.__name__}")
    if route.middleware:
        print("Middleware:")
        for mw in route.middleware:
            print(f" - {mw.__class__.__name__}")
