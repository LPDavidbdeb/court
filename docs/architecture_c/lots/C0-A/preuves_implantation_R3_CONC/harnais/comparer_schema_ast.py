"""Compare, par AST, les déclarations de champs et les classes Meta des modèles entre deux révisions."""
import ast, json, subprocess, sys
repo, revs = sys.argv[1], sys.argv[2:]
FICHIERS = ['document_manager/models.py', 'case_manager/models.py']
def declarations(source):
    out = {}
    for cls in ast.parse(source).body:
        if not isinstance(cls, ast.ClassDef):
            continue
        champs = [ast.unparse(n) for n in cls.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
        meta = [ast.unparse(n) for n in cls.body if isinstance(n, ast.ClassDef) and n.name == 'Meta']
        bases = [ast.unparse(b) for b in cls.bases]
        out[cls.name] = {'bases': bases, 'champs': champs, 'meta': meta}
    return out
res = {}
for f in FICHIERS:
    decl = {r: declarations(subprocess.run(['git', '-C', repo, 'show', f'{r}:{f}'], check=True,
                                           capture_output=True, text=True).stdout) for r in revs}
    ref = decl[revs[0]]
    res[f] = {r: ('IDENTIQUE' if d == ref else 'DIFFERENT') for r, d in decl.items()}
print(json.dumps({'reference': revs[0], 'comparaisons': res}, indent=1))
