from storm.common import Get
from storm.common import Module
from storm.common import Controller
from storm.common import Logger
from storm.core import StormApplication

from rx import from_iterable
from rx.operators import map, filter, to_list, take
# Define Controller


@Controller("/process")
class ProcessController():

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    @Get()
    async def process(self):
        # Define a stream of numbers
        numbers = from_iterable(range(1, 100000))  # Stream: [1, 2, ..., 10]

        # Apply RxPy operations
        result = (
            numbers.pipe(
                filter(lambda x: x % 2 == 0),  # Keep only even numbers
                map(lambda x: x * x),          # Square each number
                take(1000),                    # Take only the first 1000 numbers
                to_list()                      # Collect the result into a list
            )
        )

        # Convert the Observable into a Python list and return
        return await result
# Define Module


@Module(controllers=[ProcessController], imports=[])
class UsersModule:
    pass


@Module(imports=[UsersModule])
class AppModule:
    pass


# Initialize the application with AppModule
app = StormApplication(AppModule)

# Create the Storm Application and Run the Server
if __name__ == "__main__":

    # Start the application
    app.run()
