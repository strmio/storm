import asyncio
from storm.core.interceptor import Interceptor

class CachingInterceptor(Interceptor):
    def __init__(self):
        self.cache = {}

    async def intercept(self, request, next):
        cache_key = request.path
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        response = await next()
        self.cache[cache_key] = response
        return response
