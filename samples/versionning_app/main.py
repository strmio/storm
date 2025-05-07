from modules.app_module import AppModule
from settings import get_settings

from storm.common import VersioningType
from storm.core import StormApplication

# Initialize the application with AppModule
app = StormApplication(AppModule, settings=get_settings())

# app.enable_versioning({"type": VersioningType.URI})
# app.enable_versioning({"type": VersioningType.HEADER, "header": "X-API-Version"})
app.enable_versioning({"type": VersioningType.MEDIA_TYPE, "key": "v="})

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
