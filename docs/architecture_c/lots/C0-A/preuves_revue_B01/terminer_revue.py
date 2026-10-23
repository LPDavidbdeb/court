"""Phases bornées de revue B01; jamais de connexion directe ni de réglages réels."""
from pathlib import Path
import subprocess,json,hashlib,shutil
r=Path(__file__).resolve().parents[1]
expected=json.loads((r/'candidat_sha256.json').read_text())
def check():
 for n,sha in expected.items():
  assert hashlib.sha256((r/'repo'/n).read_bytes()).hexdigest()==sha,n
check()
results=[]
def run(name,labels):
 cmd=[str(r/'venv/bin/python'),str(r/'harness/run_tests.py'),name,*labels]
 p=subprocess.run(cmd,cwd=r/'repo',stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
 results.append({'journal':name,'commande':cmd,'code':p.returncode})
 print(name,'code',p.returncode,flush=True)
run('candidat-outillage',['scripts.regime_citations.test_projection','scripts.regime_citations.test_verifier_ab'])
run('candidat-schema',['C0A_SCHEMA_CHECK'])
# Contre-épreuve ciblée : uniquement les deux modules de production antérieurs,
# exactement tels que reconstruits depuis le premier patch. Tests corrigés A conservés.
modules=('concordance.py','protection.py');current={n:(r/'repo/document_manager'/n).read_bytes() for n in modules}
try:
 for n in modules:shutil.copyfile(r/'avant_delta'/n,r/'repo/document_manager'/n)
 run('ancienne-contre-epreuve-A',['document_manager.test_e01_numerotation.C0ARepriseConcurrence'])
 run('ancienne-contre-epreuve-B',['revue_b01_B_tests.RevueB01.test_B01_statement_initial_refuse','revue_b01_B_tests.RevueB01.test_B01_citation_initial_refuse'])
finally:
 for n,data in current.items():(r/'repo/document_manager'/n).write_bytes(data)
 check()
 (r/'logs/phases_complementaires.json').write_text(json.dumps({'phases':results,'candidat_restaure_sha256':expected},indent=2)+'\n')
print('Candidat corrigé restauré et huit empreintes vérifiées.',flush=True)
