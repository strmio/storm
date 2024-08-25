import logging
from storm.core.interceptors import Interceptor

logger = logging.getLogger(__name__)

class LoggingInterceptor(Interceptor):
    async def intercept(self, request, next):
        logger.info(f"Request received: {request.path}")
        response = await next()
        logger.info(f"Response sent: {response}")
        return response
