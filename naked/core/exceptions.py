class ProviderError(Exception):
    """
    Error de provider que SÍ queremos reportar como resultado
    (status=ERROR), en vez de dejar que reviente el engine.
    """


class RateLimitError(ProviderError):
    """El provider nos está limitando (429, o 403 por rate limit)."""


class ProviderUnavailableError(ProviderError):
    """Timeout, error de red, o 5xx del lado del provider."""
