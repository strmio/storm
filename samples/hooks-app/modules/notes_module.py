from storm.common import Module
from controllers.notes_controllers import NotesController
from services.users_notes_service import UsersNotesService
from services.users_service import UsersService


@Module(controllers=[NotesController], providers=[UsersNotesService, UsersService])
class NotesModule:
    pass