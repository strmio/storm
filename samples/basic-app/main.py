from storm.common.decorators.controller import Controller
from storm.common.decorators.http import Get, Post
from storm.common.decorators.module import Module
from storm.common.services.logger import Logger
from storm.core.application import StormApplication

# Define Controller


@Controller("/users/")  # Define base path for this controller
class UsersController:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @Get("/")
    async def get_users(self):
        # Simulate fetching users from a database
        users = [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
        return {"users": users}

    @Get("/me")
    async def get_me(self):
        # Simulate fetching the current user's information
        current_user = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        return {"user": current_user}

    @Post()
    async def create_user(self):
        # Simulate creating a new user
        new_user = {"id": 3, "name": "Alice Johnson", "email": "alice@example.com"}
        # Normally, you would save the new user to the database here
        return {"message": "User created successfully", "user": new_user}

    @Post("/stats")
    async def get_users_stats(self):
        # Simulate fetching user statistics
        user_stats = {"total_users": 2, "active_users": 2, "inactive_users": 0}
        return {"stats": user_stats}


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
