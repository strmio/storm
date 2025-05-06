from controllers.users_controllers import UsersController
from services.users_service import UsersService

from storm.common import Module


@Module(controllers=[UsersController], providers=[UsersService])
class UsersModule:
    pass
