from enum import StrEnum

class ContentType(StrEnum):
    # Text
    PLAIN = "text/plain"
    HTML = "text/html"
    CSS = "text/css"
    JAVASCRIPT = "text/javascript"
    CSV = "text/csv"

    # JSON & XML
    JSON = "application/json"
    XML = "application/xml"
    TEXT_XML = "text/xml"

    # Images
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    WEBP = "image/webp"
    SVG = "image/svg+xml"

    # Application
    FORM_URLENCODED = "application/x-www-form-urlencoded"
    MULTIPART_FORM_DATA = "multipart/form-data"
    OCTET_STREAM = "application/octet-stream"
    PDF = "application/pdf"
    ZIP = "application/zip"

    # Audio & Video
    MP3 = "audio/mpeg"
    MP4 = "video/mp4"
    WEBM = "video/webm"

    # Others
    YAML = "application/x-yaml"
    MARKDOWN = "text/markdown"

    # Custom or unknown types
    CUSTOM = "application/octet-stream"
