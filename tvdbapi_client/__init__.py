__all__ = ['__version__', 'get_client']

import logging

import pbr.version

logging.getLogger(__package__).addHandler(logging.NullHandler())

version_info = pbr.version.VersionInfo(__package__)
__version__ = version_info.version_string()


def get_client(config_file=None, apikey=None, username=None, userpass=None,
               service_url=None, verify_ssl_certs=None, select_first=None):
    """Configures the API service and creates a new instance of client.

    :param str config_file: absolute path to configuration file
    :param str apikey: apikey from thetvdb
    :param str username: username used on thetvdb
    :param str userpass: password used on thetvdb
    :param str service_url: the url for thetvdb api service
    :param str verify_ssl_certs: flag for validating ssl certs for
                                 service url (https)
    :param str select_first: flag for selecting first series from
                             search results
    :returns: tvdbapi client
    :rtype: tvdbapi_client.api.TVDBClient
    """

    from oslo_config import cfg

    from tvdbapi_client import api

    if config_file is not None:
        cfg.CONF([], default_config_files=[config_file])
    else:
        if apikey is not None:
            cfg.CONF.set_override('apikey', apikey)
        if username is not None:
            cfg.CONF.set_override('username', username)
        if userpass is not None:
            cfg.CONF.set_override('userpass', userpass)
        if service_url is not None:
            cfg.CONF.set_override('service_url', service_url)
        if verify_ssl_certs is not None:
            cfg.CONF.set_override('verify_ssl_certs', verify_ssl_certs)
        if select_first is not None:
            cfg.CONF.set_override('select_first', select_first)

    return api.TVDBClient()
