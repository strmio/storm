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
    app._load_modules()  # Assume a private method exists to reload modules
    print("Application reloaded.")
