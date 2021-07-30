import json

fl = open('misc/ihtfp.txt').read().splitlines()
js_fl = open('data/meaning_rating.json', 'w')
fin = {"default": {}, "options": {}}
for ln in fl:
    fin["default"][ln] = 1
    fin["options"][ln] = 1
json.dump(fin, js_fl, sort_keys=True, indent=4)
js_fl.close()
