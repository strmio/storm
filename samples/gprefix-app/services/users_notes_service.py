from storm.common import Injectable, Logger
from services.users_service import UsersService


@Injectable()
class UsersNotesService:
    _notes = [
        {"id": 1, "user_id": 1, "content": "This is a note."},
        {"id": 2, "user_id": 1, "content": "This is another note."},
        {"id": 3, "user_id": 2, "content": "This is a note for Jane."},
        {"id": 4, "user_id": 2, "content": "This is another note for Jane."},
    ]

    def __init__(self, user_service: UsersService):
        self.logger = Logger(self.__class__.__name__)

    def get_notes(self, user_id):
        # Simulate fetching notes from a database or external service
        user_notes = [note for note in self._notes if note["user_id"] == user_id]
        return {"notes": user_notes}

    def note_by_id(self, user_id, note_id):
        # Simulate fetching a note by ID from a database or external service
        user_notes = self._notes
        note = next((note for note in user_notes if note["id"] == note_id), None)
        return {"note": note}
