import os

from oslo_config import cfg


OPTS = [
    cfg.StrOpt('apikey',
               secret=True,
               default=os.environ.get('TVDB_API_KEY'),
               help='API key from your TVDB account ENV[\'TVDB_API_KEY\']'),
    cfg.StrOpt('username',
               default=os.environ.get('TVDB_USERNAME'),
               help='Username from your TVDB account ENV[\'TVDB_USERNAME\']'),
    cfg.StrOpt('userpass',
               secret=True,
               default=os.environ.get('TVDB_PASSWORD'),
               help='Password from your TVDB account ENV[\'TVDB_PASSWORD\']'),
    cfg.StrOpt('service_url',
               default='https://api-dev.thetvdb.com',
               help='the url for thetvdb api service'),
    cfg.BoolOpt('verify_ssl_certs',
                default=True,
                help='flag for validating ssl certs for service url (https)'),
    cfg.BoolOpt('select_first',
                default=False,
                help='flag for selecting first series from search results'),
]

cfg.CONF.register_opts(OPTS, 'tvdb')


def _make_opt_list(opts, group):
    """Generate a list of tuple containing group, options

    :param opts: option lists associated with a group
    :type opts: list
    :param group: name of an option group
    :type group: str
    :return: a list of (group_name, opts) tuples
    :rtype: list
    """
    import copy
    import itertools

    _opts = [(group, list(itertools.chain(*opts)))]
    return [(g, copy.deepcopy(o)) for g, o in _opts]


def list_opts():
    """Returns a list of oslo_config options available in the library.

    The returned list includes all oslo_config options which may be registered
    at runtime by the library.
    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.
    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by this library.

    :returns: a list of (group_name, opts) tuples
    """
    return _make_opt_list([OPTS], 'tvdb')
