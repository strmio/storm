from storm.common.decorators.body import Body
from storm.common.decorators.controller import Controller
from storm.common.decorators import Delete, Get, Post, Param
from storm.common.decorators.query_params import Query
from storm.common.pipes.parse_int_pipe import ParseIntPipe
from storm.common.services.logger import Logger
from storm.core.hooks.hooks import OnModuleInit
from services.user_service import UsersService

@Controller("/users")  # Define base path for this controller
class UsersController(OnModuleInit):

    users_service: UsersService
    _logger: Logger = Logger("UsersController")
    

    def on_module_init(self):
        self._logger.info("UsersController initialized.")

    @Get()
    @Query("q")
    async def get_users(self, q):
        return self.users_service.get_users(q)

    @Get("/:id")
    @Param("id", ParseIntPipe)
    async def get_user(self, id):
        self._logger.info(f"Fetching user with ID: {id}")
        return self.users_service.get_user(id)

    @Get("/count")
    async def get_users_count(self, ip, host):
        self._logger.info(f"IP: {ip}, Host: {host}")
        return self.users_service.get_count()

    @Post()
    @Body()
    async def add_user(self, body):
        return self.users_service.add_user(body)

    @Get("/me")
    async def get_me(self, auth):
        self._logger.info(auth)
        if not auth:
            return {"error": "Unauthorized"}
        return self.users_service.get_me()

    @Delete("/:id")
    async def delete_user(self, id: int = Param("id", ParseIntPipe)):
        self._logger.info(f"Deleting user with ID: {id}")
        return self.users_service.delete_user(id)
