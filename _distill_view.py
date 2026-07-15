# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('distill_analysis.json', encoding='utf-8'))
print('SCANNED:', d['scanned'])
print('RECURRING (>=3):')
for t, c in d['recurring_titles'].items():
    print('  %dx  %s' % (c, t))
print('ALL TITLES >=2:')
for t, c in sorted(d['title_counter'].items(), key=lambda x: -x[1]):
    if c >= 2:
        print('  %dx  %s' % (c, t))
print('CANDIDATES:')
for c in d.get('candidates', []):
    print('  conf=%.2f  %s (x%d) project=%s' % (c['confidence'], c['title'], c['count'], c['project_bound']))
print('VERB COUNTER:')
for v, c in sorted(d.get('verb_counter', {}).items(), key=lambda x: -x[1]):
    print('  %dx  %s' % (c, v))
