from storm.common import Module
from storm.core.application import StormApplication
from services.user_service import UsersService
from services.users_notes_service import UsersNotesService
from controllers.users_controllers import UsersController
from controllers.notes_controllers import NotesController

@Module(controllers=[UsersController], providers=[UsersService])
class UsersModule:
    pass


@Module(controllers=[NotesController], providers=[UsersNotesService, UsersService])
class NotesModule:
    pass


@Module(imports=[UsersModule, NotesModule])
class AppModule:
    pass

# Initialize the application with AppModule
app = StormApplication(AppModule)

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
