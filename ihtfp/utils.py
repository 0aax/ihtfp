import os
import json
import random as rd
import numpy as np

from datetime import date, timedelta
from matplotlib.colors import ListedColormap

def pick_random(k, mnrt):
    rand_mn = rd.sample(mnrt['other'].items(), k)
    return rand_mn

def get_color(code):
    """
    Gets full ANSI color from code.
    """
    return u'\u001b[38;5;{}m'.format(code)

def date_to_int(date):
    """
    Converts string date into an int.
    """
    return int(date.replace('-', ''))

def get_prev_day(d):
    """
    Returns the date of the previous day.
    """
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

def load_json(prim_arg):
    """
    Leads .json files as python dictionaries and collects them in an array.
    """
    js_load = []
    arg_load = {'daily': ['meaning_rating', 'config', 'log'],
                'add': ['meaning_rating'],
                'del': ['meaning_rating'],
                'export': ['config']}

    for fn in arg_load[prim_arg]:
        with open(os.path.join(os.path.dirname(__file__), 'data', fn + '.json'), 'r') as fl_tmp:
            js_load.append(json.load(fl_tmp))
            fl_tmp.seek(0)

    return js_load

def dump_json(prim_arg, modified):
    """
    Dumps python dictionaries into json files.
    """
    arg_dump = {'daily': ['meaning_rating', 'log'],
                'add': ['meaning_rating'],
                'del': ['meaning_rating'],
                'export': ['config']}

    for i, fn in enumerate(arg_dump[prim_arg]):
        with open(os.path.join(os.path.dirname(__file__), 'data', fn + '.json'), 'w') as fl_tmp:
            json.dump(modified[i], fl_tmp, indent=4)