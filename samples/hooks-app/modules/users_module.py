
from storm.common import Module
from controllers.users_controllers import UsersController
from services.users_service import UsersService


@Module(controllers=[UsersController], providers=[UsersService])
class UsersModule:
    pass