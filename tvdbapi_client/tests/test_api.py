import datetime
import os

import testtools
from testtools import matchers

import tvdbapi_client
from tvdbapi_client import api
from tvdbapi_client import exceptions
from tvdbapi_client.tests import base
from tvdbapi_client import timeutil

MINS_15 = datetime.timedelta(minutes=15)


def disabled():
    return not os.environ.get('TEST_API_KEY') or not os.environ.get(
        'TEST_API_USER') or not os.environ.get('TEST_API_PASSWORD')


class ApiTest(base.BaseTest):

    def setUp(self):
        super(ApiTest, self).setUp()
        self.client = api.TVDBClient(
            apikey=os.environ.get('TEST_API_KEY'),
            username=os.environ.get('TEST_API_USER'),
            userpass=os.environ.get('TEST_API_PASSWORD'))

    def test_set_language(self):
        self.assertEqual(self.client.language, 'en')
        self.client.language = 'es'
        self.assertEqual(self.client.language, 'es')

    def test_token_expired(self):
        self.assertTrue(self.client.token_expired)

        # current time
        self.client._token_timer = timeutil.utcnow()
        self.assertFalse(self.client.token_expired)

        # 15 minutes after current
        self.client._token_timer += MINS_15
        self.assertFalse(self.client.token_expired)

        # 30 minutes after current
        self.client._token_timer += MINS_15
        self.assertFalse(self.client.token_expired)

        # 45 minutes after current
        self.client._token_timer += MINS_15
        self.assertFalse(self.client.token_expired)

        # 60 minutes after current
        self.client._token_timer += MINS_15
        self.assertTrue(self.client.token_expired)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_authenicate_login(self):
        self.client.authenticate()
        self.assertIsNotNone(self.client._token_timer)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_authenicate_refresh(self):
        self.client.authenticate()
        first_ts = self.client._token_timer

        self.client.authenticate()
        second_ts = self.client._token_timer
        self.assertThat(second_ts, matchers.GreaterThan(first_ts))

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_search_series(self):
        series = self.client.search_series(name='The Big Bang Theory')
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]['id'], 80379)

        series = self.client.search_series(imdbId='tt0898266')
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]['id'], 80379)

        series = self.client.search_series(zap2itId='EP00931182')
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]['id'], 80379)

        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.search_series,
                          name='Fake Unknown Test')

        self.CONF.set_override('select_first', True, 'tvdb')
        series = self.client.search_series(name='The Big Bang Theory')
        self.assertEqual(series['id'], 80379)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_series(self):
        series = self.client.get_series(80379)
        self.assertEqual(series['seriesName'], 'The Big Bang Theory')

        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_series,
                          0)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episodes(self):
        episodes = self.client.get_episodes(94981)
        self.assertEqual(len(episodes), 17)

        episodes = self.client.get_episodes(80379,
                                            airedSeason=3,
                                            airedEpisode=7)
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0].get('episodeName'),
                         'The Guitarist Amplification')

        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episodes,
                          0)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episodes_summary(self):
        ep_summary = self.client.get_episodes_summary(94981)
        self.assertEqual(ep_summary['airedEpisodes'], '17')

        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episodes_summary,
                          0)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_series_image_info(self):
        image_info = self.client.get_series_image_info(94981)
        self.assertEqual(image_info['series'], 2)

        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_series_image_info,
                          0)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episode(self):
        episode = self.client.get_episode(1137661)
        self.assertEqual(episode['episodeName'], 'Diamond Jane')

        self.assertRaises(exceptions.TVDBRequestException,
                          self.client.get_episode,
                          0)


class SimpleApiTest(base.BaseTest):

    def test_get_client(self):
        client = tvdbapi_client.get_client()
        self.assertIsInstance(client, api.TVDBClient)

        # validate client not configured
        self.assertRaises(exceptions.TVDBRequestException,
                          client.authenticate)

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_configured_client(self):
        client = tvdbapi_client.get_client(
            apikey=os.environ.get('TEST_API_KEY'),
            username=os.environ.get('TEST_API_USER'),
            userpass=os.environ.get('TEST_API_PASSWORD'),
            service_url='https://api-dev.thetvdb.com',
            verify_ssl_certs=True,
            select_first=False)
        self.assertIsInstance(client, api.TVDBClient)

        # validate auth is successful
        client.authenticate()
        self.assertIsNotNone(client._token_timer)
