import json

from storm.common.exceptions.exception import StormHttpException


class HttpResponse:
    """
    A class to construct and send HTTP responses in an ASGI application.
    """

    def __init__(self, content=None, status_code=200, headers=None, content_type="text/plain"):
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
        self.headers["content-type"] = self.content_type

    @staticmethod
    def from_request(request, content=None, status_code=200, headers=None):
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

        # Example: Add a header based on request headers
        if "accept-language" in request.headers:
            headers["content-language"] = request.headers["accept-language"]

        
        # Example: Echo query parameters back in the response for debugging
        if request.query_params:
            headers["x-query-params"] = json.dumps(request.query_params)

        # Create the response
        return HttpResponse(
            content=content,
            status_code=status_code,
            headers=headers,
            content_type="application/json"
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
            content_type="application/json"
        )

    def update_content(self, content):
        """
        Update the response content.
        :param content: New response content
        """
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

    def update_content_type(self, content_type):
        """
        Update the Content-Type header.
        :param content_type: New Content-Type value
        """
        self.content_type = content_type
        self.headers["content-type"] = self.content_type

    async def send(self, send):
        """
        Send the HTTP response using the ASGI `send` channel.

        :param send: The ASGI send callable
        """
        body = self._encode_content()
        # Send the response start event
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [[key.encode("utf-8"), value.encode("utf-8")] for key, value in self.headers.items()],
        })
        # Send the response body
        await send({
            "type": "http.response.body",
            "body": body,
        })

    def _encode_content(self):
        """
        Encode the response content based on its type.

        :return: Encoded content as bytes
        """
        if isinstance(self.content, (dict, list)):  # JSON content
            return json.dumps(self.content).encode("utf-8")
        elif isinstance(self.content, str):  # Plain text or HTML
            return self.content.encode("utf-8")
        elif isinstance(self.content, bytes):  # Binary content
            return self.content
        else:
            return b""  # Empty response

# Helper methods to create common response types
def JsonResponse(data, status_code=200, headers=None):
    """
    Create a JSON response.
    """
    return HttpResponse(
        content=data,
        status_code=status_code,
        headers=headers,
        content_type="application/json"
    )


def TextResponse(text, status_code=200, headers=None):
    """
    Create a plain text response.
    """
    return HttpResponse(
        content=text,
        status_code=status_code,
        headers=headers,
        content_type="text/plain"
    )


def HtmlResponse(html, status_code=200, headers=None):
    """
    Create an HTML response.
    """
    return HttpResponse(
        content=html,
        status_code=status_code,
        headers=headers,
        content_type="text/html"
    )


def FileResponse(file_bytes, filename, content_type="application/octet-stream", status_code=200, headers=None):
    """
    Create a file download response.
    """
    headers = headers or {}
    headers["content-disposition"] = f'attachment; filename="{filename}"'
    return HttpResponse(
        content=file_bytes,
        status_code=status_code,
        headers=headers,
        content_type=content_type
    )
