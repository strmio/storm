import json
from urllib.parse import parse_qs


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

        # Basic request info
        self.method = scope.get("method")
        self.path = scope.get("path")
        self.raw_path = scope.get("raw_path", b"").decode("utf-8")
        self.scheme = scope.get("scheme", "http")
        self.http_version = scope.get("http_version", "1.1")

        # Headers, query params, and cookies
        self.headers = self._parse_headers(scope.get("headers", []))
        self.query_params = self._parse_query_params(scope.get("query_string", b""))
        self.cookies = self._parse_cookies(self.headers.get("cookie", ""))

        # Client and server information
        self.client = scope.get("client", (None, None))
        self.client_ip = self.client[0]
        self.client_port = self.client[1]
        self.server = scope.get("server", (None, None))
        self.server_host = self.server[0]
        self.server_port = self.server[1]

        # WebSocket-specific attributes
        self.is_websocket = scope.get("type") == "websocket"
        self.subprotocols = scope.get("subprotocols", [])

        # Middleware or framework-injected fields
        self.user = scope.get("user")
        self.auth = scope.get("auth")

        # Request body
        self.body = None

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
        self.body = self._decode_body(body_content)

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
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(query_string.decode("utf-8")).items()}

    def _parse_cookies(self, cookie_header):
        """
        Parse cookies from the Cookie header.
        :param cookie_header: Cookie header as a string
        :return: Dictionary of cookies
        """
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split(";"):
                if "=" in cookie:
                    key, value = cookie.strip().split("=", 1)
                    cookies[key] = value
        return cookies

    def _decode_body(self, body_content):
        """
        Decode the body content based on content type.
        :param body_content: Raw body bytes
        :return: Decoded body (JSON, text, or raw bytes)
        """
        content_type = self.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            try:
                return json.loads(body_content.decode("utf-8")) if body_content else {}
            except json.JSONDecodeError:
                return body_content.decode("utf-8")
        elif "application/x-www-form-urlencoded" in content_type:
            return parse_qs(body_content.decode("utf-8"))
        else:
            return body_content.decode("utf-8") if body_content else ""

    def get_request_info(self):
        """
        Returns a tuple containing method, path, and request_kwargs.
        :return: Tuple (method, path, request_kwargs)
        """
        request_kwargs = {
            "headers": self.headers,
            "query_params": self.query_params,
            "cookies": self.cookies,
            "body": self.body,
            "client_ip": self.client_ip,
            "client_port": self.client_port,
            "server_host": self.server_host,
            "server_port": self.server_port,
            "scheme": self.scheme,
            "http_version": self.http_version,
            "is_websocket": self.is_websocket,
            "subprotocols": self.subprotocols,
            "user": self.user,
            "auth": self.auth,
            "params": {},
        }
        return self.method, self.path, request_kwargs
