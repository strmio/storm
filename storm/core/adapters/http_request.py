import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs
from enum import StrEnum
from storm.common.enums.http_headers import HttpHeaders


class HttpRequestEnums(StrEnum):
    """
    Enums to avoid magic strings in HttpRequest.
    """

    CONTENT_TYPE = "content-type"
    APPLICATION_JSON = "application/json"
    APPLICATION_FORM = "application/x-www-form-urlencoded"
    COOKIE = "cookie"
    HTTP_REQUEST = "http.request"
    METHOD = "method"
    PATH = "path"
    RAW_PATH = "raw_path"
    SCHEME = "scheme"
    HTTP_VERSION = "http_version"
    HEADERS = "headers"
    QUERY_STRING = "query_string"
    CLIENT = "client"
    SERVER = "server"
    TYPE = "type"
    WEBSOCKET = "websocket"
    SUBPROTOCOLS = "subprotocols"
    USER = "user"
    AUTH = "auth"


class HttpRequest:
    """
    A class to parse and encapsulate HTTP request details
    from ASGI scope, receive, and send.
    """

    def __init__(
        self,
        scope: Dict[str, Any],
        receive: Callable[[], Any],
        send: Callable[[Dict[str, Any]], None],
    ):
        """
        Initialize the HttpRequest object.

        :param scope: The scope of the ASGI connection
        :param receive: The receive channel
        :param send: The send channel
        """
        self.scope: Dict[str, Any] = scope
        self.receive: Callable[[], Any] = receive
        self.send: Callable[[Dict[str, Any]], None] = send
        self.params: Optional[Dict[str, Any]] = None

        # Basic request info
        self.method: Optional[str] = scope.get(HttpRequestEnums.METHOD)
        self.path: Optional[str] = scope.get(HttpRequestEnums.PATH)
        self.raw_path: str = scope.get(HttpRequestEnums.RAW_PATH, b"").decode("utf-8")
        self.scheme: str = scope.get(HttpRequestEnums.SCHEME, "http")
        self.http_version: str = scope.get(HttpRequestEnums.HTTP_VERSION, "1.1")

        # Headers, query params, and cookies
        self.headers: Dict[str, str] = self._parse_headers(
            scope.get(HttpRequestEnums.HEADERS, [])
        )
        self.query_params: Dict[str, Union[str, List[str]]] = self._parse_query_params(
            scope.get(HttpRequestEnums.QUERY_STRING, b"")
        )
        self.cookies: Dict[str, str] = self._parse_cookies(
            self.headers.get(HttpRequestEnums.COOKIE, "")
        )

        # Client and server information
        self.client: Tuple[Optional[str], Optional[int]] = scope.get(
            HttpRequestEnums.CLIENT, (None, None)
        )
        (ip, port) = self.client
        self.client_ip: Optional[str] = ip
        self.client_port: Optional[int] = port

        self.server: Tuple[Optional[str], Optional[int]] = scope.get(
            HttpRequestEnums.SERVER, (None, None)
        )
        (ip, port) = self.server
        self.server_host: Optional[str] = ip
        self.server_port: Optional[int] = port

        # WebSocket-specific attributes
        self.is_websocket: bool = (
            scope.get(HttpRequestEnums.TYPE) == HttpRequestEnums.WEBSOCKET
        )
        self.subprotocols: List[str] = scope.get(HttpRequestEnums.SUBPROTOCOLS, [])

        # Middleware or framework-injected fields
        self.user: Optional[Any] = scope.get(HttpRequestEnums.USER)
        self.auth: Optional[Any] = scope.get(HttpRequestEnums.AUTH)

        # Request body
        self.body: Optional[Union[str, Dict[str, Any], List[Any]]] = None

    async def parse_body(self) -> None:
        """
        Asynchronously parse the body from the receive channel.
        """
        body_content: bytes = b""
        while True:
            event: Dict[str, Any] = await self.receive()
            if event["type"] == HttpRequestEnums.HTTP_REQUEST:
                body_content += event.get("body", b"")
                if not event.get("more_body", False):
                    break
        self.body = self._decode_body(body_content)

    def _parse_headers(self, raw_headers: List[Tuple[bytes, bytes]]) -> Dict[str, str]:
        """
        Parse headers from raw scope headers.
        :param raw_headers: List of (key, value) byte tuples
        :return: Dictionary of headers
        """
        return {
            key.decode("utf-8"): value.decode("utf-8") for key, value in raw_headers
        }

    def _parse_query_params(
        self, query_string: bytes
    ) -> Dict[str, Union[str, List[str]]]:
        """
        Parse query parameters from a query string.
        :param query_string: Query string as bytes
        :return: Dictionary of query parameters
        """
        return {
            k: v[0] if len(v) == 1 else v
            for k, v in parse_qs(query_string.decode("utf-8")).items()
        }

    def _parse_cookies(self, cookie_header: str) -> Dict[str, str]:
        """
        Parse cookies from the Cookie header.
        :param cookie_header: Cookie header as a string
        :return: Dictionary of cookies
        """
        cookies: Dict[str, str] = {}
        if cookie_header:
            for cookie in cookie_header.split(";"):
                if "=" in cookie:
                    key, value = cookie.strip().split("=", 1)
                    cookies[key] = value
        return cookies

    def _decode_body(
        self, body_content: bytes
    ) -> Union[str, Dict[str, Any], List[Any]]:
        """
        Decode the body content based on content type.
        :param body_content: Raw body bytes
        :return: Decoded body (JSON, text, or raw bytes)
        """
        content_type: str = self.headers.get(HttpRequestEnums.CONTENT_TYPE, "").lower()
        if HttpRequestEnums.APPLICATION_JSON in content_type:
            try:
                return json.loads(body_content.decode("utf-8")) if body_content else {}
            except json.JSONDecodeError:
                return body_content.decode("utf-8")
        elif HttpRequestEnums.APPLICATION_FORM in content_type:
            return parse_qs(body_content.decode("utf-8"))
        else:
            return body_content.decode("utf-8") if body_content else ""

    def get_request_info(self) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
        """
        Returns a tuple containing method, path, and request_kwargs.
        :return: Tuple (method, path, request_kwargs)
        """
        request_kwargs: Dict[str, Any] = {
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
            "params": self.params or {},
        }
        return self.method, self.path, request_kwargs

    def get_header(self, key, default=None):
        """
        Get a specific header value.
        :param key: Header key
        :param default: Default value if the header is not found
        :return: Header value or default
        """
        return self.headers.get(key.lower(), default)

    def get_headers(self):
        """
        Get headers.
        :return: Headers dictionary
        """
        return self.headers

    def set_header(self, key, value):
        """
        Set or update a specific header value.
        :param key: Header key
        :param value: Header value
        """
        self.headers[key.lower()] = value

    def get_cookie(self, key, default=None):
        """
        Get a specific cookie value.
        :param key: Cookie key
        :param default: Default value if the cookie is not found
        :return: Cookie value or default
        """
        return self.cookies.get(key, default)

    def set_cookie(self, key, value):
        """
        Set or update a specific cookie value.
        :param key: Cookie key
        :param value: Cookie value
        """
        self.cookies[key] = value

    def get_query_params(self, key=None, default=None):
        """
        Get a specific query parameter value.
        :param key: Query parameter key
        :param default: Default value if the query parameter is not found
        :return: Query parameter value or default
        """
        if not key:
            return self.query_params
        return self.query_params.get(key, default)

    def set_query_param(self, key, value):
        """
        Set or update a specific query parameter value.
        :param key: Query parameter key
        :param value: Query parameter value
        """
        self.query_params[key] = value

    def get_body(self):
        """
        Get the request body.
        :return: Body content
        """
        return self.body

    def set_body(self, body):
        """
        Set or update the request body.
        :param body: New body content
        """
        self.body = body

    def get_client_info(self):
        """
        Get client information (IP and port).
        :return: Tuple of client IP and port
        """
        return self.client_ip, self.client_port

    def get_server_info(self):
        """
        Get server information (host and port).
        :return: Tuple of server host and port
        """
        return self.server_host, self.server_port

    def set_params(self, key_or_dict, value=None):
        """
        Set or update the params attribute.

        :param key_or_dict: A dictionary to update the params or a key for a specific parameter.
        :param value: The value to set if a key is provided.
        """
        if not self.params:
            self.params = {}

        if isinstance(key_or_dict, dict):
            # Merge the dictionary into existing params
            self.params.update(key_or_dict)
        elif isinstance(key_or_dict, str) and value is not None:
            # Set or update a specific key-value pair
            self.params[key_or_dict] = value
        else:
            raise ValueError("Provide either a dictionary or a key-value pair.")

    def get_params(self, key: str = None, default: str = None):
        """
        Get the value of a specific parameter or all parameters.

        :param key: The key of the parameter to retrieve (optional).
        :param default: The default value to return if the key is not found.
        :return: The value of the parameter or all parameters if no key is provided.
        """
        if key is None:
            # Return all params
            return self.params or {}
        return self.params.get(key, default)

    def get_client_ip(self):
        """
        Get the client IP address.
        :return: The client IP address
        """
        return self.client_ip

    def get_client_port(self):
        """
        Get the client port.
        :return: The client port
        """
        return self.client_port

    def get_server_host(self):
        """
        Get the server host.
        :return: The server host
        """
        return self.server_host

    def get_if_none_match(self) -> Optional[str]:
        """
        Get the value of the If-None-Match header from the request.
        :return: The value of the If-None-Match header, or None if not present.
        """
        return self.get_header(HttpHeaders.IF_NONE_MATCH)

    def get_if_match(self) -> Optional[str]:
        """
        Retrieve the value of the 'If-Match' header from the HTTP request headers.

        :retuen: Optional[str]: The value of the 'If-Match' header if it exists, otherwise None.
        """
        return self.get_header(HttpHeaders.IF_MATCH)
