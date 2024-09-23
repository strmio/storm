from storm.core.application import StormApplication
from storm.core.repl.repl import StormRepl
from storm.common.decorators.module import Module

# Define a service
class TodoService:
    def __init__(self):
        self.todos = []

    def add(self, todo):
        self.todos.append(todo)

    def get_all(self):
        return self.todos

# Define the module
@Module(
    providers=[TodoService]
)
class TodoModule:
    pass

# Define the module
@Module(imports=[TodoModule])
class AppModule:
    pass

app = StormApplication(root_module=AppModule)

# Initialize the application
app = StormApplication(root_module=AppModule)

if __name__ == "__main__":
        StormRepl(app).start()
