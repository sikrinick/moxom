
class Computer:

    def __init__(self, computer_name: str = "Default"):
        self.name = computer_name

    async def open_app(self, app_name: str = "Test app"):
        print(f"Computer {self.name}. Open app {app_name}")

    def start(self):
        print(f"Computer {self.name} started")

    def shutdown(self):
        print(f"Computer {self.name} shut down")
