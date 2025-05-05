def strip_etag_quotes(etag: str) -> str:
    """
    Removes surrounding quotes and weak validator prefix ('W/') from an ETag string.

    :param etag: The ETag string to be processed.
    :return: The cleaned ETag string without quotes or weak validator prefix.
    """
    return etag.strip().strip('"').lstrip("W/").strip('"')
