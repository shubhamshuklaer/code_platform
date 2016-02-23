import os
import click
import lang
import utils
from subprocess import Popen
import config as Config
from spoj import Spoj


@click.group()
@click.version_option()
@click.pass_context
def main(ctx):
    pass

@click.command()
@click.pass_context
def cmpile(ctx):
    check,problem,language,filename=utils.get_info(os.getcwd())
    if not check:
        ctx.exit("Fix problems")
    spoj = Spoj(problem,language,filename)
    spoj.cmpile()
    pass

@click.command()
@click.argument('test_case_num',required=True)
@click.pass_context
def run(ctx,test_case_num):
    check,problem,language,filename=utils.get_info(os.getcwd())
    if not check:
        ctx.exit("Fix problems")
    spoj = Spoj(problem,language,filename)
    spoj.run(test_case_num)
    pass



@click.command()
@click.argument('problem',required=True)
@click.option('--language','-l')
@click.pass_context
def start(ctx,problem,language):
    if language is None:
        language=Config.get_language()
    if language is None:
        ctx.exit("Please set default lang or provide as argument")
    if Config.get_extension(language) is None:
        ctx.exit("Please set extension for lang "+language)
    if Config.get_cmp_cmd(language) is None:
        ctx.exit("Please set cmp_cmd for lang "+language)
    if Config.get_run_cmd(language) is None:
        ctx.exit("Please set run_cmd for lang "+language)
    spoj=Spoj(problem,language,problem+"."+Config.get_extension(language))
    spoj.start()
    pass


@click.command()
@click.pass_context
def submit(ctx):
    check,problem,language,filename=utils.get_info(os.getcwd())
    if not check:
        ctx.exit("Fix problems")
    spoj = Spoj(problem,language,filename)
    submit_status, message = spoj.submit()
    if submit_status:
        print message
        spoj.fetch_status()
    else:
        print message
    pass


@click.command()
@click.option('--language', '-l', help='Choose Default Language. \033[91mSee `spoj language`\033[0m',
              type=click.Choice(map(str, sorted([lan[0] for lan in lang.LANG]))))
@click.option('--credential', '-c', is_flag=True)
@click.option('--root','-r', help='Choose root directory for storing code')
@click.option('--extension','-e',help='Give extention for a file type',is_flag=True)
@click.option('--cmp_cmd',help='Give compile command, inp_file and out_file are placeholders',is_flag=True)
@click.option('--run_cmd',help='Give run command, inp_file and out_file are placeholders',is_flag=True)
@click.pass_context
def config(ctx, language, credential,root,extension,cmp_cmd,run_cmd):
    if credential:
        username, password = utils.ask_credentials()
        click.echo('Verifying Credentials...Please wait')
        creds = Spoj.verify_credentials(username, password)
        if not creds:
            ctx.exit()
        Config.set_credentials(username, password)
    if language is not None:
        Config.set_language(language)
    if root is not None:
        if os.path.exists(root):
            Config.set_root(root)
            if not os.path.exists(os.path.join(root,'.git')):
                Popen(['git','init'],cwd=root)
            if not os.path.exists(os.path.join(root,'spoj')):
                os.mkdir(os.path.join(root,'spoj'))
        else:
            click.echo('dir does not exist')
    if extension:
        lang_code,extension= utils.ask_extension()
        Config.set_extension(lang_code,extension)
    if cmp_cmd:
        lang_code,cmp_cmd=utils.ask_cmp_cmd()
        Config.set_cmp_cmd(lang_code,cmp_cmd)
    if run_cmd:
        lang_code,run_cmd=utils.ask_run_cmd()
        Config.set_run_cmd(lang_code,run_cmd)
    pass


@click.command()
def language():
    click.echo_via_pager('Supported Languages:\n' +
                             '\n'.join('\t\033[94m%s\033[0m : \033[91m%d\033[0m' % (lan[1], lan[0])
                                       for lan in lang.LANG))

@click.command()
def status():
    pass


main.add_command(submit)
main.add_command(config)
main.add_command(language)
main.add_command(status)
main.add_command(start)
main.add_command(cmpile)
main.add_command(run)
