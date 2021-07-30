#!/usr/bin/env python3
"""\
Usages:
    ihtfp                         choose daily ihtfp
    ihtfp daily                   choose daily ihtfp
    ihtfp graph                   generate and save graph

    ihtfp add "MEANING" RATING    add new meaning and rating
    ihtfp del "MEANING"           delete all instances of meaning
    ihtfp color R G B             change global graph color (rgb)
    ihtfp time WEEKS              set time period (number of weeks)

Options:
    -s,  --save                   save graph
    -sp, --save-at-path PATH      save graph at path
"""

import os
import sys
import argparse
import json
import random

from datetime import date

def pick_random(k, mnrt):
    rand_mn = random.sample(list(mnrt['neg'].items()) + list(mnrt['pos'].items()), k)
    return rand_mn

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
            opt_tmp = ' {} > {} ({})'.format(i+1, k, v)
            print(opt_tmp)
        i_other = len(mns)+1
        opt_other = ' {} > Other'.format(i_other)
        print(opt_other)
        
        print('')
        chosen_opt = input(' [*] Option number: ')
        while not chosen_opt.isdigit() or int(chosen_opt) > cfg['num_options'] + 1:
            print(' [!] Try again, enter the number associated with an option')
            chosen_opt = input(' [*] Option number: ')
        chosen_opt = int(chosen_opt)

        today = date.today()
        if chosen_opt != i_other:
            chosen_mn, chosen_rt = mns[chosen_opt-1][0], mns[chosen_opt-1][1]
            print(' [~] saved {} IHTFP as "{}" ({})'.format(today, chosen_mn, chosen_rt))
            log[str(today)] = [chosen_mn, chosen_rt]
        else:
            other_mn = input(' [+] New meaning: ')
            other_rt = input(' [+] New rating: ')

            while not other_rt.isdigit():
                print(' [!] Try again, enter a positive integer for the rating')
                other_rt = input(' + Other RATING: ')
            
            other_rt = int(other_rt)
            assoc = 'neg' if other_rt < 5 else 'pos'
            meaning_rating[assoc][other_mn] = other_rt
            print(' [~] saved {} IHTFP as "{}" ({})'.format(today, other_mn, other_rt))
            log[str(today)] = [other_mn, other_rt]
    elif args[0] == 'add':
        if len(args) != 3:
            print(' [!] Incorrect number of parameters')
            sys.exit()
        meaning = args[1]
        rating = args[2]
        if not rating.isdigit():
            print(' [!] Enter a positive integer for the rating')
            sys.exit()
        rating = int(rating)

        assoc = 'neg' if rating < 5 else 'pos'
        meaning_rating[assoc][meaning] = rating

        print(' [+] added "{}" with rating {}'.format(meaning, rating))
    elif args[0] == 'del':
        if len(args) != 2:
            print(' [!] Incorrect number of parameters')
            sys.exit()
        meaning = args[1]
        deleted = 0
        for assoc, d in meaning_rating.items():
            if meaning in d:
                del meaning_rating[assoc][meaning]
                deleted += 1
        print(' [-] Deleted {} instance(s) of "{}"'.format(deleted, meaning))
    elif args[0] == 'color':
        old_color = tuple(cfg['color'])
        if len(args) != 4:
            print(' ! Incorrect number of parameters')
            sys.exit()
        color = args[1:]
        try: color = [int(c) for c in color]
        except: print(' ! Invalid RGB value')
        cfg['color'] = color
        print(' [~] Changed color from {} to {}'.format(old_color, tuple(color)))
    elif args[0] == 'time':
        old_time = cfg['time']
        if len(args) != 2:
            print(' [!] Incorrect number of parameters')
            sys.exit()
        time = args[1]
        if not time.isdigit():
            print(' [!] Invalid value for time period')
            sys.exit()
        time = int(time)
        cfg['time'] = time
        print(' [~] Changed time period from {} to {} weeks'.format(old_time, time))

    # print(' ')
    # print(meaning_rating, '\n')
    # print(log, '\n')
    # print(cfg, '\n')

if __name__ == '__main__':
    main()