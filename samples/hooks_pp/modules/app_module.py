from modules.notes_module import NotesModule
from modules.users_module import UsersModule

from storm.common import Module


@Module(imports=[UsersModule, NotesModule])
class AppModule:
    pass
