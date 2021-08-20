#!/usr/bin/env python3

import os
import sys

from ihtfp.commands import daily, add, delete, export, undefined, help
from ihtfp.utils import load_json, dump_json

os.system("")

def main():
    data_filenames = ['meaning_rating', 'config', 'log']

    aargs = sys.argv
    args = aargs[1:] if len(aargs) != 1 else []

    meaning_rating, cfg, log = load_json(data_filenames)

    if len({"-h", "--help"} & set(args)) != 0:
        help()

    if len(args) == 0 or args[0] == 'daily':
        meaning_rating, log = daily(meaning_rating, cfg, log)
    elif args[0] == 'add':
        meaning_rating = add(meaning_rating, args)
    elif args[0] == 'del':
        meaning_rating = delete(meaning_rating, args)
    elif args[0] == 'export':
        cfg = export(cfg, args)
    else:
        undefined(args)
    
    dump_json(data_filenames, [meaning_rating, cfg, log])
 
if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt:
        print('')
        print('interrupted... exiting')
        sys.exit(0)