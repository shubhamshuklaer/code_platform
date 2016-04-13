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
from bs4 import BeautifulSoup
import re
import pickle


APP_NAME = 'PYTHON_SPOJ'
CONFIG = 'config'
COOKIE = 'cookie'
PROBLEM_DATABASE_NAME='problem_database'
TAGS_DATABASE_NAME='tags_database'

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




def get_info(prob_dir):
    if not os.path.exists(prob_dir):
        return False,None,None,None
    info_file=os.path.join(prob_dir,'info.txt')
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

def get_response(br,url):
    ungzip_response(br.open(url),br)
    return br.response()

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


def fix_string(string):
    # \xa0 is actually non-breaking space in Latin1 (ISO 8859-1), also
    # chr(160). You should replace it with a space. string =
    # string.replace(u'\xa0', u' ')
    # str will convert unicode to normal string
    # http://stackoverflow.com/questions/24358361/removing-u2018-and-u2019-character
    #  return str(string.replace(u'\xa0', u' ').replace(u"\u2018", "'").replace(u"\u2019", "'").strip())
    return str(string.encode("ascii","ignore")).strip()

def set_problem_database(problem_database):
    app_dir = get_add_dir()
    problem_database_file = os.path.join(app_dir, PROBLEM_DATABASE_NAME)
    with open(problem_database_file,"w") as f:
        pickle.dump(problem_database,f)

def get_problem_database():
    app_dir = get_add_dir()
    problem_database_file = os.path.join(app_dir, PROBLEM_DATABASE_NAME)
    if os.path.exists(problem_database_file):
        with open(problem_database_file,"r") as f:
            return pickle.load(f)
    else:
        click.echo("Update problem database first")
        return None

def set_tags_database(tags_database):
    app_dir = get_add_dir()
    tags_database_file = os.path.join(app_dir, TAGS_DATABASE_NAME)
    with open(tags_database_file,"w") as f:
        pickle.dump(tags_database,f)

def get_tags_database():
    app_dir = get_add_dir()
    tags_database_file = os.path.join(app_dir, TAGS_DATABASE_NAME)
    if os.path.exists(tags_database_file):
        with open(tags_database_file,"r") as f:
            return pickle.load(f)
    else:
        click.echo("Update tags_database first")
        return None

def print_problem_data(pd):
    # http://stackoverflow.com/questions/10623727/python-spacing-and-aligning-strings
    output="{0:5} {1:6} {2:50} {3:5} {4:5} {5:8} {6:6} {7:6} {8:6} {9:}".format(pd["solved"],pd["id"],pd["title"],pd["up_votes"],pd["down_votes"],pd["users"],pd["accuracy"],pd["implementation_diffi"],pd["conceptual_diffi"],pd["tags"])
    print(output)

def print_problem_database():
    problem_database=get_problem_database()
    # http://stackoverflow.com/questions/5466618/too-many-values-to-unpack-iterating-over-a-dict-key-string-value-list
    for key,val in problem_database.iteritems():
        print_problem_data(val)

def print_tags_database():
    tags_database=get_tags_database()
    for key,val in tags_database.iteritems():
        print(key+" : "+str(val))


def update_tags_database(problem_database,br):
    print("updating tags database")
    tags_database=dict()
    s=BeautifulSoup(get_response(br,urls.TAGS_DATABASE_URL),"lxml")
    tbody=s.find('table').find('tbody')
    for tr in tbody.find_all('tr'):
        tag_url=tr.find('a')['href']
        tag_name=fix_string(tr.find('a').get_text())
        tags_database[tag_name]=[]
        tbody_tag=BeautifulSoup(get_response(br,urls.BASE_URL+tag_url),"lxml").find("table",class_="problems").find('tbody')
        for tr_tag in tbody_tag.find_all('tr'):
            tds=tr_tag.find_all("td")
            prob_code=fix_string(tds[2].find("a",{"href": re.compile(".*problems.*")})["href"]).rsplit('/', 1)[-1]
            if prob_code in problem_database:
                # We are only getting problems from
                # http://www.spoj.com/problems/classical/
                tags_database[tag_name].append(prob_code)
                problem_database[prob_code]["tags"].append(tag_name)

        sys.stdout.write('\rTags database Len : '+str(len(tags_database)))
        sys.stdout.flush()
    sys.stdout.write('\r\n')
    sys.stdout.flush()

    set_tags_database(tags_database)

def process_tr(problem_database,tr):
    problem_data=dict()
    tds=tr.find_all("td")
    problem_data["solved"]= "fa-check" in tds[0].find("span")["class"]
    problem_data["id"]=fix_string(tds[1].get_text())
    problem_data["prob_code"]=fix_string(tds[2].find("a",{"href": re.compile(".*problems.*")})["href"]).rsplit('/', 1)[-1]
    problem_data["title"]=fix_string(tds[2].get_text())
    up_down_span=tds[3].find("span")
    up_votes=0
    down_votes=0
    if up_down_span != None:
        up_down_str=fix_string(up_down_span["title"])
        result=re.match("\+([0-9]+)\s+\-([0-9]+)",up_down_str)
        up_votes=int(result.group(1))
        down_votes=int(result.group(2))

    problem_data["up_votes"]=up_votes
    problem_data["down_votes"]=down_votes

    problem_data["users"]=fix_string(tds[4].get_text())
    problem_data["accuracy"]=fix_string(tds[5].get_text())
    difficulty_divs=tds[6].find_all("div",class_="progress-bar")

    # Heighest default difficulty
    problem_data["implementation_diffi"]=1
    problem_data["conceptual_diffi"]=1

    problem_data["tags"]=[]

    if len(difficulty_divs)>=1:
        problem_data["implementation_diffi"]=float(difficulty_divs[0]["aria-valuenow"])/float(difficulty_divs[0]["aria-valuemax"])
    if len(difficulty_divs)>=2:
        problem_data["conceptual_diffi"]=float(difficulty_divs[1]["aria-valuenow"])/float(difficulty_divs[1]["aria-valuemax"])
    if problem_data["prob_code"] not in problem_database:
        #  print_problem_data(problem_data)
        problem_database[problem_data["prob_code"]]=problem_data

def update_problem_database():
    br=login()
    if br == None:
        click.echo("Could not login")
        return

    problem_database=dict()
    done=False
    while not done:
        prev_len=len(problem_database)
        r=get_response(br,urls.PROBLEM_DATABASE_URL+"start="+str(prev_len))
        s=BeautifulSoup(r,"lxml")
        problem_table=s.find("table",class_="problems")
        if problem_table == None or problem_table.find("tbody") == None:
            click.echo("Problem couldn't find table")
            return

        problem_tbody=problem_table.find("tbody")
        for tr in problem_tbody.find_all("tr"):
            process_tr(problem_database,tr)

        if len(problem_database)==prev_len:
            done=True
        sys.stdout.write('\rProblem database Len : '+str(len(problem_database)))
        sys.stdout.flush()

    sys.stdout.write('\r\n')
    sys.stdout.flush()

    update_tags_database(problem_database,br)
    set_problem_database(problem_database)
    print_problem_database()
    print_tags_database()

def config_set_learning_rate():
    while True:
        extension = float(raw_input('set the learning rate: '))
        config.set_learning_rate(extension)
        if (extension<=1 and extension>=0):
            break
