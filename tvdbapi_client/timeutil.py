"""Time related utilities and helper functions."""

import datetime

# almost an hour so token does not expire without
# ability to simply refresh token.
ONE_HOUR = datetime.timedelta(minutes=55)


def utcnow():
    """Gets current time.

    :returns: current time from utc
    :rtype: :py:obj:`datetime.datetime`
    """
    return datetime.datetime.utcnow()


def is_older_than(before, delta):
    """Checks if a datetime is older than delta

    :param datetime before: a datetime to check
    :param timedelta delta: period of time to compare against
    :returns: ``True`` if before is older than time period else ``False``
    :rtype: bool
    """
    return utcnow() - before > delta


def is_newer_than(after, delta):
    """Checks if a datetime is newer than delta

    :param datetime after: a datetime to check
    :param timedelta delta: period of time to compare against
    :returns: ``True`` if before is newer than time period else ``False``
    :rtype: bool
    """
    return after - utcnow() > delta
