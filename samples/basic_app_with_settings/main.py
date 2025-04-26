from storm.common.decorators.http import Get
from storm.common.decorators.injectable import Injectable
from storm.common.decorators.module import Module
from storm.common.decorators.controller import Controller
from storm.common.services.logger import Logger
from storm.core.application import StormApplication
from settings import get_settings


# Define Controller
@Injectable()
class UsersService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def get_users(self):
        return {"users": ["John", "Jane"]}

    def get_count(self):
        return {"users_count": 1000 + 1}


# Define Controller
@Controller("/users")  # Define base path for this controller
class UsersController:
    def __init__(self, users_service: UsersService):
        self.logger = Logger(self.__class__.__name__)
        self.users_service = users_service

    @Get("/")
    async def get_users(self):
        return self.users_service.get_users()

    @Get("/count")
    async def get_users_count(self):
        return self.users_service.get_count()


# Define Module
@Module(controllers=[UsersController], providers=[UsersService])
class UsersModule:
    pass


@Module(imports=[UsersModule])
class AppModule:
    pass


# Initialize the application with AppModule
app = StormApplication(AppModule, settings=get_settings())

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
    print(app.settings)
