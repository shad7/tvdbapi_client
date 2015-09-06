import os
import shutil

from testtools import matchers

import tvdbapi_client
from tvdbapi_client import api
from tvdbapi_client import exceptions
from tvdbapi_client.tests import base
from tvdbapi_client.tests import schema_helper


class MockedApiTest(base.BaseHTTPTest):

    cfg_data = []
    cfg_data.append('[tvdb]\n')
    cfg_data.append('apikey=abc123xyz456\n')
    cfg_data.append('username=test_user\n')
    cfg_data.append('userpass=sample\n')
    cfg_data.append('service_url=https://api-dev.thetvdb.com\n')
    cfg_data.append('verify_ssl_certs=true\n')
    cfg_data.append('select_first=false\n')

    def setUp(self):
        super(MockedApiTest, self).setUp()
        self.base_url = self.CONF.tvdb.service_url

        self.stub_url(method='post',
                      parts=['login'],
                      data={'token': 'abc123'})
        self.client = api.TVDBClient()

    def test_get_configured_client(self):
        client = tvdbapi_client.get_client(
            apikey='abc123xyz456',
            username='test_user',
            userpass='sample',
            service_url='https://api-dev.thetvdb.com',
            verify_ssl_certs=True,
            select_first=False)
        self.assertIsInstance(client, api.TVDBClient)

        # validate auth is successful
        client.authenticate()
        self.assertIsNotNone(client._token_timer)

        cfgfile = self.create_tempfiles(
            [('tvdbapi_client', ''.join(self.cfg_data))])[0]
        self.addCleanup(shutil.rmtree, os.path.dirname(cfgfile), True)

        client = tvdbapi_client.get_client(config_file=cfgfile)
        self.assertIsInstance(client, api.TVDBClient)

    def test_authenicate_refresh(self):
        self.stub_url(parts=['refresh_token'],
                      data={'token': 'abc456'})
        self.client.authenticate()
        first_ts = self.client._token_timer

        self.stub_url(parts=['refresh_token'],
                      status_code=401)
        self.client.authenticate()
        second_ts = self.client._token_timer
        self.assertThat(second_ts, matchers.GreaterThan(first_ts))

        self.stub_url(parts=['refresh_token'],
                      status_code=400)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.authenticate)

    def test_search_series(self):
        resp_data = schema_helper.make_response(
            schema_helper.SEARCH_SERIES,
            {'id': 80379,
             'name': 'The Big Bang Theory',
             'imdbId': 'tt0898266',
             'zap2itId': 'EP00931182'},
            as_list=True)

        self.stub_url(parts=['search', 'series'],
                      params={'name': 'The Big Bang Theory'},
                      data=resp_data)
        series = self.client.search_series(name='The Big Bang Theory')
        self.assertEqual(len(series), 1, series)
        self.assertEqual(series[0]['id'], 80379)

        self.stub_url(parts=['search', 'series'],
                      params={'imdbId': 'tt0898266'},
                      data=resp_data)
        series = self.client.search_series(imdbId='tt0898266')
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]['id'], 80379)

        self.stub_url(parts=['search', 'series'],
                      params={'zap2itId': 'EP00931182'},
                      data=resp_data)
        series = self.client.search_series(zap2itId='EP00931182')
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]['id'], 80379)

        self.stub_url(parts=['search', 'series'],
                      params={'name': 'Fake Unknown Test'},
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.search_series,
                          name='Fake Unknown Test')

        self.stub_url(parts=['search', 'series'],
                      params={'name': 'Fake Unknown Test'},
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.search_series,
                          name='Fake Unknown Test',
                          unknown='xyz')

        self.stub_url(parts=['search', 'series'],
                      params={'name': 'The Big Bang Theory'},
                      data=resp_data)
        self.CONF.set_override('select_first', True, 'tvdb')
        series = self.client.search_series(name='The Big Bang Theory')
        self.assertEqual(series['id'], 80379)

    def test_get_series(self):
        resp_data = schema_helper.make_response(
            schema_helper.SERIES,
            {'id': 80379,
             'seriesName': 'The Big Bang Theory',
             'imdbId': 'tt0898266',
             'zap2itId': 'EP00931182'})

        self.stub_url(parts=['series', 80379],
                      data=resp_data)
        series = self.client.get_series(80379)
        self.assertEqual(series['seriesName'], 'The Big Bang Theory')

        self.stub_url(parts=['series', 0],
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_series,
                          0)

        self.stub_url(parts=['series', 0],
                      exc=exceptions.TVDBRequestException)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_series,
                          0)

    def test_get_episodes(self):
        resp_data = schema_helper.make_response(
            schema_helper.EPISODES,
            {'id': 1},
            as_list=True,
            total=17)

        self.stub_url(parts=['series', 94981, 'episodes', 'query'],
                      data=resp_data)
        episodes = self.client.get_episodes(94981)
        self.assertEqual(len(episodes), 17)

        self.stub_url(parts=['series', 94981, 'episodes', 'query'],
                      params={'page': 1},
                      data=resp_data)
        episodes = self.client.get_episodes(94981, page=1)
        self.assertEqual(len(episodes), 17)

        self.stub_url(parts=['series', 0, 'episodes', 'query'],
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episodes,
                          0)

        self.stub_url(parts=['series', 0, 'episodes', 'query'],
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episodes,
                          0, other='abc')

    def test_get_episodes_summary(self):
        resp_data = schema_helper.make_response(
            schema_helper.EPISODES_SUMMARY,
            {'airedEpisodes': '17'})

        self.stub_url(parts=['series', 94981, 'episodes', 'summary'],
                      data=resp_data)
        ep_summary = self.client.get_episodes_summary(94981)
        self.assertEqual(ep_summary['airedEpisodes'], '17')

        self.stub_url(parts=['series', 0, 'episodes', 'summary'],
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episodes_summary,
                          0)

    def test_get_series_image_info(self):
        resp_data = schema_helper.make_response(
            schema_helper.IMAGE_INFO,
            {'series': 2})

        self.stub_url(parts=['series', 94981, 'images'],
                      data=resp_data)
        image_info = self.client.get_series_image_info(94981)
        self.assertEqual(image_info['series'], 2)

        self.stub_url(parts=['series', 0, 'images'],
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_series_image_info,
                          0)

    def test_get_episode(self):
        resp_data = schema_helper.make_response(
            schema_helper.EPISODE,
            {'episodeName': 'Diamond Jane'})

        self.stub_url(parts=['episodes', 1137661],
                      data=resp_data)
        episode = self.client.get_episode(1137661)
        self.assertEqual(episode['episodeName'], 'Diamond Jane')

        self.stub_url(parts=['episodes', 0],
                      status_code=404)
        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episode,
                          0)
