#!/usr/bin/env python3
"""\
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

import os
import sys
import json
import random
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.colors import ListedColormap
from datetime import date, timedelta

os.system("")

ccodes = {'blue': 69,
          'orange': 166,
          'red': 160,
          'yellow': 220,
          'green': 64,
          'beige': 216,
          'purple': 140}

ansi_codes = {'reset': u'\u001b[0m'}

def pick_random(k, mnrt):
    rand_mn = random.sample(mnrt['other'].items(), k)
    return rand_mn

def get_color(code):
    return u'\u001b[38;5;{}m'.format(code)

def date_to_int(date):
    return int(date.replace('-', ''))

def get_prev_day(d):
    curr = date(*map(int, d.split('-')))
    prev = curr - timedelta(days=1)
    return int(str(prev).replace('-', ''))

def build_colormap(r, g, b):
    N = 10
    vals = np.ones((N, 4))
    vals[:, 0] = np.linspace(r/256, 1, N)[::-1]
    vals[:, 1] = np.linspace(g/256, 1, N)[::-1]
    vals[:, 2] = np.linspace(b/256, 1, N)[::-1]
    cmap = ListedColormap(vals)
    return cmap

error_sym = get_color(ccodes['red']) + '!' + ansi_codes['reset']
add_sym = get_color(ccodes['green']) + '+' + ansi_codes['reset']
del_sym = get_color(ccodes['orange']) + '-' + ansi_codes['reset']
change_sym = get_color(ccodes['purple']) + '~' + ansi_codes['reset']
save_sym = get_color(ccodes['beige']) + '.' + ansi_codes['reset']
list_sym = get_color(ccodes['blue']) + '>' + ansi_codes['reset']
warning_sym = get_color(ccodes['yellow']) + '?' + ansi_codes['reset']

data_fls = ['meaning_rating', 'config', 'log']

def main():

    aargs = sys.argv
    args = aargs[1:] if len(aargs) != 1 else []

    js_load = []
    for fn in data_fls:
        with open(os.path.join(os.path.dirname(__file__), 'data', fn + '.json'), 'r') as fl_tmp:
            js_load.append(json.load(fl_tmp))
            fl_tmp.seek(0)
    meaning_rating, cfg, log = js_load

    if len({"-h", "--help"} & set(args)) != 0:
        print(__doc__.rstrip())
        sys.exit(0)

    if len(args) == 0 or args[0] == 'daily':
        def_opts = [(k, v) for k, v in meaning_rating['default'].items()]
        rand_mns = pick_random(cfg['num_options']-len(def_opts), meaning_rating)
        mns = def_opts + rand_mns

        for i, (k, v) in enumerate(mns):
            print(' ', i+1, list_sym, '{} ({})'.format(k, v))
        i_other = len(mns)+1
        print(' ', i_other, list_sym, 'Other:')
        
        print('')
        chosen_opt = input('Option number: ')
        while not chosen_opt.isdigit() or int(chosen_opt) > cfg['num_options'] + 1:
            print(' {} '.format(error_sym), 'Invalid option')
            chosen_opt = input('Option number: ')
        chosen_opt = int(chosen_opt)

        today = date.today()
        if chosen_opt != i_other:
            chosen_mn, chosen_rt = mns[chosen_opt-1][0], mns[chosen_opt-1][1]
            print(' {} '.format(save_sym), '{} logged "{}" with mood rating {}'.format(today, chosen_mn, chosen_rt))
            log[str(today)] = [chosen_mn, chosen_rt]
        else:
            other_mn = input('IHTFP Meaning: ')
            other_rt = input('Mood rating: ')

            while not other_rt.isdigit() or int(other_rt) > 10 or int(other_rt) == 0:
                print(' {} '.format(error_sym), 'Invalid mood rating')
                other_rt = input('Mood rating: ')
            
            other_rt = int(other_rt)
            meaning_rating['other'][other_mn] = other_rt
            print(' {} '.format(add_sym), 'added "{}" with mood rating {}'.format(other_mn, other_rt))
            print(' {} '.format(save_sym), '{} logged "{}" with mood rating {}'.format(today, other_mn, other_rt))
            log[str(today)] = [other_mn, other_rt]
    elif args[0] == 'plot':
        lst_func = (lambda k, v: (date_to_int(k), k, v[1]))
        sort_func = (lambda x: x[0])
        log_lst = sorted([lst_func(k, v) for k, v in log.items()], key=sort_func, reverse=True)
        len_log = len(log_lst)
        time = cfg['time']

        mood_array = [[0]*time for _ in range(7)]
        log_pos = 0
        prev_log_val = ''

        for c in range(time):
            for r in range(7):
                if log_pos > len_log - 1:
                    mood_array[6-r][time-1-c] = 0
                else:
                    curr_log = log_lst[log_pos]
                    if prev_log_val == '' or curr_log[0] == get_prev_day(prev_log_val):
                        mood_array[6-r][time-1-c] = curr_log[2]
                        log_pos += 1
                    prev_log_val = curr_log[1]
    
        scaled_ma = np.repeat(np.repeat(mood_array, repeats=15, axis=0), repeats=15, axis=1)    
        cmap = build_colormap(cfg['color'][0], cfg['color'][1], cfg['color'][2])
        plt.axis('off')

        save_path = os.path.expanduser('~')
        plt.imsave(os.path.join(save_path, '{}_mood_plot.png'.format(str(date.today()))), scaled_ma, vmin=0.0, vmax=10.0, cmap=cmap)
        plt.close()
        print(' {} '.format(save_sym), 'saved mood plot to {}'.format(os.path.join(save_path, '{}_mood_plot.png'.format(str(date.today())))))
    elif args[0] == 'add':
        if len(args) != 3:
            print(' {} '.format(error_sym), 'Incorrect number of parameters')
            sys.exit(0)
        meaning = args[1]
        rating = args[2]
        if not rating.isdigit() or int(rating) > 10 or int(rating) == 0:
            print(' {} '.format(error_sym), 'Invalid mood rating')
            sys.exit(0)
        rating = int(rating)
        meaning_rating['other'][meaning] = rating
        print(' {} '.format(add_sym), 'added "{}" with mood rating {}'.format(meaning, rating))
    elif args[0] == 'del':
        if len(args) != 2:
            print(' {} '.format(error_sym), 'Incorrect number of parameters')
            sys.exit(0)
        meaning = args[1]
        deleted = 0
        for assoc, d in meaning_rating.items():
            if meaning in d:
                if assoc == 'default':
                    del_default = input(' ' + warning_sym + ' continue deleting default option "{}" [y/N] '.format(meaning))
                    delete = True if del_default.lower() == 'y' else False
                else: delete = True
                if delete:
                    del meaning_rating[assoc][meaning]
                    deleted += 1
        print(' {} '.format(del_sym), 'deleted {} instance(s) of "{}"'.format(deleted, meaning))
    elif args[0] == 'export':
        if len(args) < 2:
            print(' {} '.format(error_sym), 'Incorrect number of parameters')
            sys.exit(0)
        if args[1] == 'color':
            if len(args) != 5:
                print(' {} '.format(error_sym), 'Incorrect number of parameters')
                sys.exit(0)
            color = args[2:]
            try: new = [int(c) for c in color]
            except:
                print(' {} '.format(error_sym), 'Invalid RGB value')
                sys.exit(0)
            cfg['color'] = new
            new = tuple(new)
            name = 'color'
        elif args[1] == 'time':
            if len(args) != 3:
                print(' {} '.format(error_sym), 'Incorrect number of parameters')
                sys.exit(0)
            time = args[2]
            if not time.isdigit():
                print(' {} '.format(error_sym), 'Invalid time period')
                sys.exit(0)
            new = int(time)
            cfg['time'] = new
            name = 'time'
        elif args[1] == 'num_options':
            if len(args) != 3:
                print(' {} '.format(error_sym), 'Incorrect number of parameters')
                sys.exit(0)
            nops = args[2]
            if not nops.isdigit():
                print(' {} '.format(error_sym), 'Invalid number of options')
                sys.exit(0)
            new = int(nops)
            cfg['num_options'] = new
            name = 'number of options'
        else:
            print(' {} '.format(error_sym), '{} is not a valid config variable'.format(args[1]))
            sys.exit(0)
        print(' {} '.format(change_sym), 'set {} to {}'.format(name, new))
    else:
        print(' {} '.format(error_sym), '{} is not a valid command'.format(args[0]))
        sys.exit(0)

    for i, fn in enumerate(data_fls):
        with open(os.path.join(os.path.dirname(__file__), 'data', fn + '.json'), 'w') as fl_tmp:
            json.dump(js_load[i], fl_tmp, indent=4)

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt:
        print('')
        print('interrupted... exiting')
        sys.exit(0)