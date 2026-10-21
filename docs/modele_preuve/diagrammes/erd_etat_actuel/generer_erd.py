"""Generate the current ORM ERD without importing real settings or connecting to a database."""
import argparse
import ast
import hashlib
import subprocess
from datetime import date
import inspect
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--date', required=True, help='Date documentaire YYYY-MM-DD')
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
date.fromisoformat(args.date)
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
style_file = Path(__file__).resolve().with_name('style.iuml')
if OUT != style_file.parent:
    (OUT/'style.iuml').write_bytes(style_file.read_bytes())
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
os.environ.clear()
os.environ['PATH'] = '/usr/bin:/bin'

def guard(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        if Path(os.fsdecode(args[0])).name.startswith('.env'):
            raise PermissionError('ERD: environment files forbidden')
    if event == 'import' and args[0].startswith('mysite.settings'):
        raise PermissionError('ERD: production settings forbidden')
    if event in ('socket.connect', 'socket.bind', 'sqlite3.connect'):
        raise PermissionError('ERD: database and network forbidden')
sys.addaudithook(guard)

constants = {}
for node in ast.parse((ROOT/'mysite/settings/base.py').read_text()).body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ('INSTALLED_APPS', 'MIDDLEWARE', 'AUTH_USER_MODEL'):
                constants[target.id] = ast.literal_eval(node.value)
from django.conf import settings
settings.configure(**constants, SECRET_KEY='synthetic-schema-only', DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}}, DEFAULT_AUTO_FIELD='django.db.models.BigAutoField', USE_TZ=True, LANGUAGE_CODE='en-us', LOGGING_CONFIG=None, ACCOUNT_EMAIL_VERIFICATION='none', BASE_DIR=ROOT, ROOT_URLCONF='mysite.urls')
from django.db.backends.base.base import BaseDatabaseWrapper
def no_connection(*args, **kwargs):
    raise PermissionError('ERD: every database connection is forbidden')
BaseDatabaseWrapper.ensure_connection = no_connection
import psycopg2
psycopg2.connect = no_connection
import django
django.setup()
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey

project_apps = sorted(c.label for c in apps.get_app_configs() if Path(c.path).parent == ROOT)
result = []
for m in sorted(apps.get_models(include_auto_created=True), key=lambda m: m._meta.label_lower):
    meta = m._meta
    if meta.proxy:
        continue
    fields = []
    for f in meta.local_fields:
        row = {'name': f.name, 'column': f.column, 'type': f.get_internal_type(), 'null': f.null, 'blank': f.blank, 'primary_key': f.primary_key, 'unique': f.unique, 'db_index': f.db_index}
        for attr in ('max_length', 'max_digits', 'decimal_places', 'dimensions'):
            value = getattr(f, attr, None)
            if value is not None: row[attr] = value
        if f.choices: row['choices'] = [[str(v), str(t)] for v,t in f.flatchoices]
        if f.is_relation:
            row.update(target=f.remote_field.model._meta.label, target_field=f.target_field.name, on_delete=f.remote_field.on_delete.__name__, db_constraint=f.db_constraint, one_to_one=f.one_to_one)
        fields.append(row)
    many = []
    for f in meta.local_many_to_many:
        many.append({'name': f.name, 'target': f.remote_field.model._meta.label, 'through': f.remote_field.through._meta.label, 'through_table': f.remote_field.through._meta.db_table, 'through_auto': bool(f.remote_field.through._meta.auto_created), 'symmetrical': f.remote_field.symmetrical})
    generic = [{'name': f.name, 'content_type_field': f.ct_field, 'object_id_field': f.fk_field, 'for_concrete_model': f.for_concrete_model} for f in meta.private_fields if isinstance(f, GenericForeignKey)]
    constraints = []
    for c in meta.constraints:
        constraints.append({'type': type(c).__name__, 'name': c.name, 'fields': list(getattr(c, 'fields', ())), 'condition': str(getattr(c, 'condition', None)), 'expressions': [str(e) for e in getattr(c, 'expressions', ())]})
    source_owner = meta.auto_created if meta.auto_created else m
    source = Path(inspect.getsourcefile(source_owner))
    result.append({'label': meta.label, 'app': meta.app_label, 'name': meta.object_name, 'table': meta.db_table, 'managed': meta.managed, 'auto_created_for': meta.auto_created._meta.label if meta.auto_created else None, 'project': meta.app_label in project_apps, 'source': str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source), 'fields': fields, 'many_to_many': many, 'generic': generic, 'unique_together': [list(t) for t in meta.unique_together], 'constraints': constraints, 'indexes': [{'name': i.name, 'fields': list(i.fields), 'condition': str(i.condition), 'expressions': [str(e) for e in i.expressions]} for i in meta.indexes]})

from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState
from django.db.migrations.autodetector import MigrationAutodetector
loader = MigrationLoader(None, ignore_no_migrations=True)
changes = MigrationAutodetector(loader.project_state(), ProjectState.from_apps(apps)).changes(graph=loader.graph)
data = {'django_version': django.get_version(), 'project_apps': project_apps, 'models': result, 'migration_drift': {label: [{'name': m.name, 'operations': [type(op).__name__ for op in m.operations]} for m in ms] for label,ms in changes.items()}, 'migration_leaves': [list(t) for t in loader.graph.leaf_nodes()]}

# The following outputs contain schema metadata only, never object values.
data['date'] = args.date
data['source_head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
sources = sorted({m['source'] for m in result if m['project']})
data['source_sha256'] = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
by_label = {m['label']: m for m in result}
project_models = [m for m in result if m['project'] and not m['auto_created_for']]
technical_models = [m for m in result if not m['project'] and not m['auto_created_for']]
joins = [m for m in result if m['auto_created_for']]
assert len({m['table'] for m in result}) == len(result), 'Duplicate SQL table representation'

# Each real table has exactly one full detail view. References to other views
# are rendered as grey PK-only entities, without inventing additional tables.
groups = [
    ('01_causes_documents', 'Causes, documents et structure', [
        'cause_manager.Cause', 'cause_manager.EtatCause', 'cause_manager.LienCause',
        'document_manager.Document', 'document_manager.Statement', 'document_manager.LibraryNode',
        'document_manager.SchemaNiveaux', 'document_manager.Niveau']),
    ('02_historique_e01', 'Référent, captures et concordance E01', [
        'document_manager.ReferentHistorique', 'document_manager.InstantaneReferent',
        'document_manager.InstantaneNoeud', 'document_manager.VersionTexte',
        'document_manager.Correspondance', 'document_manager.ExtremiteCorrespondance',
        'document_manager.NoeudArchive']),
    ('03_bordereau_appuis', 'Bordereau de juillet, appuis et citations', [
        'case_manager.BordereauDepotJuillet', 'case_manager.AppuiDepotJuillet',
        'case_manager.ConfirmationAppui', 'case_manager.AncrageCitation']),
    ('04_argumentation', 'Ancien pont : argumentation', [m['label'] for m in project_models if m['app'] == 'argument_manager']),
    ('05_dossiers_transmissions', 'Dossiers historiques et transmissions existantes', [
        'case_manager.LegalCase', 'case_manager.ExhibitRegistry', 'case_manager.PerjuryContestation',
        'case_manager.AISuggestion', 'case_manager.ProducedExhibit', 'case_manager.DestinataireInstance',
        'case_manager.Transmission', 'case_manager.FichierTransmis']),
    ('06_courriels_pdf_protagonistes', 'Courriels, PDF et protagonistes', [m['label'] for m in project_models if m['app'] in ('email_manager', 'pdf_manager', 'protagonist_manager')]),
    ('07_photos_evenements', 'Photographies et événements', [m['label'] for m in project_models if m['app'] in ('photos', 'events')]),
    ('08_google_chat', 'Google Chat', [m['label'] for m in project_models if m['app'] == 'googlechat_manager']),
    ('09_utilisateurs_ia', 'Utilisateur personnalisé et réponses IA', ['users.CustomUser', 'ai_services.GeminiResponse']),
    ('10_tables_techniques', 'Django, allauth et miniatures', [m['label'] for m in technical_models]),
]
assignment = {}
for stem, title, labels in groups:
    for label in labels:
        assert label not in assignment, label
        assignment[label] = stem
for m in joins:
    assignment[m['label']] = assignment[m['auto_created_for']]
assert set(assignment) == set(by_label), 'A registered table has no detail view'
for m in result:
    m['detail_view'] = assignment[m['label']]

def alias(label):
    return 'E_' + label.replace('.', '_')

def quoted(value):
    return str(value).replace('"', "'").replace('\n', ' ')

def color(m, reference=False):
    if reference:
        return '#F0F0F0'
    if m['auto_created_for']:
        return '#FFF4E0'
    if not m['project']:
        return '#F3F3F3'
    if m['app'] in ('document_manager', 'cause_manager'):
        return '#EAF2FB'
    if m['app'] in ('case_manager', 'argument_manager'):
        return '#F0EAF8'
    return '#EEF7EA'

def datatype(f):
    names = {'CharField': 'Char', 'TextField': 'Text', 'DateField': 'Date', 'DateTimeField': 'DateTime',
             'BooleanField': 'Bool', 'JSONField': 'JSON', 'ForeignKey': 'FK', 'OneToOneField': 'FK',
             'BigAutoField': 'BigAuto', 'AutoField': 'Auto', 'IntegerField': 'Integer',
             'BigIntegerField': 'BigInteger', 'PositiveIntegerField': 'PositiveInteger',
             'PositiveBigIntegerField': 'PositiveBigInteger', 'PositiveSmallIntegerField': 'PositiveSmallInteger',
             'FloatField': 'Float', 'FileField': 'File', 'VectorField': 'Vector'}
    t = names.get(f['type'], f['type'])
    if f['type'] in ('CharField', 'FileField') and f.get('max_length'):
        t += '(' + str(f['max_length']) + ')'
    if f.get('dimensions'):
        t += '(' + str(f['dimensions']) + ')'
    return t

def entity(m, reference=False, compact=False):
    if compact:
        title = m['name']
    elif m['auto_created_for']:
        title = 'M2M ' + m['name'] + r'\n' + m['table']
    else:
        title = m['name'] + r'\n' + m['table']
    tag = ' <<ref>>' if reference else (' <<M2M auto>>' if m['auto_created_for'] else '')
    lines = ['entity "' + quoted(title) + '" as ' + alias(m['label']) + tag + ' ' + color(m, reference) + ' {']
    if not compact:
        fields = [f for f in m['fields'] if f['primary_key']] if reference else m['fields']
        for f in fields:
            tags = ['PK'] if f['primary_key'] else []
            if 'target' in f: tags.append('FK')
            if f['unique'] and not f['primary_key']: tags.append('UQ')
            label = ('* ' if not f['null'] else '  ') + f['column'] + ' : ' + datatype(f)
            if f['null']: label += ' ?'
            if tags: label += ' <<' + ','.join(tags) + '>>'
            lines.append('  {field} ' + label)
        if not reference:
            compound = list(m['unique_together'])
            compound += [c['fields'] for c in m['constraints'] if c['type'] == 'UniqueConstraint' and c['fields'] and c['condition'] == 'None']
            if compound:
                lines.append('  .. Unicité composée ..')
                lines += ['  {field} UQ (' + ', '.join(v) + ')' for v in compound]
            for c in m['constraints']:
                if c['type'] != 'UniqueConstraint' or c['condition'] != 'None' or c['expressions']:
                    lines.append('  {field} ' + ('CHECK ' if c['type'] == 'CheckConstraint' else 'UQ conditionnelle ') + c['name'])
            if m['generic']:
                lines.append('  .. Référence générique sans FK objet ..')
                for g in m['generic']:
                    lines.append('  {field} ' + g['name'] + ' = GFK(' + g['content_type_field'] + ', ' + g['object_id_field'] + ')')
    lines.append('}')
    return lines

def relation(m, f, compact=False):
    left = '|o' if f['null'] else '||'
    right = 'o|' if f['unique'] else 'o{'
    line = '--' if f['db_constraint'] else '..'
    caption = f['name'] if compact else f['column'] + ' / ' + f['on_delete']
    return alias(f['target']) + ' ' + left + line + right + ' ' + alias(m['label']) + ' : ' + caption

def preamble(stem, title):
    return ['@startuml ' + stem, '!include style.iuml', 'left to right direction',
            'title ERD actuel — ' + title + r'\nCode ' + data['source_head'][:12] + ' — ' + args.date,
            'footer Schéma ORM déclaré, sans lecture de la base réelle | Types Django, pas un DDL PostgreSQL']

legend = [
    'legend bottom',
    '  * champ NOT NULL   ? NULL autorisé   PK clé primaire   FK clé étrangère   UQ unicité',
    '  || un   |o zéro ou un   o{ zéro à plusieurs. La cardinalité inverse minimale reste zéro.',
    '  Gris <<ref>> : table détaillée dans une autre vue. Ocre : jointure M2M automatique.',
    '  / CASCADE, PROTECT, SET_NULL, DO_NOTHING : politique Django on_delete, pas un relevé SQL.',
    '  GFK et identifiants historiques scalaires ne créent pas de FK SQL vers l’objet désigné.',
    'endlegend',
]

view_coverage = {}
for stem, title, labels in groups:
    full = {label for label, view in assignment.items() if view == stem}
    references = {f['target'] for label in full for f in by_label[label]['fields'] if 'target' in f} - full
    lines = preamble(stem, title)
    lines += ['scale max 3800*3600']
    for label in sorted(full): lines += entity(by_label[label])
    for label in sorted(references): lines += entity(by_label[label], reference=True)
    for label in sorted(full):
        for f in by_label[label]['fields']:
            if 'target' in f: lines.append(relation(by_label[label], f))
    lines += legend + ['@enduml', '']
    (OUT/(stem+'.puml')).write_text('\n'.join(lines))
    view_coverage[stem] = {'title': title, 'tables': sorted(full), 'references': sorted(references)}

# Global logical ERD: automatic join entities are collapsed to M:N links.
# The explicitly defined Event/Photo join is retained as a normal entity.
stem = '00_vue_globale'
lines = preamble(stem, 'vue globale logique, ' + str(len(project_models)+len(technical_models)) + ' modèles hors jointures automatiques')
lines += ['scale max 3800*3000', 'hide members']
primary = [m for m in result if not m['auto_created_for']]
for app in sorted({m['app'] for m in primary}):
    lines.append('package "' + app + '" {')
    for m in primary:
        if m['app'] == app: lines += entity(m, compact=True)
    lines.append('}')
for m in primary:
    for f in m['fields']:
        if 'target' in f: lines.append(relation(m, f, compact=True))
    for f in m['many_to_many']:
        if f['through_auto']:
            lines.append(alias(m['label']) + ' }o..o{ ' + alias(f['target']) + ' : ' + f['name'] + ' [M2M]')
lines += ['legend bottom',
          '  Vue globale : modèles métier et techniques réellement enregistrés.',
          '  Traits pleins : FK / OneToOne déclarés. Pointillés M2M : jointures automatiques repliées.',
          '  Les ' + str(len(joins)) + ' jointures automatiques et tous les champs figurent dans les dix vues détaillées.',
          '  Les GFK n’imposent pas une FK SQL sur object_id. Voir le dictionnaire pour leurs propriétaires.',
          '  SVG conseillé pour zoomer. Aucune entité future de l’architecture C n’est ajoutée.',
          'endlegend', '@enduml', '']
(OUT/(stem+'.puml')).write_text('\n'.join(lines))
data['views'] = view_coverage
data['counts'] = {'project_models': len(project_models), 'technical_models': len(technical_models),
                  'automatic_join_tables': len(joins), 'tables_total': len(result),
                  'columns': sum(len(m['fields']) for m in result),
                  'foreign_keys_including_one_to_one': sum('target' in f for m in result for f in m['fields']),
                  'many_to_many_fields': sum(len(m['many_to_many']) for m in result),
                  'generic_foreign_keys': sum(len(m['generic']) for m in result)}
(OUT/'schema_modeles.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

# Human-readable dictionary, exhaustive for the registered concrete tables.
dictionary = ['# Dictionnaire des tables et champs actuels', '',
              'Généré le ' + args.date + ' depuis le code `' + data['source_head'] + '`.', '',
              '**Métadonnées Django uniquement. Aucune donnée ni structure de la base réelle n’a été lue.**', '',
              'Les types sont ceux du modèle ORM. Les noms de colonnes et de tables sont déclarés par Django.', '',
              '## Index des tables', '', '| Modèle | Table déclarée | Vue détaillée |', '|---|---|---|']
for m in result:
    dictionary.append('| `' + m['label'] + '` | `' + m['table'] + '` | [' + m['detail_view'] + '](' + m['detail_view'] + '.svg) |')
dictionary += ['', '## Champs, relations et contraintes', '']
for m in result:
    dictionary += ['### ' + m['label'], '', 'Table : `' + m['table'] + '`. Source : `' + m['source'] + '`.', '']
    if m['auto_created_for']: dictionary += ['Jointure automatique de `' + m['auto_created_for'] + '`.', '']
    dictionary += ['| Colonne | Type ORM | NULL | Clé / référence |', '|---|---|---|---|']
    for f in m['fields']:
        flags = ['PK'] if f['primary_key'] else []
        if f['unique'] and not f['primary_key']: flags.append('UNIQUE')
        if 'target' in f: flags.append('FK → ' + f['target'] + '.' + f['target_field'] + ' / ' + f['on_delete'] + (' / db_constraint=False' if not f['db_constraint'] else ''))
        dictionary.append('| `' + f['column'] + '` | ' + datatype(f) + ' | ' + ('oui' if f['null'] else 'non') + ' | ' + '; '.join(flags) + ' |')
    dictionary.append('')
    for f in m['many_to_many']:
        dictionary += ['- M2M `' + f['name'] + '` → `' + f['target'] + '` via `' + f['through_table'] + '`.', '']
    for g in m['generic']:
        dictionary += ['- GFK `' + g['name'] + '` = (`' + g['content_type_field'] + '`, `' + g['object_id_field'] + '`). **Pas de FK SQL vers l’objet.**', '']
    for unique in m['unique_together']: dictionary += ['- Unicité composée : `' + ', '.join(unique) + '`.', '']
    for c in m['constraints']:
        dictionary += ['- `' + c['type'] + ' ' + c['name'] + '` : champs `' + ', '.join(c['fields']) + '`, condition `' + c['condition'].replace('|', '\\|') + '`, expressions `' + ', '.join(c['expressions']).replace('|', '\\|') + '`.', '']
    for index in m['indexes']:
        dictionary += ['- Index `' + index['name'] + '` : `' + ', '.join(index['fields']) + '`.', '']
(OUT/'DICTIONNAIRE_MODELES.md').write_text('\n'.join(dictionary))

assert not data['migration_drift'], 'Models/migrations differ: inspect schema_modeles.json; no migrations were written'
print(json.dumps({'head': data['source_head'], 'counts': data['counts'], 'detail_views': len(groups), 'migration_drift': data['migration_drift'], 'database_connections': 0}, ensure_ascii=False, indent=2))
