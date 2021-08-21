import os
import json
import random as rd
from datetime import date, timedelta

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
    return str(prev)

def get_colormap(base_color):
    """
    Returns dictionary of RGB equivalents of base color different alpha intervals.
    """
    colormap = {}

    for i in range(10):
        color_tmp = tuple(((1 - i/10) * 255) + (i/10 * v) for v in base_color)
        colormap[i] = color_tmp
    colormap[10] = tuple(base_color)
    
    return colormap

def save_ppm(width, height, window_size, arr):
    PPMheader = 'P6\n' + str(width*window_size) + ' ' + str(height*window_size) + '\n255\n'

    save_path = os.path.expanduser('~')
    with open(os.path.join(save_path, '{}_mood_plot.png'.format(str(date.today()))), 'wb') as f:
        f.write(bytearray(PPMheader, 'ascii'))
        arr.tofile(f)

def load_json(prim_arg):
    """
    Leads .json files as python dictionaries and collects them in an array.
    """
    js_load = []
    arg_load = {'daily': ['meaning_rating', 'config', 'log'],
                'add': ['meaning_rating'],
                'del': ['meaning_rating'],
                'export': ['config'],
                'plot': ['config', 'log']}

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