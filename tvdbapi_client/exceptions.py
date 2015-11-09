"""Exceptions for API and decorator to wrap request exceptions."""
from requests import exceptions
import six


def error_map(func):
    """Wrap exceptions raised by requests.

    .. py:decorator:: error_map
    """
    @six.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.RequestException as err:
            raise TVDBRequestException(
                (getattr(err, 'errno', None),
                 getattr(err, 'strerror', None)),
                response=getattr(err, 'response', None),
                request=getattr(err, 'request', None))
    return wrapper


class TVDBRequestException(exceptions.RequestException):
    """Provide a base exception for local use."""
    pass
