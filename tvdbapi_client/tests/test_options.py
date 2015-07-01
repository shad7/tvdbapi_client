from tvdbapi_client import options
from tvdbapi_client.tests import base


class OptionsTest(base.BaseTest):

    def test_list_opts(self):
        self.assertIsNotNone(options.list_opts())
