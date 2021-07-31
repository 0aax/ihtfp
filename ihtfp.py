#!/usr/bin/env python3
"""\
Usages:
    ihtfp                         choose daily ihtfp
    ihtfp daily                   choose daily ihtfp
    ihtfp graph                   generate and save graph

    ihtfp add "MEANING" RATING    add new meaning and rating
    ihtfp del "MEANING"           delete all instances of meaning
    ihtfp export VAR VAL          change value in config
"""

import os
import sys
import json
import random

from datetime import date

os.system("")

ccodes = {'blue': 69,
          'red': 160,
          'yellow': 220,
          'green': 64,
          'beige': 216,
          'purple': 140}

ansi_codes = {'reset': u'\u001b[0m'}

def pick_random(k, mnrt):
    rand_mn = random.sample(list(mnrt['neg'].items()) + list(mnrt['pos'].items()), k)
    return rand_mn

def get_color(code):
    return u'\u001b[38;5;{}m'.format(code)

error_sym = get_color(ccodes['red']) + '!' + ansi_codes['reset']
add_sym = get_color(ccodes['green']) + '+' + ansi_codes['reset']
del_sym = get_color(ccodes['yellow']) + '-' + ansi_codes['reset']
change_sym = get_color(ccodes['purple']) + '~' + ansi_codes['reset']
save_sym = get_color(ccodes['beige']) + '.' + ansi_codes['reset']
list_sym = get_color(ccodes['blue']) + '>' + ansi_codes['reset']

def main():

    aargs = sys.argv
    args = aargs[1:] if len(aargs) != 1 else []

    ## meanings ratings
    js_mr = open(os.path.join('data', 'meaning_rating.json'))
    meaning_rating = json.load(js_mr)
    ## config
    js_cfg = open(os.path.join('data', 'config.json'))
    cfg = json.load(js_cfg)
    ## log
    js_log = open(os.path.join('data', 'log.json'))
    log = json.load(js_log)

    if len({"-h", "--help"} & set(args)) != 0:
        print(__doc__.rstrip())
        sys.exit()

    if len(args) == 0 or args[0] == 'daily':
        def_opts = [(k, v) for k, v in meaning_rating['default'].items()]

        rand_mns = pick_random(cfg['num_options']-len(def_opts), meaning_rating)

        mns = def_opts + rand_mns

        for i, (k, v) in enumerate(mns):
            print(' ', i+1, list_sym, '{} ({})'.format(k, v))
        i_other = len(mns)+1
        print(' ', i_other, list_sym, 'Other')
        
        print('')
        chosen_opt = input('Option number: ')
        while not chosen_opt.isdigit() or int(chosen_opt) > cfg['num_options'] + 1:
            print(' {} '.format(error_sym), 'Invalid option')
            chosen_opt = input('Option number: ')
        chosen_opt = int(chosen_opt)

        today = date.today()
        if chosen_opt != i_other:
            chosen_mn, chosen_rt = mns[chosen_opt-1][0], mns[chosen_opt-1][1]
            print(' {} '.format(save_sym), '{} logged as "{}" with rating {}'.format(today, chosen_mn, chosen_rt))
            log[str(today)] = [chosen_mn, chosen_rt]
        else:
            other_mn = input('Meaning: ')
            other_rt = input('Rating: ')

            while not other_rt.isdigit():
                print(' {} '.format(error_sym), 'Invalid rating')
                other_rt = input('Rating: ')
            
            other_rt = int(other_rt)
            assoc = 'neg' if other_rt < 5 else 'pos'
            meaning_rating[assoc][other_mn] = other_rt
            print(' {} '.format(add_sym), 'added "{}" with rating {}'.format(other_mn, other_rt))
            print(' {} '.format(save_sym), '{} logged as "{}" with rating {}'.format(today, other_mn, other_rt))
            log[str(today)] = [other_mn, other_rt]
    elif args[0] == 'add':
        if len(args) != 3:
            print(' {} '.format(error_sym), 'Incorrect number of parameters')
            sys.exit()
        meaning = args[1]
        rating = args[2]
        if not rating.isdigit():
            print(' {} '.format(error_sym), 'Invaid rating')
            sys.exit()
        rating = int(rating)

        assoc = 'neg' if rating < 5 else 'pos'
        meaning_rating[assoc][meaning] = rating

        print(' {} '.format(add_sym), 'added "{}" with rating {}'.format(meaning, rating))
    elif args[0] == 'del':
        if len(args) != 2:
            print(' {} '.format(error_sym), 'Incorrect number of parameters')
            sys.exit()
        meaning = args[1]
        deleted = 0
        for assoc, d in meaning_rating.items():
            if meaning in d:
                del meaning_rating[assoc][meaning]
                deleted += 1
        print(' {} '.format(del_sym), 'deleted {} instance(s) of "{}"'.format(deleted, meaning))
    elif args[0] == 'export':
        if len(args) < 2:
            print(' {} '.format(error_sym), 'Incorrect number of parameters')
            sys.exit()
        if args[1] == 'color':
            if len(args) != 5:
                print(' {} '.format(error_sym), 'Incorrect number of parameters')
                sys.exit()
            color = args[2:]
            try: new = [int(c) for c in color]
            except: print(' {} '.format(error_sym), 'Invalid RGB value')
            cfg['color'] = new
            new = tuple(new)
            name = 'color'
        elif args[1] == 'time':
            if len(args) != 3:
                print(' {} '.format(error_sym), 'Incorrect number of parameters')
                sys.exit()
            time = args[2]
            if not time.isdigit():
                print(' {} '.format(error_sym), 'Invalid time period')
                sys.exit()
            new = int(time)
            cfg['time'] = new
            name = 'time'
        elif args[1] == 'num_options':
            if len(args) != 3:
                print(' {} '.format(error_sym), 'Incorrect number of parameters')
                sys.exit()
            nops = args[2]
            if not nops.isdigit():
                print(' {} '.format(error_sym), 'Invalid number of options')
                sys.exit()
            new = int(nops)
            cfg['num_options'] = new
            name = 'number of options'
        else:
            print(' {} '.format(error_sym), '{} is not a valid config variable'.format(args[1]))
            sys.exit()
        print(' {} '.format(change_sym), 'set {} to {}'.format(name, new))
    else:
        print(' {} '.format(error_sym), '{} is not a valid command'.format(args[0]))
        sys.exit()

    json.dumps(meaning_rating, js_mr, indent=4)
    json.dumps(log, js_log, indent=4)
    json.dumps(cfg, js_cfg, indent=4)

if __name__ == '__main__':
    main()