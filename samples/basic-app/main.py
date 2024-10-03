from storm.common.decorators.http import Get
from storm.common.decorators.module import Module
from storm.common.decorators.controller import Controller
from storm.core.application import StormApplication

# Define Controller
@Controller("/users")  # Define base path for this controller
class UsersController():

    @Get("/")
    async def get_users(self, request):
        return {"users": ["John", "Jane"]}

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
