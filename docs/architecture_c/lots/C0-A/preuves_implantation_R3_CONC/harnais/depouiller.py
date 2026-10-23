"""Dépouille un journal unittest : issue de chaque essai et message de l'exception."""
import json, re, sys
lignes = open(sys.argv[1], encoding='utf-8').read().split('\n')
issues = {}
for l in lignes:
    m = re.match(r'^(test_\S+) \((\S+)\)', l)
    if m:
        nom = m.group(1)
        fin = re.search(r'\.\.\. (ok|FAIL|ERROR)\s*$', l)
        issues.setdefault(nom, fin.group(1) if fin else None)
    elif l.strip() in ('ok', 'FAIL', 'ERROR'):
        for k, v in issues.items():
            if v is None:
                issues[k] = l.strip()
incidents = []
for i, l in enumerate(lignes):
    m = re.match(r'^(FAIL|ERROR): (test_\S+) \((\S+)\)\s*(.*)$', l)
    if not m:
        continue
    msg = ''
    for j in range(i + 1, len(lignes)):
        if lignes[j].startswith('======'):
            break
        if re.match(r'^[A-Za-z_.]*(Error|Exception|Refusee|Concluant)\b', lignes[j]):
            msg = lignes[j]
            break
    incidents.append({'type': m.group(1), 'essai': m.group(2), 'sous_cas': m.group(4).strip(' ()'), 'message': msg[:400]})
# Les incidents FAIL/ERROR font foi : la sortie verbeuse entremêle les observations.
for x in incidents:
    issues[x['essai']] = 'ERROR' if x['type'] == 'ERROR' and issues.get(x['essai']) != 'FAIL' else 'FAIL'
issues = {k: (v if v in ('FAIL', 'ERROR') else 'ok') for k, v in issues.items()}
print(json.dumps({'issues': issues, 'incidents': incidents}, ensure_ascii=False, indent=1))
