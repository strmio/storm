from storm.common import VersioningType
from storm.core import StormApplication

from modules.app_module import AppModule
from settings import get_settings


# Initialize the application with AppModule
app = StormApplication(AppModule, settings=get_settings())

app.enable_versioning({"type": VersioningType.URI})

app.setGlobalPrefix("prefix_app/api")

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
