
from storm.common import Module
from modules.notes_module import NotesModule
from modules.users_module import UsersModule


@Module(imports=[UsersModule, NotesModule])
class AppModule:
    pass
