"""Extract current Python domain classes statically; never import the application."""

import argparse
import ast
import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[4]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--date', required=True, help='Date documentaire YYYY-MM-DD')
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
date.fromisoformat(args.date)
OUT = args.output.resolve()
metadata_path = ROOT / 'docs/modele_preuve/diagrammes/erd_etat_actuel/schema_modeles.json'
metadata = json.loads(metadata_path.read_text())
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
if head != metadata['source_head']:
    raise SystemExit('Le relevé ORM et HEAD diffèrent. Actualiser le relevé ERD séparément avant de continuer.')
for relative, expected in metadata['source_sha256'].items():
    if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
        raise SystemExit('Le relevé ORM est périmé : ' + relative)

OUT.mkdir(parents=True, exist_ok=True)
style = Path(__file__).with_name('style.iuml')
if OUT != style.parent:
    (OUT / style.name).write_bytes(style.read_bytes())

models = {
    m['label']: m for m in metadata['models']
    if m['project'] and not m['auto_created_for']
}
orm_key = {label: m['app'] + '.models.' + m['name'] for label, m in models.items()}
technical = {m['label']: m for m in metadata['models'] if not m['project']}

# These are actual supporting classes. HTTP controllers, forms, admin classes,
# management-command wrappers, tests and third-party internals are out of scope.
support_sources = [
    'core/mixins.py', 'core/quote_regime.py', 'core/piece_import.py',
    'document_manager/numerotation.py', 'document_manager/protection.py',
    'document_manager/export_concordance.py', 'document_manager/reprise_numeros.py',
    'case_manager/cotes_concordance.py', 'case_manager/evidence_audit.py',
    'case_manager/piece_file_audit.py', 'photos/services.py', 'ai_services/utils.py',
    'argument_manager/mixins.py',
]
sources = sorted(set(metadata['source_sha256']) | set(support_sources))
trees = {p: ast.parse((ROOT / p).read_text()) for p in sources}
imports = {}
nodes = {}
classes = {}


def module_name(path):
    return path.removesuffix('.py').replace('/', '.')


def resolve_import(module, name):
    first, *rest = name.split('.')
    resolved = imports[module].get(first, module + '.' + first)
    return '.'.join([resolved] + rest)


def annotation(value):
    return ast.unparse(value) if value is not None else None


def literal_type(value):
    try:
        literal = ast.literal_eval(value)
        return type(literal).__name__ if literal is not None else None
    except (ValueError, TypeError, SyntaxError):
        return None


def signature(node):
    arguments = copy.deepcopy(node.args)
    positional = arguments.posonlyargs or arguments.args
    if positional and positional[0].arg in ('self', 'cls'):
        positional.pop(0)
    return node.name + '(' + ast.unparse(arguments) + ')'


for relative, tree in trees.items():
    module = module_name(relative)
    imports[module] = {'Exception': 'builtins.Exception'}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            if node.level:
                prefix = module.split('.')[:-node.level]
                imported = '.'.join(prefix + ([node.module] if node.module else []))
            else:
                imported = node.module or ''
            for item in node.names:
                imports[module][item.asname or item.name] = imported + '.' + item.name
        elif isinstance(node, ast.Import):
            for item in node.names:
                imports[module][item.asname or item.name.split('.')[0]] = item.name if item.asname else item.name.split('.')[0]
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            key = module + '.' + node.name
            nodes[key] = node
            imports[module][node.name] = key

for key, node in nodes.items():
    module = key.rsplit('.', 1)[0]
    bases = [resolve_import(module, ast.unparse(b)) for b in node.bases]
    enum = 'django.db.models.TextChoices' in bases
    orm = next((m for label, m in models.items() if orm_key[label] == key), None)
    decorators = [ast.unparse(d) for d in node.decorator_list]
    kind = 'model' if orm else 'enum' if enum else 'class'
    if key.startswith('core.mixins.') or key == 'argument_manager.mixins.EvidenceDeleteMixin':
        kind = 'mixin'
    if key in ('core.quote_regime.HeriteQuoteManager', 'core.quote_regime.PhraseQuoteManager'):
        kind = 'manager'
    if any(d.startswith('dataclass(') for d in decorators):
        kind = 'dataclass'
    attributes, methods, values = [], [], []
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decos = [ast.unparse(d) for d in item.decorator_list]
            if 'property' in decos or 'cached_property' in decos:
                attributes.append({'name': item.name, 'type': annotation(item.returns), 'kind': 'property', 'line': item.lineno})
            else:
                methods.append({'name': item.name, 'signature': signature(item), 'return': annotation(item.returns), 'decorators': decos, 'line': item.lineno})
        elif enum and isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name) and not target.id.startswith('_'):
                    value = ast.literal_eval(item.value)
                    values.append({'name': target.id, 'value': value[0] if isinstance(value, tuple) else value})
        elif not orm and isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            attributes.append({'name': item.target.id, 'type': annotation(item.annotation), 'kind': 'declared', 'line': item.lineno})
        elif isinstance(item, ast.Assign) and not enum and (not orm or any(isinstance(t,ast.Name) and t.id == 'champs_editables' for t in item.targets)):
            for target in item.targets:
                if isinstance(target, ast.Name) and not target.id.startswith('__'):
                    attributes.append({'name': target.id, 'type': literal_type(item.value), 'kind': 'class_attribute', 'line': item.lineno})
    if not orm and not enum:
        # Preserve instance members actually assigned in methods. No guessed
        # domain types or runtime targets are introduced for untyped members.
        seen = {a['name'] for a in attributes}
        for method in (m for m in node.body if isinstance(m, ast.FunctionDef)):
            for assignment in ast.walk(method):
                if not isinstance(assignment, ast.Assign):
                    continue
                for target in assignment.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self' and target.attr not in seen:
                        attributes.append({'name': target.attr, 'type': literal_type(assignment.value), 'kind': 'instance_attribute', 'line': assignment.lineno})
                        seen.add(target.attr)
    managers = []
    choices = []
    if orm:
        for item in node.body:
            if not isinstance(item, ast.Assign) or not isinstance(item.value, ast.Call):
                continue
            target_names = [t.id for t in item.targets if isinstance(t, ast.Name)]
            constructor = resolve_import(module, ast.unparse(item.value.func))
            if constructor in ('core.quote_regime.HeriteQuoteManager', 'core.quote_regime.PhraseQuoteManager', 'django.db.models.Manager'):
                managers += [{'name': name, 'target': constructor} for name in target_names]
            for keyword in item.value.keywords:
                if keyword.arg == 'choices' and isinstance(keyword.value, ast.Attribute) and keyword.value.attr == 'choices':
                    target = resolve_import(module, ast.unparse(keyword.value.value))
                    choices += [{'field': name, 'target': target} for name in target_names]
    classes[key] = {'key': key, 'name': node.name, 'module': module, 'source': module.replace('.', '/') + '.py', 'line': node.lineno,
                    'kind': kind, 'bases': bases, 'decorators': decorators, 'attributes': attributes,
                    'methods': methods, 'values': values, 'managers': managers, 'choices': choices,
                    'orm_label': orm['label'] if orm else None, 'orm': orm}

groups = [
    ('01_causes_documents', 'Causes, documents et structure', [k for k,c in classes.items() if c['orm'] and c['orm']['detail_view'] == '01_causes_documents']),
    ('02_historique_e01', 'Captures et concordance E01', [k for k,c in classes.items() if c['orm'] and c['orm']['detail_view'] == '02_historique_e01']),
    ('03_bordereau_appuis', 'Bordereau, appuis et ancrages', [k for k,c in classes.items() if c['orm'] and c['orm']['detail_view'] == '03_bordereau_appuis']),
    ('04_argumentation', 'Argumentation existante', [k for k,c in classes.items() if c['orm'] and c['orm']['app'] == 'argument_manager']),
    ('05_dossiers_transmissions', 'Dossiers et transmissions', [k for k,c in classes.items() if c['orm'] and c['orm']['detail_view'] == '05_dossiers_transmissions']),
    ('06_courriels', 'Courriels et citations de courriel', [k for k,c in classes.items() if c['orm'] and c['orm']['app'] == 'email_manager']),
    ('07_pdf_protagonistes', 'PDF, citations et protagonistes', [k for k,c in classes.items() if c['orm'] and c['orm']['app'] in ('pdf_manager','protagonist_manager')]),
    ('08_photos_evenements', 'Photographies et événements', [k for k,c in classes.items() if c['orm'] and c['orm']['detail_view'] == '07_photos_evenements']),
    ('09_google_chat', 'Google Chat', [k for k,c in classes.items() if c['orm'] and c['orm']['app'] == 'googlechat_manager']),
    ('10_utilisateurs_ia', 'Utilisateur et réponses IA', ['users.models.CustomUser', 'ai_services.models.GeminiResponse']),
    ('11_heritage_regimes', 'Mixins, gestionnaires et régime des citations', [k for k in classes if k.startswith(('core.mixins.', 'core.quote_regime.'))]),
    ('12_classes_services_e01', 'Classes de résultat et de protection E01', [k for k in classes if k.rsplit('.',1)[0] in ('document_manager.numerotation','document_manager.protection','document_manager.export_concordance','document_manager.reprise_numeros','case_manager.cotes_concordance')]),
    ('13_import_audit_traitement', 'Import, audit, traitement et mise en forme', [k for k in classes if k.rsplit('.',1)[0] in ('core.piece_import','case_manager.evidence_audit','case_manager.piece_file_audit','photos.services','ai_services.utils','argument_manager.mixins')]),
]
assignment = {}
for stem, title, keys in groups:
    for key in keys:
        if key in assignment:
            raise AssertionError('Duplicate class: ' + key)
        assignment[key] = stem
# A choice class is fully described next to its first owning model. The shared
# QuoteRegime is fully described with its two custom managers instead.
for key, cls in classes.items():
    if key not in assignment and cls['kind'] == 'enum':
        owners = sorted(k for k,c in classes.items() if any(d['target'] == key for d in c['choices']))
        if not owners:
            raise AssertionError('Unassigned enumeration: ' + key)
        assignment[key] = assignment[owners[0]]
assert set(assignment) == set(classes), 'A selected class has no complete view'


def target_key(label):
    if label not in orm_key and label not in technical:
        raise AssertionError('Unknown ORM target: ' + label)
    return orm_key[label] if label in orm_key else 'django_orm.' + label


edges = []
for key, cls in classes.items():
    for base in cls['bases']:
        edges.append({'source':key,'target':base,'kind':'inheritance','label':''})
    for choice in cls['choices']:
        edges.append({'source':key,'target':choice['target'],'kind':'choice','label':choice['field']})
    for manager in cls['managers']:
        edges.append({'source':key,'target':manager['target'],'kind':'manager','label':manager['name']})
    if cls['orm']:
        for f in cls['orm']['fields']:
            if 'target' in f:
                edges.append({'source':key,'target':target_key(f['target']),'kind':'association','label':f['name'],
                              'from_multiplicity':'0..1' if f['unique'] else '0..*',
                              'to_multiplicity':'0..1' if f['null'] else '1'})
        for f in cls['orm']['many_to_many']:
            edges.append({'source':key,'target':target_key(f['target']),'kind':'many_to_many','label':f['name'],
                          'from_multiplicity':'0..*','to_multiplicity':'0..*',
                          'through': None if f['through_auto'] else f['through']})
        for generic in cls['orm']['generic']:
            edges.append({'source':key,'target':'django.db.models.Model','kind':'generic','label':generic['name']})

# Dependencies below are limited to explicit class names used inside a class
# body, resolved from Python imports. They are code dependencies, not guessed
# persistent associations, call graphs, or an inference from matching PKs.
for key, cls in classes.items():
    if cls['orm'] or cls['kind'] in ('enum','manager','mixin'):
        continue
    module = cls['module']
    used = {resolve_import(module,n.id) for n in ast.walk(nodes[key]) if isinstance(n,ast.Name)}
    for target in sorted(used & classes.keys() - {key}):
        edges.append({'source':key,'target':target,'kind':'dependency','label':'utilise'})

framework_names = {
    'django.db.models.Model': 'django.db.models.Model',
    'django.db.models.Manager': 'django.db.models.Manager',
    'django.db.models.TextChoices': 'django.db.models.TextChoices',
    'treebeard.mp_tree.MP_Node': 'treebeard.mp_tree.MP_Node',
    'django.contrib.auth.models.AbstractUser': 'django.contrib.auth.models.AbstractUser',
    'django.core.exceptions.PermissionDenied': 'django.core.exceptions.PermissionDenied',
    'builtins.Exception': 'builtins.Exception',
}


def alias(key):
    return 'C_' + key.replace('.', '_')


def quoted(value):
    return str(value).replace('"', "'").replace('\n', ' ')


def field_type(field):
    if 'target' in field:
        return field['target']
    types = {'CharField':'str','TextField':'str','EmailField':'str','URLField':'str','FileField':'FieldFile','ImageField':'ImageFieldFile',
             'BooleanField':'bool','DateField':'date','DateTimeField':'datetime','JSONField':'JSON',
             'FloatField':'float','DecimalField':'Decimal','VectorField':'Vector'}
    if 'Integer' in field['type'] or field['type'] in ('AutoField','BigAutoField'):
        return 'int'
    return types.get(field['type'], field['type'])


def visibility(name):
    return '#' if name.startswith('_') and not name.startswith('__') else '+'


def wrapped_signature(value):
    if len(value) <= 92:
        return value
    parts = value.split(', ')
    lines = ['']
    for part in parts:
        if lines[-1] and len(lines[-1]) + len(part) > 88:
            lines.append('  ' + part)
        else:
            lines[-1] += (', ' if lines[-1] else '') + part
    return r',\n'.join(lines)


def declaration(key, reference=False, compact=False):
    if key not in classes:
        if key.startswith('django_orm.'):
            title = key.removeprefix('django_orm.')
        else:
            title = framework_names.get(key, key)
        return ['class "' + quoted(title) + '" as ' + alias(key) + ' <<externe>> #F0F0F0']
    cls = classes[key]
    title = cls['name'] + r'\n' + cls['module']
    tag = 'ref' if reference else {'model':'Django model','mixin':'mixin','manager':'manager','dataclass':'dataclass','class':'Python'}[cls['kind']] if cls['kind'] != 'enum' else 'TextChoices'
    keyword = 'enum' if cls['kind'] == 'enum' else 'class'
    color = '#F0F0F0' if reference else '#FFF4DF' if cls['kind'] in ('enum','manager','mixin') else '#EEF7EA' if cls['kind'] == 'dataclass' else '#EAF2FB'
    link = ' [[' + assignment[key] + '.svg]]' if reference or compact else ''
    lines = [keyword + ' "' + quoted(title) + '" as ' + alias(key) + ' <<' + tag + '>>' + link + ' ' + color + ' {']
    if not reference and not compact:
        if cls['kind'] == 'enum':
            lines += ['  ' + value['name'] + ' = ' + quoted(value['value']) for value in cls['values']]
        if cls['orm']:
            declared = {t.id for n in nodes[key].body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
            for field in cls['orm']['fields']:
                inherited = field['name'] not in declared and not field['primary_key']
                suffix = ' [0..1]' if field['null'] else ''
                suffix += ' <<inherited>>' if inherited else ''
                lines.append('  {field} + ' + field['name'] + ' : ' + field_type(field) + suffix)
            for field in cls['orm']['many_to_many']:
                lines.append('  {field} + ' + field['name'] + ' : RelatedManager[' + field['target'] + ']')
            for generic in cls['orm']['generic']:
                lines.append('  {field} + ' + generic['name'] + ' : Model [0..1] <<generic>>')
        for attribute in cls['attributes']:
            suffix = ' : ' + quoted(attribute['type']) if attribute['type'] else ''
            suffix += ' <<property, readOnly>>' if attribute['kind'] == 'property' else ''
            static = '{static} ' if attribute['kind'] == 'class_attribute' else ''
            lines.append('  {field} ' + static + visibility(attribute['name']) + ' ' + attribute['name'] + suffix)
        for manager in cls['managers']:
            lines.append('  {field} {static} + ' + manager['name'] + ' : ' + manager['target'].rsplit('.',1)[-1] + ' <<manager>>')
        if cls['methods']:
            lines.append('  -- Opérations déclarées --')
        for method in cls['methods']:
            static = '{static} ' if set(method['decorators']) & {'staticmethod','classmethod'} else ''
            suffix = ' : ' + quoted(method['return']) if method['return'] else ''
            suffix += ' <<classmethod>>' if 'classmethod' in method['decorators'] else ''
            lines.append('  {method} ' + static + visibility(method['name']) + ' ' + wrapped_signature(method['signature']) + suffix)
    lines.append('}')
    return lines


def relation(edge):
    source, target = alias(edge['source']), alias(edge['target'])
    if edge['kind'] == 'inheritance':
        return target + ' <|-- ' + source
    if edge['kind'] in ('association','many_to_many'):
        label = edge['label']
        if edge.get('through'):
            label += r'\nvia ' + edge['through']
        return source + ' "' + edge['from_multiplicity'] + '" --> "' + edge['to_multiplicity'] + '" ' + target + ' : ' + label
    label = edge['label']
    if edge['kind'] == 'generic':
        label += ' [generic, cible dynamique]'
    return source + ' ..> ' + target + ' : ' + label


def preamble(stem, title):
    return ['@startuml ' + stem, '!include style.iuml', 'left to right direction',
            'title Classes actuelles — ' + title + r'\n' + args.date + ' | Code ' + head[:12],
            'footer Relevé statique du code Python | Attributs et opérations existants | Base réelle non consultée']


legend = ['legend bottom',
          '  + public ; # convention Python non publique ; souligné : staticmethod/classmethod ou attribut de classe.',
          '  Triangle : héritage Python. Flèche pleine : association ORM. Pointillés : dépendance.',
          '  [0..1] : None admis ; <<property, readOnly>> : propriété calculée sans setter déclaré.',
          '  Gris <<ref>> : classe détaillée ailleurs ; <<externe>> : référence framework, corps omis.',
          '  Une GenericForeignKey a une cible dynamique ; elle ne crée pas une FK SQL vers cette cible.',
          'endlegend']
view_coverage = {}
for stem, title, _ in groups:
    full = {k for k,v in assignment.items() if v == stem}
    selected_edges = [e for e in edges if e['source'] in full]
    # Make mixin implementors visible without repeating all ORM associations.
    if stem == '11_heritage_regimes':
        selected_edges += [e for e in edges if e['source'] not in full and e['target'] in full and e['kind'] in ('inheritance','manager','choice')]
    references = {e[k] for e in selected_edges for k in ('source','target')} - full
    lines = preamble(stem,title)
    # Preserve the font size. SVG can zoom; PNG may be large for complex domains.
    for key in sorted(full):
        lines += declaration(key)
    for key in sorted(references):
        lines += declaration(key,reference=True)
    lines += [relation(e) for e in selected_edges]
    if stem == '01_causes_documents':
        lines += ['note bottom of ' + alias('document_manager.models.LibraryNode'),
                  '  Arbre MP_Node : path, depth, numchild hérités.',
                  '  Pas de parent_id dans LibraryNode.',
                  '  content_object se résout par content_type et object_id.', 'end note']
    if stem == '12_classes_services_e01':
        lines += ['note as ServiceNote', '  Les services de concordance, numérotation et protection',
                  '  contiennent aussi des fonctions de module.',
                  '  Elles ne sont pas transformées en classes fictives.', 'end note']
    lines += legend + ['@enduml','']
    (OUT / (stem + '.puml')).write_text('\n'.join(lines))
    view_coverage[stem] = {'title': title, 'classes': sorted(full), 'references': sorted(references)}

# Global class view: actual project model classes only; framework inheritance
# and all declared operations remain available in the separate detailed views.
stem = '00_vue_globale'
full = {k for k,c in classes.items() if c['orm']}
selected_edges = [e for e in edges if e['source'] in full and e['kind'] in ('association','many_to_many')]
references = {e['target'] for e in selected_edges} - full
lines = preamble(stem, str(len(full)) + ' modèles du projet et leurs associations')
lines += ['hide members']
for app in sorted({c['orm']['app'] for c in classes.values() if c['orm']}):
    lines.append('package "' + app + '" {')
    for key in sorted(k for k in full if classes[k]['orm']['app'] == app):
        lines += declaration(key,compact=True)
    lines.append('}')
for key in sorted(references):
    lines += declaration(key,reference=True)
lines += [relation(e) for e in selected_edges]
lines += ['legend bottom',
          '  Vue de navigation des classes Django du projet. Attributs, méthodes et héritage : vues 01–13.',
          '  Associations issues des relations ORM ; cardinalités en objets, pas en tables de jointure.',
          '  Les jointures automatiques ne sont pas des classes métier ajoutées à ce diagramme.',
          '  Aucune classe cible de l’architecture C n’est inventée. Vue SVG conseillée.',
          'endlegend','@enduml','']
(OUT / (stem + '.puml')).write_text('\n'.join(lines))

source_hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources}
source_hashes[metadata_path.relative_to(ROOT).as_posix()] = hashlib.sha256(metadata_path.read_bytes()).hexdigest()
counts = {kind: sum(c['kind'] == kind for c in classes.values()) for kind in sorted({c['kind'] for c in classes.values()})}
data = {'date': args.date, 'source_head': head, 'extraction': 'AST + verified ORM metadata; no application import',
        'source_sha256': source_hashes, 'counts': counts, 'classes_total': len(classes),
        'methods_declared': sum(len(c['methods']) for c in classes.values()),
        'properties_declared': sum(a['kind'] == 'property' for c in classes.values() for a in c['attributes']),
        'classes': [{k:v for k,v in cls.items() if k != 'orm'} | {'detail_view': assignment[key],
                   'orm_fields': cls['orm']['fields'] if cls['orm'] else [],
                   'many_to_many': cls['orm']['many_to_many'] if cls['orm'] else [],
                   'generic': cls['orm']['generic'] if cls['orm'] else []} for key,cls in sorted(classes.items())],
        'relations':edges, 'views':view_coverage}
(OUT / 'inventaire_classes.json').write_text(json.dumps(data,ensure_ascii=False,indent=2) + '\n')
index = ['# Dictionnaire des classes actuelles','',
         'Généré le ' + args.date + ' depuis `' + head + '`. Extraction statique; aucune donnée lue.','',
         'Les modèles, attributs et méthodes sont réels. Les types absents du Python ne sont pas devinés.',
         'Les attributs ORM utilisent des types de valeur abrégés; leurs contraintes complètes restent dans l’ERD.', '',
         '| Classe | Nature | Vue complète | Source |','|---|---|---|---|']
for key,cls in sorted(classes.items()):
    index.append('| `' + key + '` | ' + cls['kind'] + ' | [' + assignment[key] + '](' + assignment[key] + '.svg) | [' + cls['source'] + ':' + str(cls['line']) + '](../../../../' + cls['source'] + '#L' + str(cls['line']) + ') |')
for key,cls in sorted(classes.items()):
    index += ['', '## ' + key, '', 'Bases directes : ' + (', '.join('`' + b + '`' for b in cls['bases']) or 'aucune explicite') + '.', '']
    for method in cls['methods']:
        suffix = ' → `' + method['return'] + '`' if method['return'] else ''
        decorators = ' [' + ', '.join(method['decorators']) + ']' if method['decorators'] else ''
        index.append('- `' + method['signature'] + '`' + suffix + decorators + '.')
    for prop in (a for a in cls['attributes'] if a['kind'] == 'property'):
        index.append('- Propriété `' + prop['name'] + '`' + (' : `' + prop['type'] + '`' if prop['type'] else '') + '.')
    if not cls['methods'] and not any(a['kind'] == 'property' for a in cls['attributes']):
        index.append('Aucune opération ou propriété déclarée directement dans cette classe.')
(OUT / 'DICTIONNAIRE_CLASSES.md').write_text('\n'.join(index) + '\n')
print(json.dumps({'head':head,'classes_total':len(classes),'counts':counts,'methods_declared':data['methods_declared'],
                  'properties_declared':data['properties_declared'],'diagrams':len(groups)+1,
                  'source_hashes_verified':len(metadata['source_sha256']),'application_imports':0,'database_connections':0},ensure_ascii=False,indent=2))
