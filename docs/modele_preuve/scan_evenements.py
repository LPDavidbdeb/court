"""
Les événements de la cohabitation, classés par thème, et leur usage dans le corpus.

    .venv/bin/python manage.py shell < docs/modele_preuve/scan_evenements.py

Lecture seule. Voir CONCEPTION_PREUVE.md § 14.
"""
import re, datetime, glob, os, json
from collections import defaultdict, Counter
from events.models import Event
from case_manager.models import BordereauDepotJuillet as B
from django.contrib.contenttypes.models import ContentType

BASE = os.path.join(os.getcwd(), 'legal')
def ids_cites(text):
    out = set()
    for m in re.finditer(r'event-(\d+)', text, re.I): out.add(int(m.group(1)))
    for m in re.finditer(r'\bE-?(\d{1,3})\b', text):
        pass  # trop ambigu, ignoré
    for m in re.finditer(r'[Ee]vents?\s*(?:id\s*=\s*)?\[?((?:\d+\s*(?:,|et|à|–|-|\s)\s*)*\d+)', text):
        chunk = m.group(1)
        for r in re.finditer(r'(\d+)\s*(?:à|–)\s*(\d+)', chunk):
            a, b = int(r.group(1)), int(r.group(2))
            if 0 < b - a < 40: out.update(range(a, b+1))
        out.update(int(x) for x in re.findall(r'\d+', chunk))
    for m in re.finditer(r'Event:(\d+)', text): out.add(int(m.group(1)))
    return out

refs = {}
for f in sorted(glob.glob(f'{BASE}/implication_parentale_recurrence/*.md')):
    k = os.path.basename(f)[:2] + ('a' if '03a' in f else ''); refs[k] = refs.get(k, set()) | ids_cites(open(f).read())
corpus = defaultdict(set)
for f in glob.glob(f'{BASE}/**/*.md', recursive=True):
    if '/implication_parentale_recurrence/' in f: continue
    for i in ids_cites(open(f, errors='ignore').read()): corpus[i].add(os.path.relpath(f, BASE))
ct = ContentType.objects.get_for_model(Event)
juillet = {r.object_id: r.cote for r in B.objects.filter(content_type=ct)}

THEMES = [
 ('danse_mere', r"danse d.[ée]lise|cours de danse|[ée]lise (a|est [àa]) (des |ses )?cours|dance class|spectacle de danse d.[ée]lise"),
 ('garderie', r"garderie|maternelle|pr[ée]scolaire|[ée]cole"),
 ('activites', r"natation|piscine.*cours|ymca|acro|gym|soccer|r[ée]cital|cours d.alexia|cours de nicolas|ski|cheer"),
 ('maladie', r"malade|fi[èe]vre|m[ée]decin|h[ôo]pital|urgence|clinique|virus|grippe|otite|soins? de sant[ée]"),
 ('sorties', r"parc|escalade|plage|zoo|v[ée]lo|chalet|piscine|[îi]le|estrie|cabane|glissade|festival|mus[ée]e|patin|biblioth|march[ée]|plein air|randonn|sortie"),
 ('famille_paternelle', r"johanne|grand[- ]m[eè]re|grand[- ]p[eè]re|raymond|annie|s[oœ]ur de lp|sa s[oœ]ur|anniversaire|no[ëe]l|p[âa]ques|souper"),
 ('voyage', r"cuba|cape cod|voyage|vacances|bar harbor|floride|maine"),
 ('domicile_routine', r"chez lui avec|[àa] la maison|bain|coucher|dodo|souper|d[îi]ner|d[ée]jeuner|pyjama|routine"),
]
evs = Event.objects.filter(date__gte=datetime.date(2009,10,6), date__lt=datetime.date(2015,2,24)).order_by('date')
rows = []
for ev in evs:
    x = ' '.join((ev.explanation or '').split())
    themes = [t for t, p in THEMES if re.search(p, x, re.I)] or ['autre']
    in_ref = sorted(k for k, s in refs.items() if ev.pk in s)
    rows.append(dict(pk=ev.pk, date=str(ev.date), wd=ev.date.strftime('%a'), heure=ev.debut.strftime('%H:%M') if ev.debut else '', themes=themes,
                     ref=in_ref, juillet=juillet.get(ev.pk), corpus=sorted(corpus.get(ev.pk, []))[:3], n_corpus=len(corpus.get(ev.pk, [])),
                     photos=ev.linked_photos.count(), x=x[:170]))
print('événements de la cohabitation :', len(rows))
print('par thème :', dict(Counter(t for r in rows for t in r['themes'])))
print('dans une référence :', sum(1 for r in rows if r['ref']), '| cote de juillet :', sum(1 for r in rows if r['juillet']), '| ailleurs au corpus seulement :', sum(1 for r in rows if not r['ref'] and not r['juillet'] and r['n_corpus']), '| nulle part :', sum(1 for r in rows if not r['ref'] and not r['juillet'] and not r['n_corpus']))
