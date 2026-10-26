"""Standalone synthetic test launcher: never imports the project's settings."""
import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / 'repo'
phase = sys.argv.pop(1) if len(sys.argv) > 1 else 'baseline'
if not phase.replace('-', '').replace('_', '').isalnum():
    raise RuntimeError('Invalid run name')
log = (ROOT / 'logs' / (phase + '.log')).open('w', encoding='utf-8')
class Tee:
    def __init__(self, original): self.original = original
    def write(self, value):
        log.write(value); log.flush(); return self.original.write(value)
    def flush(self): log.flush(); self.original.flush()
    def isatty(self): return False
sys.stdout = Tee(sys.stdout)
sys.stderr = Tee(sys.stderr)
os.environ.clear()
os.environ.update({'PATH': '/usr/bin:/bin:/Library/PostgreSQL/18/bin', 'DJANGO_SETTINGS_MODULE': 'c0a_settings', 'PYTHONPATH': str(ROOT / 'harness') + ':' + str(REPO), 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(ROOT / 'tmp')})
sys.dont_write_bytecode = True
(ROOT / 'tmp').mkdir(exist_ok=True)
os.chdir(REPO)
sys.path[:0] = [str(ROOT / 'harness'), str(REPO)]

def isolation(event, args):
    if event == 'open':
        path = args[0]
        if isinstance(path, (str, bytes, os.PathLike)) and Path(os.fsdecode(path)).name.startswith('.env'):
            raise PermissionError('C0-A: environment files are forbidden')
    if event == 'import' and args[0] in {'mysite.settings', 'mysite.settings.base', 'mysite.settings.local', 'mysite.settings.remote'}:
        raise PermissionError('C0-A: real project settings are forbidden')
    if event in {'socket.connect', 'socket.bind'}:
        address = args[1]
        if not isinstance(address, str) or not address.startswith(str(ROOT / 'socket') + '/'):
            raise PermissionError('C0-A: external network disabled')
sys.addaudithook(isolation)
import psycopg2
from psycopg2.extensions import parse_dsn
original_connect = psycopg2.connect

def only_private_cluster(dsn=None, *args, **kwargs):
    params = parse_dsn(dsn) if dsn else {}
    params.update(kwargs)
    if not (params.get('host') == str(ROOT / 'socket') and str(params.get('port')) == '55439' and params.get('user') == 'c0a_runner' and params.get('dbname') in {'court_c0a', 'test_court_c0a', 'postgres'}):
        raise PermissionError('C0-A: connection outside the disposable cluster refused before libpq')
    return original_connect(dsn, *args, **kwargs) if dsn is not None else original_connect(*args, **kwargs)
psycopg2.connect = only_private_cluster
try:
    psycopg2.connect(host='/tmp', port='5432', user='c0a_runner', dbname='court_project_pg')
except PermissionError:
    print('ISOLATION: external PostgreSQL probe rejected before libpq; no .env; no TCP.', flush=True)
else:
    raise RuntimeError('C0-A isolation probe failed')
import django
django.setup()
from django.conf import settings
assert settings.DATABASES['default']['HOST'] == str(ROOT / 'socket')
assert settings.DATABASES['default']['NAME'] == 'court_c0a'
from django.core.management import call_command
labels = sys.argv[1:] or ['document_manager.test_e01_numerotation', 'case_manager.test_e01_cotes_concordance', 'core.test_regime_citations', 'argument_manager.test_affidavit_ordre']
if labels == ['C0A_SCHEMA_CHECK']:
    call_command('makemigrations', check=True, dry_run=True, verbosity=1)
    call_command('check')
    sys.exit(0)
if any(label.startswith('-') for label in labels):
    raise RuntimeError('Only explicit test labels are accepted')
print('C0-A test settings:', settings.SETTINGS_MODULE, 'private socket:', settings.DATABASES['default']['HOST'], 'labels:', labels, flush=True)
call_command('test', *labels, verbosity=2, interactive=False, keepdb=True)
