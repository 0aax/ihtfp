import json

fl = open('ihtfp.txt').read().splitlines()
js_fl = open('assets/meaning_scores.json', 'w')
fin = {}
for ln in fl:
    fin[ln] = 1
json.dump(fin, js_fl, sort_keys=True, indent=4)
js_fl.close()
