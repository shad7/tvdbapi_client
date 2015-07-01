from __future__ import print_function

import datetime

from tvdbapi_client.tests import base
from tvdbapi_client import timeutil

MINS_15 = datetime.timedelta(minutes=15)
MINS_30 = datetime.timedelta(minutes=30)
MINS_45 = datetime.timedelta(minutes=45)
ONE_HOUR = datetime.timedelta(minutes=60)


class TimeutilTest(base.BaseTest):

    def test_is_older_than(self):
        now = timeutil.utcnow()
        before = now - MINS_15
        self.assertFalse(timeutil.is_older_than(before, timeutil.ONE_HOUR))
        before = now - MINS_30
        self.assertFalse(timeutil.is_older_than(before, timeutil.ONE_HOUR))
        before = now - MINS_45
        self.assertFalse(timeutil.is_older_than(before, timeutil.ONE_HOUR))
        before = now - ONE_HOUR
        self.assertTrue(timeutil.is_older_than(before, timeutil.ONE_HOUR))

    def test_is_newer_than(self):
        now = timeutil.utcnow()
        after = now + MINS_15
        self.assertFalse(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
        after = now + MINS_30
        self.assertFalse(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
        after = now + MINS_45
        self.assertFalse(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
        after = now + ONE_HOUR
        self.assertTrue(timeutil.is_newer_than(after, timeutil.ONE_HOUR))
