from typing import List
from storm.common import (
    Body,
    Controller,
    Delete,
    Get,
    Post,
    Headers,
    Param,
    Query,
    Version,
)
from storm.common import ParseIntPipe, UnauthorizedException
from storm.common import Logger, OnModuleInit, Host, Ip
from services.users_service import UsersService


@Controller("users/")  # Define base path for this controller
class UsersController(OnModuleInit):
    users_service: UsersService

    def __init__(self):
        self._logger = Logger(self.__class__.__name__)

    def on_module_init(self):
        self._logger.info("UsersController initialized.")

    @Get()
    @Version("1")
    async def get_users_v1(self) -> List[dict]:
        return self.users_service.get_users()

    @Get()
    @Version("2")
    @Query("q")
    async def get_users_v2(self, q: str) -> List[dict]:
        return self.users_service.get_users_v2(q)

    @Get("/:id")
    async def get_user(self, id: str = Param("id", ParseIntPipe)):
        self._logger.info(f"Fetching user with ID: {id}")
        return self.users_service.get_user(id)

    @Get("/count")
    @Ip("ip")
    @Host("host")
    async def get_users_count(self, ip, host):
        self._logger.info(f"IP: {ip}, Host: {host}")
        return self.users_service.get_count()

    @Post()
    @Body()
    async def add_user(self, body):
        return self.users_service.add_user(body)

    @Get("/me")
    async def get_me(self, auth: str = Headers(header_name="authorization")):
        self._logger.info(auth)
        if not auth:
            raise UnauthorizedException()
        return self.users_service.get_me()

    @Delete("/:note_id")
    async def delete_user(self, id: int = Param("note_id", ParseIntPipe)):
        self._logger.info(f"Deleting user with ID: {id}")
        return self.users_service.delete_user(id)
