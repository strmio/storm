from enum import StrEnum


class CompressionAlgorithm(StrEnum):
    GZIP = "gzip"
    BZIP2 = "bzip2"
    LZMA = "lzma"
    ZIP = "zip"
    TAR = "tar"
    RAR = "rar"
