import base64
from email.utils import formatdate
import json
import hashlib
from storm.common.enums.content_type import ContentType
from storm.common.enums.http_headers import HttpHeaders
from storm.common.enums.http_status import HttpStatus
from storm.common.exceptions.exception import StormHttpException
from storm.core.adapters.http_request import HttpRequest


class HttpResponse:
    """
    A class to construct and send HTTP responses in an ASGI application.
    """

    def __init__(
        self,
        content=None,
        status_code=HttpStatus.OK,
        headers=None,
        content_type=ContentType.JSON,
    ):
        """
        Initialize the HttpResponse object.

        :param content: Response content (string, JSON, bytes, etc.)
        :param status_code: HTTP status code (default: 200)
        :param headers: Additional headers as a dictionary
        :param content_type: Content-Type of the response
        """
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.content_type = content_type

        # Ensure Content-Type is included in headers
        self.headers[HttpHeaders.CONTENT_TYPE] = self.content_type

    @staticmethod
    def from_request(request, content=None, status_code=HttpStatus.OK, headers=None):
        """
        Create a response based on the request object.

        :param request: HttpRequest object
        :param content: Response content
        :param status_code: HTTP status code
        :param headers: Additional headers as a dictionary
        :return: HttpResponse object
        """
        # Default headers
        headers = headers or {}

        # Add X-powered-by header
        headers[HttpHeaders.X_POWERED_BY] = "Storm"

        # Add Date header
        headers["Date"] = formatdate(timeval=None, usegmt=True)

        # Add a header based on request headers
        if HttpHeaders.ACCEPT_LANGUAGE in request.headers:
            headers[HttpHeaders.ACCEPT_LANGUAGE] = request.headers[
                HttpHeaders.ACCEPT_LANGUAGE
            ]

        # Create the response
        return HttpResponse(
            content=content,
            status_code=status_code,
            headers=headers,
            content_type=ContentType.JSON,
        )

    @staticmethod
    def from_error(error: StormHttpException, headers=None):
        """
        Create a structured error response.

        :param message: A short error message (e.g., "Bad Request").
        :param status_code: HTTP status code (default: 400).
        :param details: Optional additional details about the error (e.g., validation errors).
        :param headers: Additional headers as a dictionary.
        :return: HttpResponse object.
        """

        return HttpResponse(
            content=error.to_dict(),
            status_code=error.status_code,
            headers=headers,
            content_type=ContentType.JSON,
        )

    def update_content(self, content):
        """
        Update the response content.
        :param content: New response content
        """
        # Update Content-Length header
        if isinstance(content, (str, bytes)):
            self.headers[HttpHeaders.CONTENT_LENGTH] = str(len(content))
        elif isinstance(content, (dict, list)):
            self.headers[HttpHeaders.CONTENT_LENGTH] = str(len(json.dumps(content)))
        else:
            self.headers.pop(HttpHeaders.CONTENT_LENGTH, None)

        self.content = content

    def update_status_code(self, status_code):
        """
        Update the HTTP status code.
        :param status_code: New HTTP status code
        """
        self.status_code = status_code

    def update_headers(self, headers):
        """
        Update headers by merging with existing headers.
        :param headers: Dictionary of new headers to merge
        """
        self.headers.update(headers)

    def set_header(self, header_name: str, value: str):
        """
        Set a specific header.
        :param header_name: Header key
        :param value: Header value
        """
        self.headers[header_name] = value

    def update_content_type(self, content_type):
        """
        Update the Content-Type header.
        :param content_type: New Content-Type value
        """
        self.content_type = content_type
        self.headers[HttpHeaders.contentType] = self.content_type

    def get_headers(self):
        """
        Get the response headers.
        :return: Dictionary of headers
        """
        return self.headers

    async def send(self, send):
        """
        Send the HTTP response using the ASGI `send` channel.

        :param send: The ASGI send callable
        """
        body = self._encode_content()
        # Send the response start event
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [
                    [key.encode("utf-8"), value.encode("utf-8")]
                    for key, value in self.headers.items()
                ],
            }
        )
        # Send the response body
        await send(
            {
                "type": "http.response.body",
                "body": body,
            }
        )

    def _encode_content(self):
        """
        Encode the response content based on its type.

        :return: Encoded content as bytes
        """
        if isinstance(self.content, (dict, list)):  # JSON content
            return json.dumps(self.content).encode("utf-8")
        if isinstance(self.content, str):  # Plain text or HTML
            return self.content.encode("utf-8")
        if isinstance(self.content, bytes):  # Binary content
            return self.content

        return b""  # Empty response

    async def send_sse_headers(self, send):
        """
        Send SSE-specific headers.
        """
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"content-type", b"text/event-stream"),
                    (b"cache-control", b"no-cache"),
                    (b"connection", b"keep-alive"),
                ],
            }
        )

    async def send_sse_event(self, send, data: str, event: str = None, id: str = None):
        """
        Send a single SSE event.
        """
        message = ""
        if id:
            message += f"id: {id}\n"
        if event:
            message += f"event: {event}\n"
        message += f"data: {data}\n\n"
        await send(
            {
                "type": "http.response.body",
                "body": message.encode("utf-8"),
                "more_body": True,
            }
        )

    async def close_sse(self, send):
        """
        Close the SSE stream.
        """
        await send(
            {
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            }
        )

    def _generate_etag(self, algorithm: str = "md5", encoding: str = "base64") -> str:
        """
        Generate an ETag from the response content.

        :param algorithm: Hash algorithm ("md5", "sha256", etc.)
        :param encoding: Encoding of the digest ("hex", "base64")
        :return: Encoded ETag value (not wrapped in W/"" yet)
        """
        if isinstance(self.content, (dict, list)):
            raw = json.dumps(self.content, sort_keys=True).encode("utf-8")
        elif isinstance(self.content, str):
            raw = self.content.encode("utf-8")
        elif isinstance(self.content, bytes):
            raw = self.content
        else:
            raw = b""

        hasher = getattr(hashlib, algorithm)(raw)

        if encoding == "hex":
            return hasher.hexdigest()
        elif encoding == "base64":
            return base64.b64encode(hasher.digest()).decode("ascii")
        raise ValueError("Unsupported encoding for ETag")

    def set_etag(
        self,
        weak: bool = True,
        algorithm: str = "md5",
        encoding: str = "base64",
        prefix: str = "c-",
    ) -> str:
        """
        Set the ETag header based on current content.

        :param weak: Whether the ETag is weak (default True)
        :param algorithm: Hashing algorithm for ETag
        :param encoding: Digest encoding ("hex", "base64")
        :param prefix: Prefix to add before the digest (e.g. "c-")
        :return: The computed ETag
        """
        digest = self._generate_etag(algorithm=algorithm, encoding=encoding)
        tag = f"{prefix}{digest}"
        etag_value = f'W/"{tag}"' if weak else f'"{tag}"'
        self.set_header(HttpHeaders.ETAG, etag_value)
        return tag


# Helper methods to create common response types


def JsonResponse(data, status_code=HttpStatus.OK, headers=None):
    """
    Create a JSON response.
    """
    return HttpResponse(
        content=data,
        status_code=status_code,
        headers=headers,
        content_type=ContentType.JSON,
    )


def TextResponse(text, status_code=HttpStatus.OK, headers=None):
    """
    Create a plain text response.
    """
    return HttpResponse(
        content=text,
        status_code=status_code,
        headers=headers,
        content_type=ContentType.PLAIN,
    )


def HtmlResponse(html, status_code=HttpStatus.OK, headers=None):
    """
    Create an HTML response.
    """
    return HttpResponse(
        content=html,
        status_code=status_code,
        headers=headers,
        content_type=ContentType.TEXT_HTML,
    )


def FileResponse(
    file_bytes,
    filename,
    content_type=ContentType.OCTET_STREAM,
    status_code=200,
    headers=None,
):
    """
    Create a file download response.
    """
    headers = headers or {}

    headers["content-disposition"] = f'attachment; filename="{filename}"'
    return HttpResponse(
        content=file_bytes,
        status_code=status_code,
        headers=headers,
        content_type=content_type,
    )


async def etag_response(request: HttpRequest, response: HttpResponse):
    current_etag = response.set_etag()
    client_etag = request.get_if_none_match()

    if client_etag and client_etag.strip('"') == current_etag:
        # Resource hasn't changed, return 304
        response.update_status_code(HttpStatus.NOT_MODIFIED)
        response.update_content("")  # No body for 304
        response.update_headers({HttpHeaders.CONTENT_TYPE: ContentType.PLAIN})

    await response.send(request.send)
