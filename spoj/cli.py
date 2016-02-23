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
@click.argument('filename', required=True, type=click.File())
@click.option('--problem', '-p', help='Problem code')
@click.option('--language', '-l', help='Language of problem. \033[91mSee `spoj language`\033[0m',
              type=click.Choice(map(str, sorted([lan[0] for lan in lang.LANG]))))
@click.pass_context
def submit(ctx, filename, problem, language):
    if problem is None:
        name = filename.name
        name = name.split('/')[-1]
        try:
            name = name.split('.')[-2]
        except Exception:
            name = name.split('.')[-1]
        problem = name.upper()
    problem = problem.upper()
    if language is None:
        language = Config.get_language()
    if language is None:
        language = raw_input('Language (Integer): ')
        if language not in map(str, [lan[0] for lan in lang.LANG]):
            ctx.exit('Language not supported. Please check `spoj language`.')
    spoj = Spoj(problem,language,filename)
    submit_status, message = spoj.submit()
    if submit_status:
        print message
        spoj.fetch_status()
    else:
        print message


@click.command()
@click.option('--language', '-l', help='Choose Default Language. \033[91mSee `spoj language`\033[0m',
              type=click.Choice(map(str, sorted([lan[0] for lan in lang.LANG]))))
@click.option('--credential', '-c', is_flag=True)
@click.option('--root','-r', help='Choose root directory for storing code')
@click.option('--extension','-e',help='Give extention for a file type',is_flag=True)
@click.option('--cmp_cmd',help='Give compile command, inp_file and out_file are placeholders',is_flag=True)
@click.pass_context
def config(ctx, language, credential,root,extension,cmp_cmd):
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