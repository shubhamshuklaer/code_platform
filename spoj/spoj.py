__author__ = 'dheerendra'

import os
import mechanize
import utils
import urls
import click
import config
import ConfigParser
import re
from urllib import urlencode
from urllib2 import urlopen
from cSpinner import cSpinner
from bs4 import BeautifulSoup
import json
import time
import sys
#  import glob
import re
from subprocess import Popen,PIPE,STDOUT
import shlex

class Spoj():

    def __init__(self, problem, language, filename):
        self.problem = problem
        self.language = language
        self.filename = filename
        self.prob_dir=os.path.join(os.path.join(config.get_root(),'spoj'),self.problem)
        if not os.path.exists(self.prob_dir):
            os.mkdir(self.prob_dir)
        os.chdir(self.prob_dir)

    def num_inputs(self):
            return len([f for f in os.listdir('.') if re.match(r'i_[0-9]+\.txt', f)])

    def add_input(self,no_open_editor=False):
        # http://stackoverflow.com/questions/1320731/count-number-of-files-with-certain-extension-in-python
        #  num_inputs=len(glob.glob1(os.getcwd(),r'i_[0..9][0..9]*.txt'))
        index=str(self.num_inputs()+1)
        if no_open_editor:
            # http://stackoverflow.com/questions/12654772/create-empty-file-using-python
            open("i_"+index+".txt",'a').close()
            open("eo_"+index+".txt",'a').close()
        else:
            os.system(config.get_editor()+" i_"+index+".txt eo_"+index+".txt")

    def cmpile(self,should_commit=True):
        os.system('git add --all')
        cmd=config.get_cmp_cmd(self.language)
        cmd=cmd.replace('inp_file',self.filename)
        cmd=cmd.replace('out_file',self.problem)
        click.echo(cmd)
        ret_val=os.system(cmd)
        if ret_val == 0:
            status="success"
        else:
            status="failed"
        if should_commit:
            os.system('git commit -m "%s compile %s"' %(self.problem,status))
        if ret_val != 0:
            exit(2)

    def run(self,test_case_num,should_cmpile):
        if should_cmpile:
            self.cmpile(False)

        os.system('git add --all')
        cmd=config.get_run_cmd(self.language)
        cmd=cmd.replace('inp_file',self.filename)
        cmd=cmd.replace('out_file',self.problem)
        click.echo(cmd)
        if test_case_num is None:
            ret_val=os.system(cmd)
            correct_output= raw_input("Did it gave correct output(Y/N) [Y]") or "Y"
            message=self.problem+' return code '+str(ret_val)+ ' correct output :'+correct_output
        elif test_case_num == "0":
            success_list=[]
            failure_list=[]
            for i in range(1,self.num_inputs()+1):
                if self.run_helper(cmd,str(i)):
                    success_list.append(i)
                else:
                    failure_list.append(i)
            message="Num_success:"+str(len(success_list))+"/"+str(self.num_inputs())+" Success list: "
            message=message+str(success_list)+" Failure list: "+str(failure_list)

        else:
            success=self.run_helper(cmd,test_case_num)
            if success:
                message="Test case no. "+test_case_num+" ran with success"
            else:
                message="Test case no. "+test_case_num+" ran with failure"
        os.system('git commit -m " %s "' % (message))

    def run_helper(self,cmd,test_case_num):
        p=Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE, stdin=PIPE)
        p.stdin.write(open("i_"+test_case_num+".txt").read())
        expected_out=open("eo_"+test_case_num+".txt").read()
        output=p.stdout.read()
        open("o_"+test_case_num+".txt","w").write(output)
        if output == expected_out:
            click.echo("Test case num : "+test_case_num+" Success")
            return True
        else:
            click.echo("Test case num : "+test_case_num+" Failed")
            return False

    def start(self,no_open=False):
        prob_dir=os.path.join(os.path.join(config.get_root(),'spoj'),self.problem)

        if not os.path.exists(prob_dir):
            os.mkdir(prob_dir)

        prob_file=os.path.join(prob_dir,self.filename)
        prob_info_file=os.path.join(prob_dir,"info.txt")
        if not os.path.exists(prob_file):
            open(prob_file,'w')
        if not os.path.exists(prob_info_file):
            info=ConfigParser.ConfigParser()
            info.add_section('info')
            info.set('info','lang_code',self.language)
            info.set('info','prob_code',self.problem)
            info.set('info','file_name',self.filename)
            with open(prob_info_file,'wb') as info_file:
                info.write(info_file)

        if config.get_editor() is not None and not no_open:
            os.system('xdg-open '+urls.PROBLEM_URL+self.problem)
            os.chdir(prob_dir)
            os.system(config.get_editor()+" "+self.filename)



    # Using gzip for faster encoding of page
    # using factory=mechanize.RobustFactory() so to use a more robust parser as
    # the default parser was unable to handle www.spoj.com/submit/
    def submit(self):

        with open(self.filename, 'r') as codefile:
            solution = codefile.read()

        br=utils.login()

        if br == None:
            return False, 'Login failed'

        r=br.open(urls.SUBMIT_URL)
        utils.ungzip_response(r,br)
        # br.response().read() will return the html text
        #  click.echo(br.response().read())

        br.select_form(nr=0)
        # To fix error 'problemcode' is read only
        br.form.find_control('problemcode').readonly=False
        br['problemcode'] = self.problem
        br['file'] = solution
        br['lang'] = [self.language]
        r=br.submit()
        utils.ungzip_response(r,br)
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


    def fetch_status(self):
        submissionId = self.submissionId
        while True:
            r = urlopen(urls.STATUS_URL,
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
                if "accepted" in data['status_description']:
                    prob_db=utils.get_problem_database()
                    prob_db[self.problem]['solved']=True
                    utils.set_problem_database(prob_db)
                break
            else:
                soup = BeautifulSoup(data['status_description'],"lxml")
                string = soup.get_text().strip()
                string = string.replace('\t', '')
                string = string.replace('\n', '')
                sys.stdout.write('\r\x1b[KStatus: %s' % string)
                sys.stdout.flush()
            time.sleep(0.5)


