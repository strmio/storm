from storm.common.decorators import Get, Post, Body, Query, Param
from storm.common.pipes import ParseIntPipe
from storm.common.decorators.http import Delete
from storm.common.decorators.injectable import Injectable
from storm.common.decorators.module import Module
from storm.common.decorators.controller import Controller
from storm.common.pipes.parse_uuid_pipe import ParseUUIDPipe
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

    def get_users(self, q: str = None):
        # Simulate fetching users from a database or external service
        if q:
            users = [user for user in self.users if q.lower()
                     in user["name"].lower()]
            return {"users": users}
        return {"users": self.users}

    def get_user(self, id):
        # Simulate fetching a user by ID from a database or external service
        users = self.users
        user = next((user for user in users if user["id"] == id), None)
        return {"user": user}

    def get_count(self):
        users = self.users
        return {"users_count": len(users)}

    def get_me(self):
        # Simulate fetching the current user's information
        current_user = {"id": 1, "name": "John Doe",
                        "email": "john.doe@example.com"}
        return {"user": current_user}

    def add_user(self, user):
        self.logger.info(f"Adding user: {user}")
        # Simulate adding a new user to the database or external service
        self.users.append(user)
        return {"status": "ok", "user": user}

    def get_user_by_email(self, email):
        # Simulate fetching a user by email from a database or external service
        users = self.users
        user = next((user for user in users if user["email"] == email), None)
        return {"user": user}

    def delete_user(self, id):
        # Simulate deleting a user from the database or external service
        users = self.users
        user = next((user for user in users if user["id"] == id), None)
        if user:
            users.remove(user)
            return {"status": "ok", "user": user}
        return {"status": "error", "message": "User not found"}

# Define Controller


@Controller("/users")  # Define base path for this controller
class UsersController():

    def __init__(self, users_service: UsersService):
        self.logger = Logger(self.__class__.__name__)
        self.users_service = users_service

    @Get()
    @Query("q", "q")
    async def get_users(self, q):
        return self.users_service.get_users(q)

    @Get("/:id")
    @Param("id")
    async def get_user(self, id):
        self.logger.info(f"Fetching user with ID: {id}")
        return self.users_service.get_user(int(id))

    @Get("/count")
    async def get_users_count(self, ip, host):
        self.logger.info(f"IP: {ip}, Host: {host}")
        return self.users_service.get_count()

    @Post()
    @Body("user")
    async def add_user(self, user):
        return self.users_service.add_user(user)

    @Get("/me")
    async def get_me(self, auth):
        self.logger.info(auth)
        if not auth:
            return {"error": "Unauthorized"}
        return self.users_service.get_me()

    @Delete("/:id")
    async def delete_user(self, id: int = Param("id", ParseIntPipe)):
        self.logger.info(f"Deleting user with ID: {id}, type: {type(id)}")
        return self.users_service.delete_user(id)


@Controller("/users/:user_id/notes")  # Define base path for this controller
class NotesController():

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @Get("/:id")
    async def get_note(self, user_id: int = Param("user_id", ParseIntPipe),
                       id=Param("id", ParseUUIDPipe)):
        return {"note": {"id": str(id), "user_id": user_id, "content": "This is a note."}}

# Define Module


@Module(controllers=[UsersController, NotesController], providers=[UsersService])
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
