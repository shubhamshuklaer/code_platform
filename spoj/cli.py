import os
import click
import lang
import suggest_problem
import utils
from subprocess import Popen
import config as Config
from spoj import Spoj
from recommend import get_recommended_problem_code, set_rating

# http://click.pocoo.org/5/bashcomplete/
# Bash autocomplete
# _SPOJ_COMPLETE=source spoj > spoj-autocomplete.sh
# source /path/to/spoj-autocomplete.sh in bashrc

@click.group()
@click.version_option()
@click.pass_context
def main(ctx):
    pass


def get_info(prob_code):
    if prob_code != None:
        prob_dir=os.path.join(os.path.join(Config.get_root(),'spoj'),prob_code)
    else:
        prob_dir=os.getcwd()
    return utils.get_info(prob_dir)

@click.command()
@click.pass_context
def get_recommended(ctx):
    click.echo(get_recommended_problem_code())

@click.command()
@click.option('--rating', type=int)
@click.option('--prob_code')
@click.pass_context
def rate(ctx, rating, prob_code):
    # pass
    set_rating(rating, 45, prob_code, compute=False, SVDNeighbourhood=False)


@click.command()
@click.pass_context
def get_root(ctx):
    click.echo(Config.get_root())

@click.command()
@click.pass_context
def get_language(ctx):
    click.echo(Config.get_language())

@click.command()
@click.option('--language','-l')
@click.pass_context
def get_lang_info(ctx,language):
    if language == None:
        language=Config.get_language()
    click.echo("Compile cmd : "+str(Config.get_cmp_cmd(language)))
    click.echo("Run cmd : "+str(Config.get_run_cmd(language)))
    click.echo("Extension : "+str(Config.get_extension(language)))

@click.command()
@click.option('--language','-l')
@click.option('--cmpile_cmd')
@click.option('--run_cmd')
@click.option('--extension')
@click.pass_context
def set_lang_info(ctx,language,cmpile_cmd,run_cmd,extension):
    if language == None:
        language=Config.get_language()
    Config.set_cmp_cmd(language,cmpile_cmd)
    Config.set_run_cmd(language,run_cmd)
    Config.set_extension(language,extension)


@click.command()
@click.pass_context
def is_configured(ctx):
    click.echo(Config.is_configured())


@click.command()
@click.option('prob_code','-p',help="prob code")
@click.pass_context
def is_problem_started(ctx,prob_code):
    check,problem,language,filename=get_info(prob_code)
    if check:
        click.echo("1")
    else:
        click.echo("0")


@click.command()
@click.option('prob_code','-p',help="prob code")
@click.option('no_open_editor','-n',help="Don't open editor",is_flag=True)
@click.pass_context
def add_input(ctx,prob_code=None,no_open_editor=False):
    check,problem,language,filename=get_info(prob_code)
    if not check:
        ctx.exit("Problem does not exist run spoj start first")
    spoj = Spoj(problem,language,filename)
    spoj.add_input(no_open_editor)

@click.command()
@click.option('prob_code','-p',help="prob code")
@click.pass_context
def cmpile(ctx,prob_code=None):
    check,problem,language,filename=get_info(prob_code)
    if not check:
        ctx.exit("Problem does not exist run spoj start first")
    spoj = Spoj(problem,language,filename)
    spoj.cmpile()

@click.command()
@click.argument('test_case_num',required=False)
@click.option('prob_code','-p',help="prob code")
@click.option('should_cmpile','-c',help="Flag denoting should we compile",is_flag=True)
@click.pass_context
def run(ctx,test_case_num=None,prob_code=None,should_cmpile=False):
    check,problem,language,filename=get_info(prob_code)
    if not check:
        ctx.exit("Problem does not exist run spoj start first")
    spoj = Spoj(problem,language,filename)
    spoj.run(test_case_num,should_cmpile)



@click.command()
@click.option('prob_code','-p',help="prob code")
@click.pass_context
def submit(ctx,prob_code=None):
    check,problem,language,filename=get_info(prob_code)
    if not check:
        ctx.exit("Problem does not exist run spoj start first")
    spoj = Spoj(problem,language,filename)
    submit_status, message = spoj.submit()
    if submit_status:
        print message
        spoj.fetch_status()
    else:
        print message


@click.command()
@click.argument('problem',required=True)
@click.option('--language','-l')
@click.option('no_open','-n',help='do not open browser or editor',is_flag=True)
@click.pass_context
def start(ctx,problem,language,no_open=False):
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
    spoj.start(no_open)


@click.command()
@click.pass_context
def update_problem_database(ctx):
    utils.update_problem_database()

@click.command()
@click.pass_context
def set_learning_rate(ctx):
    utils.config_set_learning_rate()
    pass



@click.command()
@click.pass_context
def recommend_problem(ctx):
    rate = Config.get_learning_rate()
    while(rate is None):
        utils.config_set_learning_rate()
        rate = Config.get_learning_rate()
    suggest_problem.recommendProblem(rate)
    pass


@click.command()
@click.option('--language', '-l', help='Choose Default Language',
              is_flag=True)
@click.option('--credential', '-c', is_flag=True)
@click.option('--root','-r', help='Choose root directory for storing code',is_flag=True)
@click.option('--extension','-e',help='Give extention for a file type',is_flag=True)
@click.option('--cmp_cmd',help='Give compile command, inp_file and out_file are placeholders',is_flag=True)
@click.option('--run_cmd',help='Give run command, inp_file and out_file are placeholders',is_flag=True)
@click.option('--editor',help="Specify editor",is_flag=True)
@click.option('--config_all',help="Configure all options",is_flag=True)
@click.pass_context
def config(ctx, language, credential,root,extension,cmp_cmd,run_cmd,editor,config_all):
    tmp_lang=None
    if credential or config_all:
        if not utils.config_set_credentials():
            ctx.exit()
    if language or config_all:
        tmp_lang=utils.config_set_language()
        if tmp_lang is None:
            ctx.exit()
    if root or config_all:
        utils.config_set_root()
    if extension or config_all:
        utils.config_set_extension(tmp_lang)
    if cmp_cmd or config_all:
        utils.config_set_cmp_cmd(tmp_lang)
    if run_cmd or config_all:
        utils.config_set_run_cmd(tmp_lang)
    if editor or config_all:
        utils.config_set_editor()
    if config_all:
        # We came here means everything configured properly
        Config.set_configured()


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
main.add_command(add_input)
main.add_command(update_problem_database)
main.add_command(set_learning_rate)
main.add_command(recommend_problem)
main.add_command(get_root)
main.add_command(get_language)
main.add_command(get_lang_info)
main.add_command(set_lang_info)
main.add_command(is_configured)
main.add_command(is_problem_started)
main.add_command(get_recommended)
main.add_command(rate)

