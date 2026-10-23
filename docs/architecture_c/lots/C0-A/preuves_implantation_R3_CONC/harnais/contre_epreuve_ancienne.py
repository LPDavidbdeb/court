"""Contre-épreuve R3-CONC : nouveaux essais contre les quatre modules de production de f35ec85.

Seuls les modules de production sont remplacés, dans la copie jetable du banc ; le
fichier d'essais reste celui du candidat. Le candidat est restauré et vérifié par
empreinte dans un `finally`. Aucune autre ressource n'est touchée.
"""
from pathlib import Path
import hashlib, json, subprocess, sys
r = Path(__file__).resolve().parents[1]
repo = r / 'repo'
MODULES = ['document_manager/concordance.py', 'document_manager/protection.py',
           'document_manager/models.py', 'document_manager/views/produced_views.py']
def sha(p): return hashlib.sha256((repo / p).read_bytes()).hexdigest()
def git(*a): return subprocess.run(['git', '-C', str(repo), *a], check=True, capture_output=True, text=True).stdout
assert git('status', '--porcelain') == '', 'copie non propre'
candidat = {p: sha(p) for p in MODULES + ['document_manager/test_e01_numerotation.py']}
tete = git('rev-parse', 'HEAD').strip()
phases = []
def run(nom, *labels):
    p = subprocess.run([str(r / 'venv/bin/python'), str(r / 'harness/run_tests.py'), nom, *labels],
                       cwd=repo, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, timeout=1200)
    phases.append({'journal': nom, 'etiquettes': list(labels), 'code': p.returncode})
    print(nom, 'code', p.returncode, flush=True)
try:
    for p in MODULES:
        (repo / p).write_bytes(subprocess.run(['git', '-C', str(repo), 'show', f'ancien-f35ec85:{p}'],
                                              check=True, capture_output=True).stdout)
    ancien = {p: sha(p) for p in MODULES}
    run('ancienne-contre-epreuve-R3',
        'document_manager.test_e01_numerotation.C0AR3Concurrence',
        'document_manager.test_e01_numerotation.C0AR3SauvegardeExistante',
        'document_manager.test_e01_numerotation.C0AR3Retrait')
    run('ancienne-contre-epreuve-reprise-C0A',
        'document_manager.test_e01_numerotation.C0ARepriseConcurrence')
finally:
    git('checkout', tete, '--', *MODULES)
    restaure = {p: sha(p) for p in candidat}
    assert restaure == candidat, 'restauration incomplète'
    assert git('status', '--porcelain') == '', 'copie non propre après restauration'
    (r / 'logs/contre_epreuve_ancienne.json').write_text(json.dumps(
        {'tete_candidat': tete, 'modules_anciens_sha256': ancien, 'candidat_restaure_sha256': restaure,
         'phases': phases}, indent=2) + '\n')
print('Candidat restauré ; empreintes vérifiées ; copie propre.', flush=True)
