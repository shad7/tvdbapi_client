from requests import exceptions
import six


def error_map(f):
    """Wraps exceptions raised by requests.

    .. py:decorator:: error_map
    """
    @six.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except exceptions.RequestException as err:
            raise TVDBRequestException(
                (getattr(err, 'errno', None),
                 getattr(err, 'strerror', None)),
                response=getattr(err, 'response', None),
                request=getattr(err, 'request', None))
    return wrapper


class TVDBRequestException(exceptions.RequestException):
    pass
