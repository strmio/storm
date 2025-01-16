from storm.common.decorators.http import Get, Post
from storm.common.decorators.module import Module
from storm.common.decorators.controller import Controller
from storm.common.services.logger import Logger
from storm.core.application import StormApplication

# Define Controller
@Controller("/users")  # Define base path for this controller
class UsersController():
    
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @Get("/")
    async def get_users(self):
        return {"users": ["John", "Jane"]}

    @Get("/me")
    async def get_me(self):
        return {"users": ["John", "Jane"]}

    @Post()
    async def create_user(self):
        return {"users": ["John", "Jane"]}

    @Post("/stats")
    async def get_users_stats(self):
        return 1 + 1

# Define Module
@Module(controllers=[UsersController], imports=[])
class UsersModule:
    pass

@Module(imports=[UsersModule])
class AppModule:
    pass

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Initialize the application with AppModule
    app = StormApplication(AppModule)

    # Start the application
    app.run()
