# http://click.pocoo.org/5/bashcomplete/
# Bash autocomplete
# _SPOJ_COMPLETE=source spoj > spoj-autocomplete.sh
# source /path/to/spoj-autocomplete.sh in bashrc

_spoj_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _SPOJ_COMPLETE=complete $1 ) )
    return 0
}

complete -F _spoj_completion -o default spoj;
