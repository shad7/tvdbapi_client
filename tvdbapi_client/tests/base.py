import json
import logging

from oslo_config import fixture as fixture_config
from oslotest import base as test_base
from requests_mock.contrib import fixture as requests_mock_fixture
from six.moves.urllib import parse

# see urllib3 regarding InsecureRequestWarning and InsecurePlatformWarning
logging.captureWarnings(True)


class BaseTest(test_base.BaseTestCase):

    def setUp(self):
        super(BaseTest, self).setUp()

        self.CONF = self.useFixture(fixture_config.Config()).conf
        self.CONF([])


class BaseHTTPTest(BaseTest):

    def setUp(self):
        super(BaseHTTPTest, self).setUp()
        self.requests_mock = self.useFixture(requests_mock_fixture.Fixture())
        self.base_url = ''

    def stub_url(self, method=None, parts=None, params=None,
                 data=None, **kwargs):

        if method is None:
            method = 'get'

        if data and 'exc' not in kwargs:
            kwargs['text'] = json.dumps(data)
            headers = kwargs.setdefault('headers', {})
            headers['Content-Type'] = 'application/json'

        if not parts:
            parts = []

        url = '/'.join([str(p).strip('/') for p in [self.base_url] + parts])

        if params:
            url += '?%s' % parse.urlencode(params, doseq=True)

        self.requests_mock.register_uri(method, url, **kwargs)
