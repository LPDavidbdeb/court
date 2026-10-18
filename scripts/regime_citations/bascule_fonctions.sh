# Bibliothèque de la bascule du régime des citations.
#
# Sourcée par bascule.sh et essai_bascule.sh ; jamais exécutée seule. Compatible bash 3.2
# (celui de macOS) : ni tableau associatif, ni mapfile.
#
# Chaque contrôle affiche « OK » ou « ÉCHEC » et rend un code non nul en cas d'écart :
# rien ne repose sur une lecture humaine d'un diff. Plan : docs/modele_preuve/BASCULE_REGIME_ETAPE1.md.

# --- I1 : bash exigé --------------------------------------------------------------------
if [ -z "${BASH_VERSION:-}" ]; then
  echo "ÉCHEC   ces commandes exigent bash : lancer « bash scripts/regime_citations/bascule.sh … »" >&2
  return 1 2>/dev/null || exit 1
fi

PG_BIN=${PG_BIN:-/Library/PostgreSQL/18/bin}
BASE_REELLE=court_project_pg

ok ()    { echo "OK      $*"; }
info ()  { echo "        $*"; }
echec () { echo "ÉCHEC   $*" >&2; return 1; }

# --- Identifiants PostgreSQL ------------------------------------------------------------
# Lus dans ~/.court-backup.env sans sourcer le fichier : il porte aussi DB_NAME, qui ne doit
# jamais décider de la cible. Le mot de passe passe par PGPASSWORD et n'est jamais affiché.
charger_identifiants () {
  local f="${BASCULE_IDENTIFIANTS:-$HOME/.court-backup.env}" ligne cle val
  [ -r "$f" ] || { echec "identifiants illisibles : $f"; return 1; }
  PG_HOTE=""; PG_PORT=""; PG_UTILISATEUR=""
  while IFS= read -r ligne || [ -n "$ligne" ]; do
    case "$ligne" in \#*|'') continue ;; esac
    cle=${ligne%%=*}; val=${ligne#*=}
    val=${val%\"}; val=${val#\"}; val=${val%\'}; val=${val#\'}
    case "$cle" in
      DB_HOST) PG_HOTE=$val ;;
      DB_PORT) PG_PORT=$val ;;
      DB_USER) PG_UTILISATEUR=$val ;;
      DB_PASSWORD) PGPASSWORD=$val; export PGPASSWORD ;;
    esac
  done < "$f"
  if [ -z "$PG_HOTE" ] || [ -z "$PG_PORT" ] || [ -z "$PG_UTILISATEUR" ] || [ -z "${PGPASSWORD:-}" ]; then
    echec "identifiants incomplets dans $f"; return 1
  fi
}

# psql : sans ~/.psqlrc, arrêt à la première erreur, sortie brute.
_psql () {
  "$PG_BIN/psql" -X -q -v ON_ERROR_STOP=1 -At -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" "$@"
}

base_existe () {  # $1 base
  [ "$(_psql -d postgres -c "select count(*) from pg_database where datname='$1'")" = "1" ]
}

# --- 4.1 : identité de la cible -----------------------------------------------------------
# base | port du serveur | identifiant système du serveur (pg_control_system) : la même
# requête est posée par psql (ici) et par Django (bascule_fumee.py cible).
identite_base () {
  _psql -d "$1" -c "select current_database()||'|'||inet_server_port()||'|'||system_identifier from pg_control_system()"
}

verifier_cible () {  # $1 base ; compare à CIBLE_PORT et CIBLE_SYSID
  local attendu="$1|$CIBLE_PORT|$CIBLE_SYSID" vu
  vu=$(identite_base "$1") || { echec "connexion impossible à la base $1"; return 1; }
  if [ "$vu" = "$attendu" ]; then ok "cible (psql) : $vu"; else echec "cible (psql) : $vu, attendu $attendu"; fi
}

# --- I4 : connexions ------------------------------------------------------------------------
verifier_connexions () {  # bases… : aucune autre connexion ne doit être ouverte
  local b liste ko=0
  for b in "$@"; do
    liste=$(_psql -d postgres -c "select pid||' '||coalesce(nullif(application_name,''),'-')||' '||coalesce(client_addr::text,'local')||' '||coalesce(state,'-')||' depuis '||to_char(backend_start,'YYYY-MM-DD HH24:MI:SS') from pg_stat_activity where datname='$b' and pid<>pg_backend_pid()") \
      || { echec "pg_stat_activity illisible"; return 1; }
    if [ -n "$liste" ]; then
      echec "connexions ouvertes sur $b :"; echo "$liste" | sed 's/^/          /' >&2; ko=1
    else
      ok "aucune connexion sur $b"
    fi
  done
  if [ "$ko" -ne 0 ]; then
    info "processus clients de PostgreSQL (lsof, port $PG_PORT) :"
    lsof -nP -iTCP:"$PG_PORT" 2>/dev/null | awk 'NR>1 && $0 !~ /LISTEN/ {print "          "$1" pid "$2}' | sort -u >&2
    info "arrêter ces processus à la source, puis reprendre ; pg_terminate_backend seulement en dernier recours"
    return 1
  fi
}

# --- I7 : processus Python d'un arbre du projet --------------------------------------------
processus_projet () {  # liste « pid dossier commande » des processus Python lancés dans un arbre court*
  local p cwd
  for p in $(pgrep -i python 2>/dev/null); do
    cwd=$(lsof -a -p "$p" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p')
    case "$cwd" in
      "$DEPOTS_PREFIXE"*) echo "$p $cwd $(ps -o command= -p "$p" 2>/dev/null | cut -c1-90)" ;;
    esac
  done
}

# --- 4.2 : instantanés de la base -----------------------------------------------------------
colonnes () {  # $1 base -> table<TAB>colonnes préfixées « x. », ordre de déclaration
  _psql -F $'\t' -d "$1" -c "select c.relname, string_agg('x.'||quote_ident(a.attname), ',' order by a.attnum) from pg_attribute a join pg_class c on c.oid=a.attrelid join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind='r' and a.attnum>0 and not a.attisdropped group by c.relname order by c.relname"
}

md5_tables () {  # $1 base, $2 fichier de colonnes -> table|lignes|md5 ; une seule requête, arrêt sur toute erreur
  local sql="" t cols
  while IFS=$'\t' read -r t cols; do
    [ -n "$t" ] || continue
    [ -n "$sql" ] && sql="$sql union all "
    sql="${sql}select '$t', count(*), md5(coalesce(string_agg(row($cols)::text, '|' order by row($cols)::text), '')) from public.\"$t\" x"
  done < "$2"
  [ -n "$sql" ] || { echec "liste de colonnes vide : $2"; return 1; }
  _psql -F '|' -d "$1" -c "select * from ($sql) s order by 1"
}

schema () {  # $1 base -> structure normalisée : colonnes, contraintes, index, séquences, extensions
  _psql -d "$1" -c "
select l from (
  select 'COL|'||c.relname||'|'||a.attname||'|'||format_type(a.atttypid, a.atttypmod)||'|'
         ||case when a.attnotnull then 'NOT NULL' else 'NULL' end
         ||'|défaut='||coalesce(pg_get_expr(d.adbin, d.adrelid), '')||'|identité='||a.attidentity::text as l
    from pg_attribute a join pg_class c on c.oid=a.attrelid join pg_namespace n on n.oid=c.relnamespace
    left join pg_attrdef d on d.adrelid=a.attrelid and d.adnum=a.attnum
   where n.nspname='public' and c.relkind='r' and a.attnum>0 and not a.attisdropped
  union all
  select 'CON|'||c.relname||'|'||co.conname||'|'||co.contype::text||'|'||pg_get_constraintdef(co.oid)
    from pg_constraint co join pg_class c on c.oid=co.conrelid join pg_namespace n on n.oid=c.relnamespace
   where n.nspname='public'
  union all
  select 'IDX|'||tablename||'|'||indexname||'|'||indexdef from pg_indexes where schemaname='public'
  union all
  select 'SEQ|'||sequencename||'|'||data_type||'|'||increment_by||'|'||min_value||'|'||max_value||'|'||cycle
    from pg_sequences where schemaname='public'
  union all
  select 'EXT|'||extname||'|'||extversion from pg_extension
) s order by l"
}

sequences_valeurs () {  # $1 base -> SEQV|séquence|dernière valeur
  _psql -d "$1" -c "select 'SEQV|'||sequencename||'|'||coalesce(last_value::text, '(jamais)') from pg_sequences where schemaname='public' order by 1"
}

migrations_appliquees () {  # $1 base -> MIG|application|migration
  _psql -d "$1" -c "select 'MIG|'||app||'|'||name from django_migrations order by 1"
}

comptes_regime () {  # $1 base -> table|régime|nombre (vide si la colonne n'existe pas)
  local n
  n=$(_psql -d "$1" -c "select count(*) from information_schema.columns where table_schema='public' and table_name in ('email_manager_quote','pdf_manager_quote') and column_name='regime'") || return 1
  [ "$n" = "2" ] || return 0
  _psql -F '|' -d "$1" -c "select 'email_manager_quote', regime, count(*) from email_manager_quote group by regime union all select 'pdf_manager_quote', regime, count(*) from pdf_manager_quote group by regime order by 1, 2"
}

instantane () {  # $1 base, $2 préfixe de sortie, $3 fichier de colonnes de référence (défaut : celles de la base)
  local base=$1 p=$2 cols=${3:-}
  colonnes "$base" > "$p.colonnes" || { echec "colonnes de $base"; return 1; }
  [ -n "$cols" ] || cols="$p.colonnes"
  md5_tables "$base" "$cols" > "$p.md5" || { echec "md5 de $base"; return 1; }
  schema "$base" > "$p.schema" || { echec "schéma de $base"; return 1; }
  sequences_valeurs "$base" > "$p.seqv" || { echec "séquences de $base"; return 1; }
  migrations_appliquees "$base" > "$p.mig" || { echec "migrations de $base"; return 1; }
  ok "instantané de $base ($(wc -l < "$p.md5" | tr -d ' ') tables)"
}

# --- I2 : comparaisons à verdict ------------------------------------------------------------
_ecarts () {  # $1 A, $2 B -> « - ligne » (dans A seulement), « + ligne » (dans B seulement)
  LC_ALL=C comm -23 <(LC_ALL=C sort "$1") <(LC_ALL=C sort "$2") | sed 's/^/- /'
  LC_ALL=C comm -13 <(LC_ALL=C sort "$1") <(LC_ALL=C sort "$2") | sed 's/^/+ /'
}

_rapporter () {  # $1 titre, $2 écarts inattendus
  if [ -z "$2" ]; then ok "$1"; return 0; fi
  echec "$1 — écarts inattendus :"; printf '%s\n' "$2" | sed 's/^/          /' >&2; return 1
}

comparer_identique () {  # $1 préfixe A, $2 préfixe B, [$3 « sans-seqv »] : tout identique
  local f e ko=0
  for f in colonnes md5 schema seqv mig; do
    [ "$f" = seqv ] && [ "${3:-}" = sans-seqv ] && continue
    e=$(_ecarts "$1.$f" "$2.$f")
    _rapporter "$f identique" "$e" || ko=1
  done
  return $ko
}

# Les deux migrations 0009 ont le droit d'ajouter, sur chacune des deux tables de citations, la
# colonne regime (varchar(6), NOT NULL, sans défaut en base), sa contrainte NOT NULL (PostgreSQL 18
# inscrit chaque NOT NULL dans pg_constraint, contype « n », nom <table>_regime_not_null) et ses
# deux index Django (btree et varchar_pattern_ops) ; d'ajouter les deux lignes 0009 dans
# django_migrations ; et d'avancer la séquence de django_migrations. Tout le reste doit être identique.
_TABLES='(email_manager_quote|pdf_manager_quote)'
_COL_OK="^\\+ COL\\|${_TABLES}\\|regime\\|character varying\\(6\\)\\|NOT NULL\\|défaut=\\|identité=$"
_IDX_OK="^\\+ IDX\\|${_TABLES}\\|${_TABLES}_regime_[0-9a-f]{8}(_like)?\\|CREATE INDEX [a-z0-9_]+ ON public\\.${_TABLES} USING btree \\(regime( varchar_pattern_ops)?\\)$"
_CON_OK="^\\+ CON\\|${_TABLES}\\|${_TABLES}_regime_not_null\\|n\\|NOT NULL regime$"
_MIG_OK='^\+ MIG\|(email_manager|pdf_manager)\|0009_quote_regime$'

# Une séquence n'est pas une donnée : elle ne recule jamais, et une migration échouée puis rejouée
# peut en consommer une valeur. Les lignes de django_migrations, elles, sont contrôlées exactement
# par le md5. D'où une avance minimale, non exacte.
_avance_au_moins () {  # $1 écarts, $2 préfixe de ligne, $3 avance minimale : « - x|n » et « + x|m », m ≥ n + min
  local e=$1 nom=$2 d=$3 avant apres
  [ "$(printf '%s\n' "$e" | grep -cF -- "- $nom")" = 1 ] && [ "$(printf '%s\n' "$e" | grep -cF -- "+ $nom")" = 1 ] || return 1
  avant=$(printf '%s\n' "$e" | grep -F -- "- $nom" | awk -F'|' '{print $NF}')
  apres=$(printf '%s\n' "$e" | grep -F -- "+ $nom" | awk -F'|' '{print $NF}')
  [ "$avant" = "(jamais)" ] && avant=0
  [ "$apres" -ge $((avant + d)) ] 2>/dev/null
}

_avance_lignes () {  # md5 : exactement « - table|n|md5 » et « + table|n+d|md5' »
  local e=$1 nom=$2 d=$3 avant apres
  [ "$(printf '%s\n' "$e" | grep -cF -- "- $nom|")" = 1 ] && [ "$(printf '%s\n' "$e" | grep -cF -- "+ $nom|")" = 1 ] || return 1
  avant=$(printf '%s\n' "$e" | grep -F -- "- $nom|" | cut -d'|' -f2)
  apres=$(printf '%s\n' "$e" | grep -F -- "+ $nom|" | cut -d'|' -f2)
  [ "$apres" -eq $((avant + d)) ] 2>/dev/null
}

comparer_apres_migration () {  # $1 préfixe référence (B2), $2 préfixe cible migrée
  local e inattendu ko=0 n_col n_con n_idx
  e=$(_ecarts "$1.schema" "$2.schema")
  inattendu=$(printf '%s\n' "$e" | grep -v '^$' | grep -Ev "$_COL_OK" | grep -Ev "$_CON_OK" | grep -Ev "$_IDX_OK")
  _rapporter "schéma : seules la colonne regime, sa contrainte NOT NULL et ses index" "$inattendu" || ko=1
  n_col=$(printf '%s\n' "$e" | grep -cE "$_COL_OK"); n_con=$(printf '%s\n' "$e" | grep -cE "$_CON_OK")
  n_idx=$(printf '%s\n' "$e" | grep -cE "$_IDX_OK")
  if [ "$n_col" = 2 ] && [ "$n_con" = 2 ] && [ "$n_idx" = 4 ]; then
    ok "schéma : 2 colonnes regime, 2 contraintes NOT NULL et 4 index ajoutés"
  else echec "schéma : attendu 2 colonnes, 2 contraintes, 4 index ; trouvé $n_col, $n_con, $n_idx"; ko=1; fi
  e=$(_ecarts "$1.mig" "$2.mig")
  inattendu=$(printf '%s\n' "$e" | grep -v '^$' | grep -Ev "$_MIG_OK")
  _rapporter "migrations : seules les deux 0009 ajoutées" "$inattendu" || ko=1
  [ "$(printf '%s\n' "$e" | grep -cE "$_MIG_OK")" = 2 ] || { echec "migrations : les deux 0009 ne sont pas présentes"; ko=1; }
  e=$(_ecarts "$1.md5" "$2.md5")
  inattendu=$(printf '%s\n' "$e" | grep -v '^$' | grep -v '^[-+] django_migrations|')
  _rapporter "contenu des tables (colonnes d'origine) : seul django_migrations change" "$inattendu" || ko=1
  if _avance_lignes "$e" django_migrations 2; then ok "django_migrations : +2 lignes"
  else echec "django_migrations : l'écart n'est pas de +2 lignes"; ko=1; fi
  e=$(_ecarts "$1.seqv" "$2.seqv")
  inattendu=$(printf '%s\n' "$e" | grep -v '^$' | grep -v '^[-+] SEQV|django_migrations_id_seq|')
  _rapporter "séquences : seule celle de django_migrations avance" "$inattendu" || ko=1
  if _avance_au_moins "$e" "SEQV|django_migrations_id_seq|" 2; then ok "séquence de django_migrations : avance d'au moins 2"
  else echec "séquence de django_migrations : avance inférieure à 2"; ko=1; fi
  return $ko
}

comparer_apres_r2 () {  # $1 préfixe référence (B2), $2 préfixe après R2, [$3 « reouverte »]
  local e inattendu ko=0
  e=$(_ecarts "$1.schema" "$2.schema");     _rapporter "schéma identique à la référence" "$e" || ko=1
  e=$(_ecarts "$1.mig" "$2.mig");           _rapporter "migrations identiques à la référence" "$e" || ko=1
  e=$(_ecarts "$1.colonnes" "$2.colonnes"); _rapporter "colonnes identiques à la référence" "$e" || ko=1
  if [ "${3:-}" = reouverte ]; then
    info "après réouverture : contenu et séquences non comparés (écritures légitimes possibles)"
    return $ko
  fi
  e=$(_ecarts "$1.md5" "$2.md5"); _rapporter "contenu des tables identique à la référence" "$e" || ko=1
  e=$(_ecarts "$1.seqv" "$2.seqv")
  inattendu=$(printf '%s\n' "$e" | grep -v '^$' | grep -v '^[-+] SEQV|django_migrations_id_seq|')
  _rapporter "séquences : seule celle de django_migrations reste avancée (elle ne recule pas)" "$inattendu" || ko=1
  if [ -n "$e" ] && ! _avance_au_moins "$e" "SEQV|django_migrations_id_seq|" 0; then
    echec "séquence de django_migrations : en recul"; ko=1
  fi
  return $ko
}
