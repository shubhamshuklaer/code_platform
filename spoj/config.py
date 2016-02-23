__author__ = 'dheerendra'

import ConfigParser
import utils
import lang


def set_credentials(username,password):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    try:
        config.add_section('user')
    except ConfigParser.DuplicateSectionError:
        pass
    config.set('user', 'username', username)
    config.set('user', 'password', utils.encode(password))
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)


def set_language(language):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_section('language'):
        config.add_section('language')
    config.set('language', 'code', language)
    config.set('language', 'name', lang.LANG_DICT[int(language)])
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)


def get_language():
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('language', 'code'):
        return config.get('language', 'code')
    else:
        return None

def get_credentials():
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_option('user', 'username'):
        return None, None
    if not config.has_option('user', 'password'):
        return None, None
    return config.get('user', 'username'), utils.decode(config.get('user', 'password'))
