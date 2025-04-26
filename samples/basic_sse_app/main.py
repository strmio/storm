import asyncio
from storm.common import Controller, Query, Module, Sse, Get
from storm.core import StormApplication
from settings import get_settings


@Controller("/events")
class EventsController:
    @Sse("/sse")
    async def send_events(self):
        async def generator():
            count = 0
            while count < 10:
                await asyncio.sleep(0.5)
                yield {"data": {"message": f"Update #{count}"}}
                count += 1

        return generator()

    @Sse("/sse_numbers")
    async def send_numbers(self):
        async def generator():
            number = 0
            while number < 5:
                await asyncio.sleep(1)
                yield {"data": {"number": number}}
                number += 1

        return generator()

    @Sse("/sse_time")
    @Query("q")
    async def send_time(self, q: str = None):
        async def generator():
            import datetime

            for _ in range(5):
                await asyncio.sleep(1)
                now = datetime.datetime.now().isoformat()
                yield {"data": {"timestamp": now}}

        return generator()

    @Get("/list")
    async def list_events(self):
        return {"events": ["sse", "sse_numbers", "sse_time"]}


@Module(controllers=[EventsController])
class AppModule:
    pass


# Initialize the application with AppModule
app = StormApplication(AppModule, settings=get_settings())

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
