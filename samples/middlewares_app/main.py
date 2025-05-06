from modules.app_module import AppModule

from storm.core import StormApplication

# Initialize the application with AppModule
app = StormApplication(AppModule)

# Create the Storm Application and Run the Server
if __name__ == "__main__":
    # Start the application
    app.run()
