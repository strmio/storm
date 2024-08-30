from enum import Enum

class MimeType(Enum):
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    TEXT_HTML = "text/html"
    TEXT_PLAIN = "text/plain"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    VIDEO_MP4 = "video/mp4"
    AUDIO_MPEG = "audio/mpeg"
    MULTIPART_FORM_DATA = "multipart/form-data"
