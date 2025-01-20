from enum import Enum

class CompressionAlgorithm(Enum):
    GZIP = "gzip"
    BZIP2 = "bzip2"
    LZMA = "lzma"
    ZIP = "zip"
    TAR = "tar"
    RAR = "rar"
