from storm.core.guards import Guard
from datetime import datetime

class TimeBasedGuard(Guard):
    def __init__(self, start_hour, end_hour, time_provider=datetime.now):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.time_provider = time_provider

    async def can_activate(self, request, metadata=None):
        current_hour = self.time_provider().hour
        return self.start_hour <= current_hour < self.end_hour
