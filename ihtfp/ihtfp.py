#!/usr/bin/env python3

import os
import sys

from ihtfp.commands import daily, add, delete, export, undefined, help
from ihtfp.utils import load_json, dump_json

os.system("")

def program():
    data_filenames = ['meaning_rating', 'config', 'log']

    aargs = sys.argv
    args = aargs[1:] if len(aargs) != 1 else []

    if len({"-h", "--help"} & set(args)) != 0:
        help()

    if len(args) == 0 or args[0] == 'daily':
        meaning_rating, cfg, log = load_json('daily')
        meaning_rating, log = daily(meaning_rating, cfg, log)
        dump_json('daily', [meaning_rating, log])
    elif args[0] == 'add':
        meaning_rating, = load_json('add')
        meaning_rating = add(meaning_rating, args)
        dump_json('add', [meaning_rating])
    elif args[0] == 'del':
        meaning_rating, = load_json('del')
        meaning_rating = delete(meaning_rating, args)
        dump_json('del', [meaning_rating])
    elif args[0] == 'export':
        cfg, = load_json('export')
        cfg = export(cfg, args)
        dump_json('export', [cfg])
    else:
        undefined(args)

def main():
    try: program()
    except KeyboardInterrupt:
        print('\ninterrupted... exiting')
        sys.exit(0)

if __name__ == '__main__':
    main()