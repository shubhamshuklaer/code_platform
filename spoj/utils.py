__author__ = 'dheerendra'

import click
import os
import getpass
import mechanize
import sys
import time
import lang
import ConfigParser
import config
import urls
import readline
from subprocess import Popen

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




def get_info(cwd):
    info_file=os.path.join(cwd,'info.txt')
    if not os.path.exists(info_file):
        return False,None,None,None
    tmp_config=ConfigParser.ConfigParser()
    tmp_config.read(info_file)
    return True,tmp_config.get('info','prob_code'),tmp_config.get('info','lang_code'),tmp_config.get('info','file_name')



#  http://mattshaw.org/news/python-mechanize-gzip-response-handling/
def ungzip_response(r,b):
    headers = r.info()
    if headers['Content-Encoding']=='gzip':
        import gzip
        gz = gzip.GzipFile(fileobj=r, mode='rb')
        html = gz.read()
        gz.close()
        headers["Content-type"] = "text/html; charset=utf-8"
        r.set_data( html )
        b.set_response(r)

def login(username=None,password=None):
    if username is None:
        username, password = config.get_credentials()
        if username is None:
            username, password = utils.ask_credentials()

    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)
    br.addheaders.append( ['Accept-Encoding','gzip'] )

    try:
        r=br.open(urls.BASE_URL)
        ungzip_response(r,br)

        found=False
        for form in br.forms():
            if form.attrs['id'] == 'login-form':
                br.form = form
                found=True
                break

        if found == False:
            click.echo("Couldn't find login form")
            return None

        br['login_user'] = username
        br['password'] = password

        r=br.submit()
        ungzip_response(r,br)

        for link in br.links():
            if 'My profile' in link.text:
                click.echo('Login Success')
                return br

        click.echo('Wrong Username/Password. Try Again')
        return None
    except mechanize.URLError:
        click.echo('Error in connecting to internet. Please check your internet connection')
        return None

def verify_credentials(username,password):
    if login(username,password) == None:
        return False
    else:
        return True


def config_set_credentials():
    username, password = ask_credentials()
    click.echo('Verifying Credentials...Please wait')
    creds = verify_credentials(username, password)
    if not creds:
        return False
    config.set_credentials(username, password)
    return True

def ask_language():
    search_term=raw_input("enter lang name to search: ")
    click.echo("Search result")
    found=False
    for key in lang.LANG_DICT:
        val=lang.LANG_DICT[key]
        if search_term.lower() in val.lower():
            found=True
            click.echo(str(key)+" : "+val)

    if not found:
        click.echo("No such language found, try searching for something smaller")
        return None

    language=raw_input("enter language code: ")
    if int(language) in lang.LANG_DICT:
        click.echo("Language : "+lang.LANG_DICT[int(language)])
        return language
    else:
        click.echo("Choose proper language code")
        return None

def config_set_language():
    language=ask_language()
    if language is not None:
        config.set_language(language)
        return language
    else:
        return None

def config_set_root():
    # This will provide path autocompletion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")

    root=os.path.expanduser(raw_input("Enter root dir for storing the code: "))
    if not os.path.exists(root):
        os.mkdir(root)

    config.set_root(root)
    if not os.path.exists(os.path.join(root,'.git')):
        Popen(['git','init'],cwd=root)
    if not os.path.exists(os.path.join(root,'spoj')):
        os.mkdir(os.path.join(root,'spoj'))

def config_set_extension(lang_code):
    while True:
        if lang_code is None:
            lang_code = ask_language()
        extension = raw_input('Enter extension(ignore the dot): ')
        config.set_extension(lang_code,extension)
        lang_code=None
        if (raw_input("Do you wanna add extension for any other lang y/n[n] ") or "n") is "n":
            break

def config_set_cmp_cmd(lang_code):
    while True:
        if lang_code is None:
            lang_code = ask_language()
        cmp_cmd = raw_input('Enter cmp_cmd(inp_file and out_file placeholder): ')
        config.set_cmp_cmd(lang_code,cmp_cmd)
        lang_code=None
        if (raw_input("Do you wanna add cmp_cmd for any other lang y/n[n] ") or "n") is "n":
            break


def config_set_run_cmd(lang_code):
    while True:
        if lang_code is None:
            lang_code = ask_language()
        run_cmd = raw_input('Enter run_cmd(inp_file and out_file placeholder): ')
        config.set_run_cmd(lang_code,run_cmd)
        lang_code=None
        if (raw_input("Do you wanna add run_cmd for any other lang y/n[n] ") or "n") is "n":
            break

def config_set_editor():
    config.set_editor(raw_input('Enter editor: ') or "")
