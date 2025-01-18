import json

class HttpRequest:
    """
    A class to parse and encapsulate HTTP request details
    from ASGI scope, receive, and send.
    """

    def __init__(self, scope, receive, send):
        """
        Initialize the HttpRequest object.

        :param scope: The scope of the ASGI connection
        :param receive: The receive channel
        :param send: The send channel
        """
        self.scope = scope
        self.receive = receive
        self.send = send

        # Initialize extracted fields
        self.method = scope.get("method")
        self.path = scope.get("path")
        self.headers = self._parse_headers(scope.get("headers", []))
        self.query_params = self._parse_query_params(scope.get("query_string", b""))
        self.body = None
        self.client_ip = self._parse_client_ip(scope)
        self.host = self.headers.get("host")

    async def parse_body(self):
        """
        Asynchronously parse the body from the receive channel.
        """
        body_content = b""
        while True:
            event = await self.receive()
            if event["type"] == "http.request":
                body_content += event.get("body", b"")
                if not event.get("more_body", False):
                    break
        try:
            self.body = json.loads(body_content.decode("utf-8")) if body_content else {}
        except json.JSONDecodeError:
            self.body = body_content.decode("utf-8") if body_content else ""

    def _parse_headers(self, raw_headers):
        """
        Parse headers from raw scope headers.
        :param raw_headers: List of (key, value) byte tuples
        :return: Dictionary of headers
        """
        return {key.decode("utf-8"): value.decode("utf-8") for key, value in raw_headers}

    def _parse_query_params(self, query_string):
        """
        Parse query parameters from a query string.
        :param query_string: Query string as bytes
        :return: Dictionary of query parameters
        """
        query_params = {}
        if query_string:
            query_string = query_string.decode("utf-8")
            query_params = {
                k: v for k, v in [pair.split("=") for pair in query_string.split("&") if "=" in pair]
            }
        return query_params

    def _parse_client_ip(self, scope):
        """
        Parse the client IP from the ASGI scope.
        :param scope: The scope of the ASGI connection
        :return: Client IP address as a string
        """
        return scope.get("client", [None])[0]

    def get_request_info(self):
        """
        Returns a tuple containing method, path, and request_kwargs.
        
        :return: Tuple (method, path, request_kwargs)
        """
        request_kwargs = {
            "headers": self.headers,
            "query_params": self.query_params,
            "body": self.body,
            "client_ip": self.client_ip,
            "host": self.host,
            "params": {},
        }
        return self.method, self.path, request_kwargs
