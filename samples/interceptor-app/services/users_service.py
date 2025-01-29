from storm.common import Injectable, NotFoundException, Logger, OnModuleInit
import rx
from rx import operators as ops


@Injectable()
class UsersService(OnModuleInit):
    _users = [
        {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
        {"id": 3, "name": "Alice Johnson", "email": "alice.johnson@example.com"},
        {"id": 4, "name": "Bob Brown", "email": "bob.brown@example.com"},
    ]

    def __init__(
        self,
    ):
        self.logger = Logger(self.__class__.__name__)

    def on_module_init(self):
        self.logger.info("UsersService initialized 100.")

    def get_users(self, q: str = None):
        # Create an observable from the users list
        return rx.from_(self._users).pipe(
            ops.filter(lambda user: not q or q.lower() in user["name"].lower()),
            ops.to_list(),  # Convert the filtered users back into a list
        )

    def get_user(self, id):
        # Simulate fetching a user by ID from a database or external service
        user = next((user for user in self._users if user["id"] == id), None)
        if not user:
            raise NotFoundException(f"User with ID {id} not found.")
        return user

    def get_count(self):
        return {"users_count": len(self._users)}

    def get_me(self):
        # Simulate fetching the current user's information
        current_user = {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}
        return {"user": current_user}

    def add_user(self, user):
        self.logger.info(f"Adding user: {user}")
        # Simulate adding a new user to the database or external service
        self._users.append(user)
        # self.user_added_subject.on_next(user)  # Emit the added user through the Subject
        return rx.of(user).pipe(
            ops.map(lambda u: {"status": "ok", "user": u})  # Transform user into a dict
        )

    def get_user_by_email(self, email):
        # Simulate fetching a user by email from a database or external service
        user = next((user for user in self._users if user["email"] == email), None)
        return user

    def delete_user(self, id):
        # Simulate deleting a user from the database or external service
        users = self._users
        user = next((user for user in users if user["id"] == id), None)
        if user:
            users.remove(user)
            return {"status": "ok", "user": user}
        raise NotFoundException(f"User with ID {id} not found.")
