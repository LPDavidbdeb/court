"""Extrait du journal PostgreSQL : démarrage/arrêt, connexions, attentes de verrou, interblocages.

Seules ces entrées et leurs compléments (DETAIL, CONTEXT, STATEMENT du même PID) sont gardées ;
toute autre entrée — notamment les erreurs attendues des suites, qui citent leurs données — est exclue.
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
tete = re.compile(r'^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+ \S+ \[(\d+)\] ')
entrees = []
for ligne in open(src, encoding='utf-8'):
    if tete.match(ligne) or not entrees:
        entrees.append([ligne])
    else:
        entrees[-1].append(ligne)
GARDER = re.compile(r'(listening on|database system is ready|connection received:|connection authorized:|'
                    r'still waiting for|acquired \w+Lock|deadlock detected|received fast shutdown|'
                    r'database system is shut down|shutting down)')
COMPLEMENT = re.compile(r'^\s*(?:\S+ ){2,3}\[\d+\] (?:\S+@\S+ )?(DETAIL|CONTEXT|STATEMENT|HINT):')
sortie, pid_garde = [], None
for e in entrees:
    m = tete.match(e[0]); pid = m.group(1) if m else None
    if GARDER.search(e[0]):
        sortie.extend(e); pid_garde = pid
    elif pid_garde and pid == pid_garde and COMPLEMENT.match(e[0]):
        sortie.extend(e)
    else:
        pid_garde = None
open(dst, 'w', encoding='utf-8').writelines(sortie)
print(len(entrees), 'entrées lues ;', len(sortie), 'lignes gardées')
