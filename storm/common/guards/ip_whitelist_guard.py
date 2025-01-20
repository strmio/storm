from storm.core.guards import Guard

class IPWhitelistGuard(Guard):
    def __init__(self, allowed_ips):
        self.allowed_ips = allowed_ips

    async def can_activate(self, request, metadata=None):
        client_ip = getattr(request, "ip", None)
        return client_ip in self.allowed_ips
