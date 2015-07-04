from __future__ import print_function

import copy

BASE_WRAPPER = {
    'data': None
    }

SEARCH_SERIES = {
    'id': None,
    'airedSeason': None,
    'airedEpisodeNumber': None,
    'episodeName': None,
    'firstAired': None,
    'guestStars': None,
    'director': None,
    'writers': [None],
    'overview': None,
    'productionCode': None,
    'showUrl': None,
    'lastUpdated': None,
    'dvdDiscid': None,
    'dvdSeason': None,
    'dvdEpisodeNumber': None,
    'dvdChapter': None,
    'absoluteNumber': None,
    'filename': None,
    'seriesId': None,
    'lastUpdatedBy': None,
    'airsAfterSeason': None,
    'airsBeforeSeason': None,
    'airsBeforeEpisode': None,
    'thumbAuthor': None,
    'thumbAdded': None,
    'thumbWidth': None,
    'thumbHeight': None,
    'imdbId': None
    }

SERIES = {
    'id': 0,
    'seriesName': None,
    'aliases': [None],
    'poster': None,
    'seriesId': 0,
    'status': None,
    'firstAired': None,
    'network': None,
    'networkId': None,
    'runtime': None,
    'genre': [None],
    'actors': [None],
    'overview': None,
    'lastUpdated': 0,
    'airsDayOfWeek': None,
    'airsTime': None,
    'rating': None,
    'imdbId': None,
    'zap2itId': None,
    'added': None
    }

EPISODES = {
    'absoluteNumber': 0,
    'airedEpisodeNumber': 0,
    'airedSeason': 0,
    'dvdEpisodeNumber': 0,
    'dvdSeason': 0,
    'episodeName': None,
    'id': 0,
    'overview': None
    }

EPISODES_SUMMARY = {
    'airedSeasons': [None],
    'airedEpisodes': None,
    'dvdSeasons': [None],
    'dvdEpisodes': None
    }

IMAGE_INFO = {
    'fanart': 0,
    'poster': 0,
    'season': 0,
    'seasonwide': 0,
    'series': 0
    }

EPISODE = {
    'id': None,
    'airedSeason': None,
    'airedEpisodeNumber': None,
    'episodeName': None,
    'firstAired': None,
    'guestStars': None,
    'director': None,
    'writers': [None],
    'overview': None,
    'productionCode': None,
    'showUrl': None,
    'lastUpdated': None,
    'dvdDiscid': None,
    'dvdSeason': None,
    'dvdEpisodeNumber': None,
    'dvdChapter': None,
    'absoluteNumber': None,
    'filename': None,
    'seriesId': None,
    'lastUpdatedBy': None,
    'airsAfterSeason': None,
    'airsBeforeSeason': None,
    'airsBeforeEpisode': None,
    'thumbAuthor': None,
    'thumbAdded': None,
    'thumbWidth': None,
    'thumbHeight': None,
    'imdbId': None
    }


def make_response(schema, data, as_list=False, total=1):
    resp = copy.deepcopy(schema)
    resp.update(**data)
    base = dict(BASE_WRAPPER)

    if as_list:
        base['data'] = []
        for x in range(0, total):
            base['data'].append(resp)
    else:
        base['data'] = resp
    return base
