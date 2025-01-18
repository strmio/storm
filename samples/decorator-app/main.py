from storm.common.decorators import Get, Post, Body
from storm.common.decorators.injectable import Injectable
from storm.common.decorators.module import Module
from storm.common.decorators.controller import Controller
from storm.common.services.logger import Logger
from storm.core.application import StormApplication

# Define Controller
@Injectable()
class UsersService():
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.users = [
            {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
            {"id": 3, "name": "Alice Johnson", "email": "alice.johnson@example.com"},
            {"id": 4, "name": "Bob Brown", "email": "bob.brown@example.com"}
        ]
    
    def get_users(self):
        # Simulate fetching users from a database or external service
        return {"users": self.users}

    def get_user(self, id):
        # Simulate fetching a user by ID from a database or external service
        users = self.users
        user = next((user for user in users if user["id"] == id), None)
        return {"user": user}

    def get_count(self):
        users = self.users
        return {"users_count": len(users)}

    def add_user(self, user):
        self.logger.info(f"Adding user: {user}")
        # Simulate adding a new user to the database or external service
        self.users.append(user)
        return {"status": "ok", "user": user}
    

# Define Controller
@Controller("/users")  # Define base path for this controller
class UsersController():
    
    def __init__(self, users_service: UsersService):
        self.logger = Logger(self.__class__.__name__)
        self.users_service = users_service

    @Get()
    async def get_users(self):
        return self.users_service.get_users()
    
    @Get("/:id")
    async def get_user(self):
        return self.users_service.get_user(1)

    @Get("/count")
    async def get_users_count(self):
        return self.users_service.get_count()

    @Post()
    @Body("user")
    async def add_user(self, user):
        return self.users_service.add_user(user)

# Define Module
@Module(controllers=[UsersController], providers=[UsersService])
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
