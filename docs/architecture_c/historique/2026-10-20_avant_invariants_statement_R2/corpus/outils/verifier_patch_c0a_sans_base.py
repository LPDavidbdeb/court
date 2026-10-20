"""Contre-épreuve documentaire : patch reconstruit en mémoire, doubles sans Django.

Aucune application du patch, aucun import applicatif, aucune connexion DB.
Ne remplace pas les tests Django/PostgreSQL à mandater sur le nouveau socle.
"""
import ast
import builtins
import hashlib
import json
import re
from pathlib import Path
from types import SimpleNamespace as NS

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
patch=(BASE/'lots/C0-A/C0A_DIFF_COMPLET.patch').read_text()
sources={}
for block in patch.split('diff --git ')[1:]:
    path=block.splitlines()[0].split(' b/',1)[1]
    old=(ROOT/path).read_text().splitlines(keepends=True)
    lines=block.splitlines(keepends=True)
    out=[]; pos=0; i=0
    while i<len(lines):
        m=re.match(r'@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@',lines[i])
        if not m: i+=1; continue
        start=int(m.group(1))-1
        out.extend(old[pos:start]); pos=start; i+=1
        while i<len(lines) and not lines[i].startswith('@@ '):
            l=lines[i]
            if l.startswith((' ','-')):
                assert old[pos]==l[1:], (path,pos,l)
                pos+=1
            if l.startswith((' ','+')): out.append(l[1:])
            i+=1
    out.extend(old[pos:]); new=''.join(out)
    ast.parse(new,filename=path)
    expected=re.search(r'^index [a-f0-9]+\.\.([a-f0-9]+)',block,re.M).group(1)
    blob=hashlib.sha1(f'blob {len(new.encode())}\0'.encode()+new.encode()).hexdigest()
    assert blob==expected, (path,blob,expected)
    sources[path]=new

class Statement: pass
class Rows(list):
    def filter(self,**kw):return Rows(x for x in self if all(getattr(x,k)==v for k,v in kw.items()))
    def select_related(self,*a):return self

source=NS(pk=1); cible=NS(pk=2); node=NS(document_id=2)
stmt=Statement(); stmt.pk=10
valid=NS(pk=30, document_id=1,content_type_id=7,object_id=10,content_object=stmt)
invalid=NS(pk=31, document_id=1,content_type_id=8,object_id=10,content_object=NS())
entry=NS(pk=5,cote='P-5')
appui=NS(statement_id=10,entree=entry,cote_citee='P-5',via_liasse='')
fake_models=NS(AppuiDepotJuillet=NS(objects=Rows([appui])))
def import_stub(name,*args,**kwargs):
    assert name=='case_manager.models', name
    return fake_models
bi=dict(vars(builtins)); bi['__import__']=import_stub
group=NS(document_source=source,document_source_id=1,document_cible_id=2,extremites=Rows())
env={'__builtins__':bi,'Statement':Statement,'RoleExtremite':NS(SOURCE='SOURCE',CIBLE='CIBLE'),
     'ContentType':NS(objects=NS(get_for_model=lambda model:NS(pk=7))),
     'correspondances_de':lambda n,r:Rows([group])}
tree=ast.parse(sources['document_manager/concordance.py'])
fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='appuis_dorigine')
exec(compile(ast.Module(body=[fn],type_ignores=[]),'patch:appuis_dorigine','exec'),env)
results=[]
for label,ants in [('valide_seul',[valid]),('valide_puis_invalide',[valid,invalid]),('invalide_puis_valide',[invalid,valid]),('valide_puis_archive',[valid,None])]:
    group.extremites=Rows(NS(role='SOURCE',noeud=x) for x in ants)
    try:
        values=env['appuis_dorigine'](node,document_source=source,document_cible=cible)
        result={'cas':label,'service':'retour','appuis':[v['entree'].pk for v in values]}
    except ValueError as e:
        result={'cas':label,'service':'ValueError','message':str(e),'appuis_restitues_par_catch_export':[]}
    results.append(result)
assert results[0]['appuis']==[5]
assert all(r['service']=='ValueError' for r in results[1:])
data={'nature':'CONTRE_EPREUVE_EN_MEMOIRE_AVEC_DOUBLES_PAS_TEST_DJANGO',
      'date':'2026-10-20','patch_sha256':hashlib.sha256(patch.encode()).hexdigest(),
      'sources_reconstruites_syntaxe_et_blob_verifies':list(sources),
      'cas':results,'diagnostic':'C0A-REV-01 confirmé pour la fonction exacte du patch; le catch export remet origines=[]; aucun test ORM/HTTP/SQL exécuté.'}
(BASE/'lots/C0-A/CONTRE_EPREUVE_LECTEUR_SANS_BASE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(data,ensure_ascii=False,indent=2))
