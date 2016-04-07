__author__ = 'dheerendra'

import ConfigParser
import utils
import lang


def is_configured():
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('configured', 'configured'):
        return config.get('configured', 'configured')
    else:
        return 0

def set_configured():
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    try:
        config.add_section('configured')
    except ConfigParser.DuplicateSectionError:
        pass
    config.set('configured', 'configured', "1")
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)


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


def set_root(root):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_section('root'):
        config.add_section('root')
    config.set('root','dir',root)

    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)

def set_extension(lang_code,extension):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_section('extension'):
        config.add_section('extension')
    config.set('extension',lang_code, extension)
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)

def get_extension(lang_code):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('extension', lang_code):
        return config.get('extension', lang_code)
    else:
        return None

def set_cmp_cmd(lang_code,cmp_cmd):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_section('cmp_cmd'):
        config.add_section('cmp_cmd')
    config.set('cmp_cmd',lang_code, cmp_cmd)
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)

def get_cmp_cmd(lang_code):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('cmp_cmd', lang_code):
        return config.get('cmp_cmd', lang_code)
    else:
        return None

def set_run_cmd(lang_code,run_cmd):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_section('run_cmd'):
        config.add_section('run_cmd')
    config.set('run_cmd',lang_code, run_cmd)
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)

def get_run_cmd(lang_code):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('run_cmd', lang_code):
        return config.get('run_cmd', lang_code)
    else:
        return None

def get_root():
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('root', 'dir'):
        return config.get('root', 'dir')
    else:
        return None

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

def set_editor(editor):
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if not config.has_section('editor'):
        config.add_section('editor')
    config.set('editor','editor', editor)
    with open(utils.get_config_file(), 'wb') as configfile:
        config.write(configfile)

def get_editor():
    config = ConfigParser.ConfigParser()
    config.read([utils.get_config_file()])
    if config.has_option('editor', "editor"):
        return config.get('editor', "editor")
    else:
        return None
