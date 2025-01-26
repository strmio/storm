from storm.common.decorators import Get, Post, Body, Query, Param, HttpCode
from storm.common.enums import HttpStatus
from storm.common.exceptions.http import ForbiddenException
from storm.common.pipes import PydanticValidationPipe
from storm.common.decorators.injectable import Injectable
from storm.common.decorators.module import Module
from storm.common.decorators.controller import Controller
from storm.common.pipes.parse_int_pipe import ParseIntPipe
from storm.common.services.logger import Logger
from storm.core.application import StormApplication
from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    name: str
    email: EmailStr
    id: int


# Define Services
@Injectable()
class UsersService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.users: list[UserModel] = [
            UserModel(id=1, name="John Doe", email="john.doe@email.com"),
            UserModel(id=2, name="Jane Smith", email="jane.smith@email.xom"),
        ]

    def get_users(self, q: str = None):
        # Simulate fetching users from a database or external service
        users = [
            user.model_dump()
            for user in self.users
            if not q or q.lower() in user.name.lower()
        ]
        return {"users": users}

    def get_user(self, id):
        # Simulate fetching a user by ID from a database or external service
        users = self.users
        user = next((user for user in users if user.id == id), None)
        return {"user": user.model_dump() if user else None}

    def add_user(self, user):
        self.logger.info(f"Adding user: {user}")
        # Simulate adding a new user to the database or external service
        self.users.append(user)
        return {"status": "ok", "user": user.model_dump()}


# Define Controller
@Controller("/users")  # Define base path for this controller
class UsersController:
    def __init__(self, users_service: UsersService):
        self.logger = Logger(self.__class__.__name__)
        self.users_service = users_service

    @Get()
    @Query("q")
    async def get_users(self, q: str = None):
        return self.users_service.get_users(q)

    @Get("/:id")
    @Param("id", ParseIntPipe)
    async def get_user(self, id):
        self.logger.info(f"Fetching user with ID: {id}")
        return self.users_service.get_user(int(id))

    @Post()
    @HttpCode(HttpStatus.CREATED)
    async def add_user(
        self, user: UserModel = Body(pipe=PydanticValidationPipe(UserModel))
    ):
        return self.users_service.add_user(user)

    @Get("/me")
    async def get_me(self):
        raise ForbiddenException("You are not allowed to access this resource")


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
