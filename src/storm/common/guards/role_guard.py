from storm.core.guards import Guard

class RoleGuard(Guard):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    async def can_activate(self, request, metadata=None):
        user_role = getattr(request, "role", None)
        return user_role in self.allowed_roles
