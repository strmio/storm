from storm.common import Controller, Module, Get, Post, Logger, Query
from storm.core import StormApplication
from settings import get_settings

import duckdb
from storm.common import Injectable


@Injectable()
class DatabaseService:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.logger.info("DatabaseService initialized.")
        self.conn = duckdb.connect(database=":memory:")
        self.logger.info("Creating table if it doesn't exist.")
        self.conn.execute("""
            CREATE SEQUENCE user_id_seq;
            CREATE TABLE users (
                id INTEGER DEFAULT nextval('user_id_seq'),
                name TEXT
            );
        """)

    def execute(self, query: str, params=None):
        if params is None:
            params = []
        return self.conn.execute(query, params)

    def fetchall(self, query: str, params=None):
        if params is None:
            params = []
        result = self.conn.execute(query, params)
        return result.fetchall()

    def fetchone(self, query: str, params=None):
        if params is None:
            params = []
        result = self.conn.execute(query, params)
        return result.fetchone()

    def close(self):
        self.conn.close()


@Controller("/users")
class UsersController:
    database_service: DatabaseService  # Will be injected automatically

    @Post()
    async def insert_user(self):
        self.database_service.execute("""
            INSERT INTO users (name) VALUES ('Alice'), ('Bob')
        """)
        return {"message": "Inserted users."}

    @Get()
    @Query("q")
    async def list_users(self, q: str = None):
        if q:
            query = "SELECT * FROM users WHERE name LIKE $1"
            params = [f"%{q}%"]
        else:
            query = "SELECT * FROM users"
            params = []

        users = self.database_service.fetchall(query, params)
        return {"users": users}


@Module(controllers=[UsersController], providers=[DatabaseService])
class UsersModule:
    pass


# Initialize the application with UsersModule
@Module(imports=[UsersModule])
class AppModule:
    pass


# Initialize the application with AppModule
app = StormApplication(AppModule, settings=get_settings())

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
