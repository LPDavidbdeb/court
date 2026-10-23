"""Consigne références de reconstruction, environnement et isolation du banc R3-CONC (lecture seule)."""
import collections, hashlib, json, os, re, subprocess, sys
B, LIV = sys.argv[1], sys.argv[2]
repo = B + '/repo'
SOCLE = '515666eb8c6e7fdcdd265f9187c9c37b769b0fed'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def git(*a): return subprocess.run(['git', '-C', repo, *a], check=True, capture_output=True, text=True).stdout.strip()
def blob(rev, p): return hashlib.sha256(subprocess.run(['git', '-C', repo, 'show', f'{rev}:{p}'], check=True, capture_output=True).stdout).hexdigest()
HUIT = git('diff', '--name-only', SOCLE, 'candidat-r3-conc').splitlines()
def etat(rev): return {'commit_banc': git('rev-parse', rev), 'arbre': git('rev-parse', rev + '^{tree}'),
                       'fichiers_sha256': {p: blob(rev, p) for p in HUIT}}
rec = {'date_utc': subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip(),
       'banc': B, 'socle': SOCLE, 'livraison_reprise': 'f35ec8586866f4359d44f52a0bc5cc57c0804217',
       'conception_approuvee': 'b0adf1136c55c38a830d3a1cd1a4332741bf297d',
       'entrees_extraites_de_f35ec85': {f: sha(B + '/entrees/' + f) for f in sorted(os.listdir(B + '/entrees'))},
       'harnais_sha256': {f: sha(B + '/harness/' + f) for f in sorted(os.listdir(B + '/harness')) if f.endswith('.py')},
       'copie_git': {'remotes': git('remote'), 'alternates': os.path.exists(repo + '/.git/objects/info/alternates'),
                     'commits_sur_le_socle': git('log', '--format=%H %s', SOCLE + '..candidat-r3-conc').splitlines()},
       'ancien_candidat_f35ec85_reconstitue': etat('ancien-f35ec85'),
       'candidat_corrige_R3_CONC': dict(etat('candidat-r3-conc'),
           fichiers_du_delta=git('diff', '--name-only', 'ancien-f35ec85', 'candidat-r3-conc').splitlines(),
           delta_numstat=git('diff', '--numstat', 'ancien-f35ec85', 'candidat-r3-conc').splitlines(),
           delta_shortstat=git('diff', '--shortstat', 'ancien-f35ec85', 'candidat-r3-conc'),
           vs_socle_shortstat=git('diff', '--shortstat', SOCLE, 'candidat-r3-conc'),
           migrations_vs_socle=[p for p in HUIT if '/migrations/' in p]),
       'livrables_git_sha256': {f: sha(LIV + '/' + f) for f in sorted(os.listdir(LIV))}}
json.dump(rec, open(B + '/logs/reconstruction.json', 'w'), indent=1, ensure_ascii=False)
L = open(B + '/logs/postgresql.log', encoding='utf-8').read()
par = collections.Counter(re.findall(r'connection authorized: user=(\S+) database=(\S+)', L))
iso = {'cluster': {'initdb': '-U c0a_owner -A trust -E UTF8 --locale=C', 'port': 55439, 'listen_addresses': "''",
                   'socket': B + '/socket (mode 700)', 'log_connections': 'on', 'log_lock_waits': 'on', 'deadlock_timeout': '1s',
                   'ecoutes': sorted(set(re.findall(r'listening on (.*)', L)))},
       'connexions': {'recues': L.count('connection received:'), 'host_local': L.count('connection received: host=[local]'),
                      'par_role_base': {f'{u}@{d}': n for (u, d), n in sorted(par.items())}},
       'attentes_consignees': L.count('still waiting for'), 'acquises_apres_attente': len(re.findall(r'acquired \w+Lock', L)),
       'interblocages': L.count('deadlock detected'),
       'demarrages': L.count('database system is ready to accept connections'), 'arrets': L.count('database system is shut down'),
       'postmaster_pid_absent': not os.path.exists(B + '/pgdata/postmaster.pid'),
       'journal_complet': 'non versionne : contient des litteraux du jeu core.test_regime_citations_etape2 ; seul postgresql_extrait.log est livre'}
json.dump(iso, open(B + '/logs/isolation.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: iso[k] for k in ('connexions', 'attentes_consignees', 'interblocages', 'demarrages', 'arrets', 'postmaster_pid_absent')}, indent=1))
