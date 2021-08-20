import ihtfp.utils as utils
import ihtfp.console as console

from datetime import date

def daily(meaning_rating, cfg, log):
    """
    Displays ihtfp meanings and logs daily selection.
    """
    def_opts = [(k, v) for k, v in meaning_rating['default'].items()]

    rand_mns = utils.pick_random(cfg['num_options']-len(def_opts), meaning_rating)
    mns = def_opts + rand_mns

    for i, (k, v) in enumerate(mns):
        console.list_message(i+1, '{} ({})'.format(k, v))

    i_other = len(mns)+1
    console.list_message(i_other, 'Other:\n')

    chosen_opt = console.loop('Option number', 'Invalid option.', lambda x: not x.isdigit() or int(x) > cfg['num_options'] + 1)

    chosen_opt = int(chosen_opt)
    today = date.today()

    if chosen_opt != i_other:
        chosen_mn, chosen_rt = mns[chosen_opt-1][0], mns[chosen_opt-1][1]

        console.save_message('{} logged "{}" with mood rating {}'.format(today, chosen_mn, chosen_rt))
        
        log[str(today)] = [chosen_mn, chosen_rt]
    else:
        other_mn = input('IHTFP Meaning: ')

        other_rt = console.loop('Mood rating', 'Invalid rating.', lambda x: not x.isdigit() or int(x) > 10)
        
        other_rt = int(other_rt)
        meaning_rating['other'][other_mn] = other_rt
        log[str(today)] = [other_mn, other_rt]

        console.add_message('added "{}" with mood rating {}'.format(other_mn, other_rt))
        console.save_message('{} logged "{}" with mood rating {}'.format(today, other_mn, other_rt))
    
    return meaning_rating, log

def add(meaning_rating, args):
    """
    Adds new ihtfp meaning and rating to the .json file.
    """
    console.validate('Invalid number of parameters.', len(args) != 3)

    meaning, rating = args[1:3]

    console.validate('Invalid mood rating.', not rating.isdigit() or int(rating) > 10)

    rating = int(rating)
    meaning_rating['other'][meaning] = rating

    console.add_message('added "{}" with mood rating {}'.format(meaning, rating))

    return meaning_rating

def delete(meaning_rating, args):
    """
    Deletes all instances of matching meaning from .json file.
    """
    console.validate('Invalid number of parameters.', len(args) != 2)

    meaning = args[1]
    deleted = 0
    
    for assoc, d in meaning_rating.items():

        if meaning in d:
            if assoc == 'default':
                del_default = console.confirmation('continue deleting default option "{}"'.format(meaning))

                delete = True if del_default.lower() in {'y', 'yes'} else False
            else:
                delete = True

            if delete:
                del meaning_rating[assoc][meaning]
                deleted += 1

    console.del_message('deleted {} instance(s) of "{}"'.format(deleted, meaning))

    return meaning_rating

def export(cfg, args):
    """
    Modifies program config variables.
    """

    if args[1] == 'color':
        color_triple = export_color(args)
        cfg['color'] = color_triple

        changed = tuple(color_triple)
    elif args[1] == 'time':
        time_period = export_time(args)
        cfg['time'] = time_period
        
        changed = time_period
    elif args[1] == 'num_options':
        num_opts = export_num_options(args)
        cfg['num_options'] = num_opts

        changed = num_opts
    else:
        console.error_message('{} is not a recognized config variable'.format(args[1]), exit=True)
    
    console.change_message('changed {} to {}'.format(args[1], changed))

    return cfg

def export_color(args):
    """
    Parses rgb color triple from args.
    """
    console.validate('Incorrect number of parameters.', len(args) != 5)

    color = args[2:]
    console.validate('Invalid rgb value.', sum([1 if v.isdigit() else 0 for v in color]) != 3)

    color_triple = [int(v) for v in color]
    return color_triple

def export_time(args):
    """
    Parses time from args.
    """
    console.validate('Incorrect number of parameters.', len(args) != 3)

    time = args[2]
    console.validate('Invalid time period.', not time.isdigit())

    return int(time)

def export_num_options(args):
    """
    Parses number of options from args.
    """
    console.validate('Incorrect number of parameters', len(args) != 3)

    num_opts = args[2]
    console.validate('Invalid number of options.', not num_opts.isdigit())

    return num_opts

def undefined(args):
    """
    For unrecognized commands.
    """
    console.error_message('{} is not a recognized command.'.format(args[0]), exit=True)

def help():
    console.help_message()