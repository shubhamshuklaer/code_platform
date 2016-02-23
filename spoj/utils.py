__author__ = 'dheerendra'

import click
import os
import getpass
import mechanize
import sys
import time
import lang
import ConfigParser

APP_NAME = 'PYTHON_SPOJ'
CONFIG = 'config'
COOKIE = 'cookie'

def get_add_dir():
    app_dir = click.get_app_dir(APP_NAME)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    return app_dir


def get_config_file():
    app_dir = get_add_dir()
    full_name = os.path.join(app_dir, CONFIG)
    if not os.path.isfile(full_name):
        open(full_name, 'a').close()
    return full_name


def get_cookie_file():
    app_dir = get_add_dir()
    full_name = os.path.join(app_dir, COOKIE)
    if not os.path.isfile(full_name):
        open(full_name, 'a').close()
    return full_name


def ask_pass():
    pass1 = getpass.getpass('Password: ')
    pass2 = getpass.getpass('Confirm Password: ')
    if pass1 == pass2:
        return pass1
    else:
        click.echo('Password didn\'t matched. Try again')
        return ask_pass()


def encode(string):
    return string.encode('base64').encode('rot13')


def decode(string):
    return string.decode('rot13').decode('base64')


def setup_browser(br):
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br


def save_cookies(cj):
    cookie_file = get_cookie_file()
    cj.save(filename=cookie_file, ignore_discard=True)


def load_cookies(cj):
    cookie_file = get_cookie_file()
    cj.revert(filename=cookie_file, ignore_discard=True)


def animate(msg):
    animation = ['.', ',', '*', 'O']
    for a in animation:
        sys.stdout.write('\r%s %s' % (a, msg))
        sys.stdout.flush()
        time.sleep(0.5)


def ask_credentials():
    username = raw_input('Username: ')
    password = ask_pass()
    return username, password

def ask_extension():
    lang_code = raw_input('Enter language code: ')
    click.echo(lang.LANG_DICT[int(lang_code)])
    extension = raw_input('Enter extension(ignore the dot): ')
    return lang_code,extension

def ask_cmp_cmd():
    lang_code = raw_input('Enter language code: ')
    click.echo(lang.LANG_DICT[int(lang_code)])
    cmp_cmd = raw_input('Enter cmp_cmd(inp_file and out_file placeholder): ')
    return lang_code,cmp_cmd

def get_info(cwd):
    info_file=os.path.join(cwd,'info.txt')
    if not os.path.exists(info_file):
        return False,None,None,None
    config=ConfigParser.ConfigParser()
    config.read(info_file)
    return True,config.get('info','prob_code'),config.get('info','lang_code'),config.get('info','file_name')
