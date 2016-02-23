__author__ = 'dheerendra'

import mechanize
import utils
import urls
import click
import config
import re
from urllib import urlencode
from urllib2 import urlopen
from cSpinner import cSpinner
from bs4 import BeautifulSoup
import json
import time
import sys

def ungzipResponse(r,b):
    headers = r.info()
    if headers['Content-Encoding']=='gzip':
        import gzip
        gz = gzip.GzipFile(fileobj=r, mode='rb')
        html = gz.read()
        gz.close()
        headers["Content-type"] = "text/html; charset=utf-8"
        r.set_data( html )
        b.set_response(r)

class Spoj():

    def __init__(self, problem, language, filename):
        self.problem = problem
        self.language = language
        self.filename = filename

    # Using gzip for faster encoding of page
    # using factory=mechanize.RobustFactory() so to use a more robust parser as
    # the default parser was unable to handle www.spoj.com/submit/
    def submit(self):
        username, password = config.get_credentials()
        if username is None:
            username, password = utils.ask_credentials()
        with open(self.filename.name, 'r') as codefile:
            solution = codefile.read()
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        br.set_handle_robots(False)
        br.addheaders.append( ['Accept-Encoding','gzip'] )
        r=br.open('http://www.spoj.com/')
        ungzipResponse(r,br)
        for form in br.forms():
            if form.attrs['id'] == 'login-form':
                br.form = form
                break
        br['login_user'] = username
        br['password'] = password
        r=br.submit()
        ungzipResponse(r,br)
        authorised = False
        for link in br.links():
            if 'My profile' in link.text:
                authorised = True
        if not authorised:
            return False, 'Invalid username/password'


        r=br.open('http://www.spoj.com/submit/')
        ungzipResponse(r,br)
        # br.response().read() will return the html text
        #  click.echo(br.response().read())

        br.select_form(nr=0)
        # To fix error 'problemcode' is read only
        br.form.find_control('problemcode').readonly=False
        br['problemcode'] = self.problem
        br['file'] = solution
        br['lang'] = [self.language]
        r=br.submit()
        ungzipResponse(r,br)
        response = br.response().read()
        wrong_code = re.search(r'wrong\s+problem', response, re.IGNORECASE)
        if wrong_code:
            return False, 'Wrong problem code'
        submissionId = re.search(r'name="newSubmissionId" value="(\d+)"', response, re.IGNORECASE)
        if submissionId:
            submissionId = submissionId.group(1)
            self.submissionId = submissionId
            return True, 'Problem submitted. Fetching Status!'
        else:
            return False, 'Not submitted, some error occurred'

        #s.stop()

    @staticmethod
    def verify_credentials(username, password):
        cj = mechanize.MozillaCookieJar()
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        br.set_cookiejar(cj)
        br = utils.setup_browser(br)
        try:
            #  click.echo(urls.BASE_URL)
            br.open(urls.BASE_URL)
            try:
                for form in br.forms():
                    if form.attrs['id'] == 'login-form':
                        br.form = form
                        break
                #  br.select_form(id='login-form')
                br['login_user'] = username
                br['password'] = password
                #br.find_control(name='autologin').items[0].selected = True
            except mechanize.FormNotFoundError:
                click.echo('Error occurred. Code VC-FNFE. Kindly contact developer')
                return False
            except NameError:
                click.echo('Error occurred. Code VC-NE. Kindly contact developer')
                return False
            except mechanize.ControlNotFoundError:
                click.echo('Error occurred. Code VC-CNFE. Kindly contact developer')
                return False
            br.submit()
            for link in br.links():
                if 'My profile' in link.text:
                    utils.save_cookies(cj)
                    click.echo('Account Verified!')
                    return True
            click.echo('Wrong Username/Password. Try Again')
            return False
        except mechanize.URLError:
            click.echo('Error in connecting to internet. Please check your internet connection')
            return False

    def fetch_status(self):
        submissionId = self.submissionId
        while True:
            r = urlopen('http://www.spoj.com/status/ajax=1,ajaxdiff=1',
                        data=urlencode(dict(
                            ids=submissionId
                        )))
            data = json.loads(r.read())
            data = data[0]
            final = data['final']
            if final == '1':
                print '\r\x1b[KResult: %s' % data['status_description'].strip()
                print 'Memory: %s' % data['mem'].strip()
                # Fixed no markup specified warning. If not specified it uses
                # best for the system but it can then behave differently for
                # different system
                soup = BeautifulSoup(data['time'],"lxml")
                time_taken = soup.get_text()
                print 'Time: %s' % time_taken.strip()
                break
            else:
                soup = BeautifulSoup(data['status_description'],"lxml")
                string = soup.get_text().strip()
                string = string.replace('\t', '')
                string = string.replace('\n', '')
                sys.stdout.write('\r\x1b[KStatus: %s' % string)
                sys.stdout.flush()
            time.sleep(0.5)


