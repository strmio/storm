import logging
from storm.core.interceptor import Interceptor

logger = logging.getLogger(__name__)

class ErrorHandlingInterceptor(Interceptor):
    async def intercept(self, request, next):
        try:
            return await next()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return {"error": str(e)}
