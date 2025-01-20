from storm.common.decorators.controller import Controller
from storm.common.decorators.http import Get
from storm.common.decorators.param import Param
from storm.common.pipes.parse_int_pipe import ParseIntPipe
from storm.common.services.logger import Logger
from services.users_notes_service import UsersNotesService
from services.user_service import UsersService

@Controller("/users/:user_id/notes")  # Define base path for this controller
class NotesController():
    notes_service: UsersNotesService
    user_service: UsersService
    
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @Get("/:id")
    async def get_note(self, user_id: int = Param("user_id", ParseIntPipe),
                       id=Param("id", ParseIntPipe)):
        return self.notes_service.note_by_id(user_id, id)
    
    @Get()
    async def get_notes(self, user_id: int = Param("user_id", ParseIntPipe)):
        return self.notes_service.get_notes(user_id)
