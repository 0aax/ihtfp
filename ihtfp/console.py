import sys
import utils as utils

ccodes = {'blue': 69,
          'orange': 166,
          'red': 160,
          'yellow': 220,
          'green': 64,
          'beige': 216,
          'purple': 140}

ansi_codes = {'reset': u'\u001b[0m'}

error_sym = utils.get_color(ccodes['red']) + '!' + ansi_codes['reset']
add_sym = utils.get_color(ccodes['green']) + '+' + ansi_codes['reset']
del_sym = utils.get_color(ccodes['orange']) + '-' + ansi_codes['reset']
change_sym = utils.get_color(ccodes['purple']) + '~' + ansi_codes['reset']
save_sym = utils.get_color(ccodes['beige']) + '.' + ansi_codes['reset']
list_sym = utils.get_color(ccodes['blue']) + '>' + ansi_codes['reset']
warning_sym = utils.get_color(ccodes['yellow']) + '?' + ansi_codes['reset']

def loop(msg, error_msg, cond):
    prompt = '{}: '.format(msg)
    var = input(prompt)
    
    while cond(var):
        error_message(error_msg)
        var = input(prompt)
    return var

def validate(error_msg, cond):
    if cond:
        error_message(error_msg)
        sys.exit(0)

def confirmation(msg):
    prompt = ' {} {} [y/N] '.format(warning_sym, msg)
    var = input(prompt)
    return var

def format_msg(sym, msg):
    """
    Formats console message.
    """
    return ' {} {}'.format(sym, msg)

def add_message(msg):
    print(format_msg(add_sym, msg))

def del_message(msg):
    print(format_msg(del_sym, msg))

def error_message(msg, exit=False):
    print(format_msg(error_sym, msg))
    if exit: sys.exit(0)

def change_message(msg):
    print(format_msg(change_sym, msg))

def save_message(msg):
    print(format_msg(save_sym, msg))

def list_message(i, msg):
    print(' {} {} {}'.format(i, list_sym, msg))

def help_message():
    help = \
    """
    Usages:
        ihtfp                         log daily ihtfp
        ihtfp daily                   log daily ihtfp
        ihtfp plot                    generate and save plot

        ihtfp add "MEANING" RATING    add new meaning and rating
        ihtfp del "MEANING"           delete all instances of meaning
        ihtfp export VAR VAL          change value in config

    Options:
        -h, --help                    get commands
    """
    print(help)
    sys.exit(0)