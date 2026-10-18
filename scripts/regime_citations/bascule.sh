#!/usr/bin/env bash
# Bascule de l'étape 1 du régime des citations — pilote.
#
#   bash scripts/regime_citations/bascule.sh ouvrir --nature essai|reelle --base B --arbre A \
#        --branche BR --vers REF [--dossier D] [--port-serveur 8000]
#   bash scripts/regime_citations/bascule.sh <étape> --etat <dossier>/etat.env [options]
#
# Étapes : b1 b2 b3 b4 b5 b6 b7 | r1 r2 r3 | reparer-git | etat
#
# Chaque étape vérifie ses préconditions, journalise sa sortie (sans aucun secret), enregistre
# l'étape atteinte dans etat.env, et rend 0 si tout est conforme, 1 sinon. La cible (base, arbre,
# branche, serveur PostgreSQL) est fixée une fois par « ouvrir » et revérifiée avant chaque
# opération critique. Pour la base réelle, chaque commande exige BASCULE_REELLE_CONFIRMEE=oui.
# Plan : docs/modele_preuve/BASCULE_REGIME_ETAPE1.md.

if [ -z "${BASH_VERSION:-}" ]; then
  echo "ÉCHEC   ce pilote exige bash : « bash scripts/regime_citations/bascule.sh … »" >&2
  exit 1
fi
set -uo pipefail

OUTIL_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
. "$OUTIL_DIR/bascule_fonctions.sh" || exit 1

# --- Constantes du chantier ----------------------------------------------------------------------
REFERENCE_VALIDEE=4b53e831144c0d042b397d809f89321e23d557cd   # merge validé sur le clone (§ 10.4)
CHEMINS_PERMIS_APRES_REFERENCE='^(docs/|scripts/regime_citations/)'
DEPOTS_PREFIXE=/Users/Louis-Philippe/Documents/GitHub/court
ARBRE_REEL=/Users/Louis-Philippe/Documents/GitHub/court
BRANCHE_REELLE=epic/E01-numerotation-concordance
PYTHON_DEFAUT=/Users/Louis-Philippe/Documents/GitHub/court/.venv/bin/python
SAUV_DEFAUT=$HOME/Backups/court/regime_etape1
LANG_SERVEUR=en_CA.UTF-8            # celui du serveur 8000 (relevé le 2026-10-18)
BASCULE_LOCK_TIMEOUT=${BASCULE_LOCK_TIMEOUT:-10s}

arret () { [ -n "${1:-}" ] && echec "$1"; exit 1; }

# --- État ------------------------------------------------------------------------------------------
etat_lire () {
  [ -n "${ETAT:-}" ] && [ -r "$ETAT" ] || arret "état illisible (--etat <dossier>/etat.env)"
  # shellcheck disable=SC1090
  . "$ETAT"
  if [ "$CIBLE_NATURE" = reelle ] && [ "${BASCULE_REELLE_CONFIRMEE:-}" != oui ]; then
    arret "cible réelle : exporter BASCULE_REELLE_CONFIRMEE=oui pour chaque commande"
  fi
  JOURNAL="$DOSSIER/journal.log"
}

etat_ecrire () {  # clé valeur
  local tmp="$ETAT.tmp"
  grep -v "^$1=" "$ETAT" > "$tmp" || true
  printf '%s=%q\n' "$1" "$2" >> "$tmp"
  mv "$tmp" "$ETAT"
  eval "$1=\$2"
}

exiger_etape () {  # étapes acceptées…
  local e
  for e in "$@"; do [ "$ETAPE" = "$e" ] && return 0; done
  arret "étape atteinte : $ETAPE ; cette commande exige : $*"
}

# --- Django : environnement propre et explicite ---------------------------------------------------
_django () {
  ( cd "$CIBLE_ARBRE" && env -i HOME="$HOME" USER="${USER:-}" PATH="/usr/bin:/bin:/usr/sbin:/sbin" \
      LANG="$LANG_SERVEUR" DJANGO_SETTINGS_MODULE=settings_bascule PYTHONPATH="$OUTIL_DIR" \
      BASCULE_BASE="$CIBLE_BASE" BASCULE_PORT="$CIBLE_PORT" BASCULE_SYSID="$CIBLE_SYSID" \
      BASCULE_REELLE_CONFIRMEE="${BASCULE_REELLE_CONFIRMEE:-non}" \
      PGOPTIONS="-c lock_timeout=$BASCULE_LOCK_TIMEOUT" \
      "$PYTHON" "$@" )
}

git_tete () { git -C "$CIBLE_ARBRE" rev-parse HEAD; }
git_propre () { [ -z "$(git -C "$CIBLE_ARBRE" status --porcelain)" ]; }

regime_en_base () {  # nombre de migrations 0009 appliquées | nombre de colonnes regime
  _psql -d "$CIBLE_BASE" -c "select (select count(*) from django_migrations where app in ('email_manager','pdf_manager') and name='0009_quote_regime')||'|'||(select count(*) from information_schema.columns where table_schema='public' and table_name in ('email_manager_quote','pdf_manager_quote') and column_name='regime')"
}

# --- ouvrir ------------------------------------------------------------------------------------------
e_ouvrir () {
  local nature="" base="" arbre="" branche="" vers="" port_serveur="" python="$PYTHON_DEFAUT"
  while [ $# -gt 0 ]; do
    case "$1" in
      --nature) nature=$2; shift 2 ;;  --base) base=$2; shift 2 ;;  --arbre) arbre=$2; shift 2 ;;
      --branche) branche=$2; shift 2 ;; --vers) vers=$2; shift 2 ;; --port-serveur) port_serveur=$2; shift 2 ;;
      --python) python=$2; shift 2 ;;  --dossier) shift 2 ;;
      *) arret "option inconnue : $1" ;;
    esac
  done
  [ -n "$nature" ] && [ -n "$base" ] && [ -n "$arbre" ] && [ -n "$branche" ] && [ -n "$vers" ] \
    || arret "ouvrir exige --nature --base --arbre --branche --vers"
  arbre=$(cd "$arbre" && pwd) || arret "arbre introuvable"
  case "$nature" in
    reelle)
      [ "${BASCULE_REELLE_CONFIRMEE:-}" = oui ] || arret "cible réelle : BASCULE_REELLE_CONFIRMEE=oui requis"
      [ "$base" = "$BASE_REELLE" ] && [ "$arbre" = "$ARBRE_REEL" ] && [ "$branche" = "$BRANCHE_REELLE" ] \
        || arret "cible réelle : base, arbre et branche doivent être $BASE_REELLE, $ARBRE_REEL, $BRANCHE_REELLE"
      [ -n "$port_serveur" ] || port_serveur=8000 ;;
    essai)
      case "$base" in bascule_essai_*) ;; *) arret "base d'essai : le nom doit commencer par bascule_essai_" ;; esac
      [ "$arbre" != "$ARBRE_REEL" ] && [ "$branche" != "$BRANCHE_REELLE" ] || arret "essai : ni l'arbre ni la branche réels" ;;
    *) arret "--nature essai|reelle" ;;
  esac
  charger_identifiants || arret
  [ "$(git -C "$arbre" rev-parse --abbrev-ref HEAD)" = "$branche" ] || arret "l'arbre $arbre n'est pas sur $branche"
  local avant apres
  avant=$(git -C "$arbre" rev-parse HEAD) || arret
  apres=$(git -C "$arbre" rev-parse --verify "$vers^{commit}") || arret "cible Git introuvable : $vers"
  git -C "$arbre" merge-base --is-ancestor "$avant" "$apres" || arret "avance rapide impossible : $avant n'est pas ancêtre de $apres"
  git -C "$arbre" merge-base --is-ancestor "$REFERENCE_VALIDEE" "$apres" || arret "la cible ne contient pas la référence validée $REFERENCE_VALIDEE"
  local hors
  hors=$(git -C "$arbre" diff --name-only "$REFERENCE_VALIDEE" "$apres" | grep -Ev "$CHEMINS_PERMIS_APRES_REFERENCE" || true)
  [ -z "$hors" ] || arret "la cible modifie, depuis la référence validée, des fichiers hors docs/ et scripts/regime_citations/ : $hors"
  ok "Git : $avant → $apres (avance rapide ; depuis $REFERENCE_VALIDEE, seulement docs/ et scripts/regime_citations/)"
  local identite
  identite=$(identite_base "$base") || arret "base $base injoignable"
  ok "cible : $identite"
  cat > "$ETAT" <<EOF
BASCULE_H=$BASCULE_H
CIBLE_NATURE=$nature
CIBLE_BASE=$base
CIBLE_HOTE=$PG_HOTE
CIBLE_PORT=$(printf '%s' "$identite" | cut -d'|' -f2)
CIBLE_SYSID=$(printf '%s' "$identite" | cut -d'|' -f3)
CIBLE_ARBRE=$arbre
CIBLE_BRANCHE=$branche
AVANT_SHA=$avant
APRES_SHA=$apres
APRES_REF=$vers
SERVEUR_PORT=$port_serveur
PYTHON=$python
DOSSIER=$DOSSIER
DUMP=$DOSSIER/avant_bascule.dump
REF_BASE=${base}_ref_${BASCULE_H//-/_}
ECHEC_BASE=${base}_echec_${BASCULE_H//-/_}
ETAPE=ouvert
REOUVERT=non
EOF
  ok "état : $ETAT"
}

# --- B1 : écritures immobilisées --------------------------------------------------------------------
e_b1 () {
  local pause=non
  [ "${1:-}" = --sessions-en-pause ] && pause=oui
  etat_lire; exiger_etape ouvert b1; charger_identifiants || arret
  verifier_cible "$CIBLE_BASE" || arret
  local procs
  procs=$(processus_projet)
  if [ "$CIBLE_NATURE" = reelle ]; then
    if lsof -nP -iTCP:"$SERVEUR_PORT" -sTCP:LISTEN >/dev/null 2>&1; then arret "le serveur écoute encore sur $SERVEUR_PORT"; fi
    ok "aucun serveur sur le port $SERVEUR_PORT"
    [ -z "$procs" ] || { echec "processus Python encore actifs dans un arbre du projet :"; echo "$procs" | sed 's/^/          /' >&2; exit 1; }
    ok "aucun processus Python dans un arbre du projet (court*)"
    [ "$pause" = oui ] || arret "confirmer la pause des sessions Claude et de tout script : --sessions-en-pause"
    info "sessions Claude Code ouvertes (à tenir en pause) : $(pgrep -f claude-code 2>/dev/null | wc -l | tr -d ' ')"
  else
    info "essai : processus Python des arbres du projet (non bloquant) :"
    [ -n "$procs" ] && echo "$procs" | sed 's/^/          /' || info "  aucun"
  fi
  verifier_connexions "$CIBLE_BASE" || arret
  etat_ecrire ETAPE b1
}

# --- B2 : sauvegarde, restauration prouvée -----------------------------------------------------------
e_b2 () {
  etat_lire; exiger_etape b1; charger_identifiants || arret
  verifier_cible "$CIBLE_BASE" || arret
  verifier_connexions "$CIBLE_BASE" || arret
  base_existe "$REF_BASE" && arret "la base de référence $REF_BASE existe déjà"
  [ -e "$DUMP" ] && arret "la sauvegarde $DUMP existe déjà"
  "$PG_BIN/pg_dump" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -Fc -f "$DUMP" "$CIBLE_BASE" || arret "pg_dump"
  local nom_dump
  nom_dump=$("$PG_BIN/pg_restore" -l "$DUMP" | sed -n 's/^;[[:space:]]*dbname: //p') || arret "pg_restore -l"
  [ "$nom_dump" = "$CIBLE_BASE" ] || arret "la sauvegarde porte la base « $nom_dump », attendu $CIBLE_BASE"
  ok "sauvegarde : $DUMP (base $nom_dump, $(du -h "$DUMP" | cut -f1 | tr -d ' '))"
  etat_ecrire DUMP_SHA256 "$(shasum -a 256 "$DUMP" | cut -d' ' -f1)"
  "$PG_BIN/createdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" "$REF_BASE" || arret "createdb $REF_BASE"
  "$PG_BIN/pg_restore" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -d "$REF_BASE" --no-owner --exit-on-error "$DUMP" \
    || arret "restauration dans $REF_BASE"
  verifier_cible "$REF_BASE" || arret
  verifier_connexions "$CIBLE_BASE" || arret
  instantane "$REF_BASE" "$DOSSIER/ref" || arret
  instantane "$CIBLE_BASE" "$DOSSIER/b2_cible" "$DOSSIER/ref.colonnes" || arret
  comparer_identique "$DOSSIER/ref" "$DOSSIER/b2_cible" || arret "la restauration ne reproduit pas la base"
  etat_ecrire COMPTE_COURRIEL "$(grep '^email_manager_quote|' "$DOSSIER/ref.md5" | cut -d'|' -f2)"
  etat_ecrire COMPTE_PDF "$(grep '^pdf_manager_quote|' "$DOSSIER/ref.md5" | cut -d'|' -f2)"
  ok "citations à la sauvegarde : $COMPTE_COURRIEL + $COMPTE_PDF"
  etat_ecrire ETAPE b2
}

# --- B3 : avance rapide ------------------------------------------------------------------------------
e_b3 () {
  etat_lire; exiger_etape b2
  [ "$(git -C "$CIBLE_ARBRE" rev-parse --abbrev-ref HEAD)" = "$CIBLE_BRANCHE" ] || arret "l'arbre n'est pas sur $CIBLE_BRANCHE"
  [ "$(git_tete)" = "$AVANT_SHA" ] || arret "HEAD $(git_tete) ≠ $AVANT_SHA : la branche a bougé depuis « ouvrir »"
  git_propre || arret "arbre non propre (diagnostic : etat ; réparation : reparer-git)"
  git -C "$CIBLE_ARBRE" merge --ff-only "$APRES_SHA" || arret "avance rapide refusée"
  [ "$(git_tete)" = "$APRES_SHA" ] && git_propre || arret "après l'avance rapide : HEAD ou arbre inattendus"
  ok "arbre à $APRES_SHA, propre"
  etat_ecrire ETAPE b3
}

# --- B4 : contrôles avant migration --------------------------------------------------------------------
e_b4 () {
  etat_lire; exiger_etape b3; charger_identifiants || arret
  [ "$(git_tete)" = "$APRES_SHA" ] && git_propre || arret "l'arbre n'est pas au nouveau code propre"
  verifier_cible "$CIBLE_BASE" || arret
  _django "$OUTIL_DIR/bascule_fumee.py" cible || arret "identité de la cible vue par Django"
  _django manage.py check || arret "manage.py check"
  local plan attendu
  plan=$(_django manage.py migrate --plan) || arret "migrate --plan"
  plan=$(printf '%s\n' "$plan" | grep -E '^[a-z_]+\.[0-9]{4}_[a-z0-9_]+$' | LC_ALL=C sort)
  attendu=$(printf '%s\n' email_manager.0009_quote_regime pdf_manager.0009_quote_regime)
  [ "$plan" = "$attendu" ] || arret "plan de migration inattendu : $(echo $plan)"
  ok "plan de migration : exactement les deux 0009_quote_regime"
  _django manage.py makemigrations --check --dry-run || arret "makemigrations --check"
  ok "modèles et migrations concordent"
  etat_ecrire ETAPE b4
}

diagnostic_migration () {
  local r; r=$(regime_en_base) || { info "état de la base illisible"; return; }
  case "${r%%|*}" in
    0) info "aucune 0009 appliquée : R1 (base intacte)" ;;
    *) info "$(printf '%s' "${r%%|*}") migration(s) 0009 appliquée(s) : R2, puis R1" ;;
  esac
}

# --- B5 : migrations ------------------------------------------------------------------------------------
e_b5 () {
  local seulement="" verif=oui
  while [ $# -gt 0 ]; do
    case "$1" in
      --seulement) seulement=$2; shift 2 ;;
      --sans-verif-connexions) verif=non; shift ;;
      *) arret "option inconnue : $1" ;;
    esac
  done
  etat_lire; exiger_etape b4; charger_identifiants || arret
  if [ -n "$seulement" ] || [ "$verif" = non ]; then
    [ "$CIBLE_NATURE" = essai ] || arret "--seulement et --sans-verif-connexions sont réservés aux essais"
  fi
  [ "$(git_tete)" = "$APRES_SHA" ] || arret "l'arbre n'est pas au nouveau code"
  verifier_cible "$CIBLE_BASE" || arret
  if [ "$verif" = oui ]; then verifier_connexions "$CIBLE_BASE" || arret; fi
  _django "$OUTIL_DIR/bascule_fumee.py" cible || arret "identité de la cible vue par Django"
  local app
  for app in email_manager pdf_manager; do
    [ -n "$seulement" ] && [ "$app" != "$seulement" ] && continue
    info "migration $app 0009_quote_regime (attente de verrou bornée à $BASCULE_LOCK_TIMEOUT)"
    if ! _django manage.py migrate "$app" 0009_quote_regime; then
      echec "migration de $app en échec"; diagnostic_migration; exit 1
    fi
  done
  if [ -n "$seulement" ]; then etat_ecrire ETAPE b5-partiel; else etat_ecrire ETAPE b5; fi
}

# --- B6 : vérifications --------------------------------------------------------------------------------
e_b6 () {
  etat_lire; exiger_etape b5; charger_identifiants || arret
  verifier_cible "$CIBLE_BASE" || arret
  verifier_connexions "$CIBLE_BASE" || arret
  _django "$OUTIL_DIR/bascule_fumee.py" cible || arret "identité de la cible vue par Django"
  _django manage.py migrate --check || arret "migrations en attente"
  ok "aucune migration en attente"
  instantane "$CIBLE_BASE" "$DOSSIER/b6_cible" "$DOSSIER/ref.colonnes" || arret
  comparer_apres_migration "$DOSSIER/ref" "$DOSSIER/b6_cible" || arret "écart inattendu après migration"
  local comptes attendu
  comptes=$(comptes_regime "$CIBLE_BASE") || arret
  attendu=$(printf 'email_manager_quote|HERITE|%s\npdf_manager_quote|HERITE|%s' "$COMPTE_COURRIEL" "$COMPTE_PDF")
  [ "$comptes" = "$attendu" ] || arret "comptes par régime : $(echo $comptes), attendu $(echo $attendu)"
  ok "comptes par régime : tout HERITE, $COMPTE_COURRIEL + $COMPTE_PDF comme à la sauvegarde"
  _django "$OUTIL_DIR/bascule_fumee.py" fumee --courriel "$COMPTE_COURRIEL" --pdf "$COMPTE_PDF" || arret "contrôle de fumée"
  instantane "$CIBLE_BASE" "$DOSSIER/b6_apres_fumee" "$DOSSIER/ref.colonnes" || arret
  comparer_identique "$DOSSIER/b6_cible" "$DOSSIER/b6_apres_fumee" || arret "le contrôle de fumée a laissé une trace durable"
  ok "aucune trace durable du contrôle de fumée (contenu, schéma, séquences, migrations)"
  etat_ecrire ETAPE b6
}

# --- B7 : réouverture -------------------------------------------------------------------------------------
e_b7 () {
  local simuler=non
  [ "${1:-}" = --simuler ] && simuler=oui
  etat_lire; exiger_etape b6
  if [ "$CIBLE_NATURE" = reelle ]; then
    [ "$simuler" = non ] || arret "--simuler est réservé aux essais"
    lsof -nP -iTCP:"$SERVEUR_PORT" -sTCP:LISTEN >/dev/null 2>&1 || arret "le serveur n'écoute pas sur $SERVEUR_PORT : le démarrer d'abord"
    local code
    code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$SERVEUR_PORT/accounts/login/") || code=000
    [ "$code" = 200 ] || arret "page de connexion : HTTP $code"
    ok "serveur en marche (page de connexion : HTTP 200)"
  else
    [ "$simuler" = oui ] || arret "essai : b7 --simuler"
    info "essai : réouverture simulée"
  fi
  etat_ecrire REOUVERT oui
  etat_ecrire REOUVERT_LE "$(date '+%Y-%m-%d %H:%M:%S')"
  etat_ecrire ETAPE b7
}

# --- R1 : retour du code --------------------------------------------------------------------------------
e_r1 () {
  etat_lire; charger_identifiants || arret
  verifier_cible "$CIBLE_BASE" || arret
  local r
  r=$(regime_en_base) || arret "état de la base illisible"
  [ "$r" = "0|0" ] || arret "la base porte encore le régime ($r : migrations 0009 | colonnes regime) : R2 ou R3 d'abord — l'ancien code ne peut pas écrire de citations sur ce schéma"
  ok "base sans régime : aucune 0009, aucune colonne regime"
  git_propre || arret "arbre non propre : reparer-git d'abord"
  case "$(git_tete)" in
    "$AVANT_SHA") ok "arbre déjà à $AVANT_SHA" ;;
    "$APRES_SHA") git -C "$CIBLE_ARBRE" reset --keep "$AVANT_SHA" || arret "git reset --keep" ;;
    *) arret "HEAD inattendu : $(git_tete)" ;;
  esac
  [ "$(git_tete)" = "$AVANT_SHA" ] && git_propre || arret "après R1 : HEAD ou arbre inattendus"
  ok "arbre revenu à $AVANT_SHA, propre"
  etat_ecrire ETAPE r1
  [ "$CIBLE_NATURE" = reelle ] && info "redémarrer le serveur : cd $CIBLE_ARBRE && .venv/bin/python manage.py runserver 0.0.0.0:$SERVEUR_PORT"
  return 0
}

# --- R2 : migrations défaites -------------------------------------------------------------------------------
e_r2 () {
  etat_lire; charger_identifiants || arret
  [ "$(git_tete)" = "$APRES_SHA" ] || arret "R2 exige le nouveau code (ses fichiers de migration) ; sinon R3"
  verifier_cible "$CIBLE_BASE" || arret
  verifier_connexions "$CIBLE_BASE" || arret
  _django "$OUTIL_DIR/bascule_fumee.py" cible || arret "Django ne peut pas viser la base : R2 impossible, passer à R3"
  _django manage.py migrate pdf_manager 0008_alter_pdfdocument_options || arret "retour de pdf_manager"
  _django manage.py migrate email_manager 0008_email_cause_origine || arret "retour de email_manager"
  instantane "$CIBLE_BASE" "$DOSSIER/r2_cible" "$DOSSIER/ref.colonnes" || arret
  if [ "$REOUVERT" = oui ]; then
    comparer_apres_r2 "$DOSSIER/ref" "$DOSSIER/r2_cible" reouverte || arret "après R2 : écart de structure"
  else
    comparer_apres_r2 "$DOSSIER/ref" "$DOSSIER/r2_cible" || arret "après R2 : écart inattendu"
  fi
  etat_ecrire ETAPE r2
  info "il reste R1"
}

# --- R3 : restauration de la référence -----------------------------------------------------------------------
e_r3 () {
  local perte=non
  [ "${1:-}" = --perte-acceptee ] && perte=oui
  etat_lire; charger_identifiants || arret
  if [ "$REOUVERT" = oui ] && [ "$perte" = non ]; then
    arret "après réouverture ($REOUVERT_LE), R3 perd les écritures faites depuis : diagnostic, puis décision explicite (--perte-acceptee)"
  fi
  if ! base_existe "$CIBLE_BASE" && base_existe "$ECHEC_BASE" && base_existe "$REF_BASE"; then
    info "reprise : premier renommage déjà fait"
  else
    base_existe "$REF_BASE" || arret "référence $REF_BASE absente"
    verifier_connexions "$CIBLE_BASE" "$REF_BASE" || arret
    instantane "$REF_BASE" "$DOSSIER/r3_ref_controle" || arret
    comparer_identique "$DOSSIER/ref" "$DOSSIER/r3_ref_controle" || arret "la référence a changé depuis B2"
    if [ "$REOUVERT" = oui ]; then
      local d="$DOSSIER/apres_reouverture_$(date +%Y%m%d-%H%M%S).dump"
      "$PG_BIN/pg_dump" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -Fc -f "$d" "$CIBLE_BASE" || arret "sauvegarde de l'état rouvert"
      ok "état rouvert sauvegardé : $d"
    fi
    _psql -d postgres -c "ALTER DATABASE \"$CIBLE_BASE\" RENAME TO \"$ECHEC_BASE\"" || arret "premier renommage"
    ok "$CIBLE_BASE → $ECHEC_BASE"
  fi
  _psql -d postgres -c "ALTER DATABASE \"$REF_BASE\" RENAME TO \"$CIBLE_BASE\"" || arret "second renommage (relancer r3)"
  ok "$REF_BASE → $CIBLE_BASE"
  verifier_cible "$CIBLE_BASE" || arret
  instantane "$CIBLE_BASE" "$DOSSIER/r3_cible" || arret
  comparer_identique "$DOSSIER/ref" "$DOSSIER/r3_cible" || arret "après R3 : la base n'est pas la sauvegarde B2"
  etat_ecrire ETAPE r3
  info "base en échec conservée : $ECHEC_BASE ; il reste R1"
}

# --- Réparation d'une avance rapide interrompue -------------------------------------------------------------
e_reparer_git () {
  etat_lire
  local tete permis ligne chemin fichiers="" a_suppr=""
  tete=$(git_tete)
  [ "$tete" = "$AVANT_SHA" ] || [ "$tete" = "$APRES_SHA" ] || arret "HEAD inattendu : $tete"
  permis=$(git -C "$CIBLE_ARBRE" diff --name-only "$AVANT_SHA" "$APRES_SHA")
  while IFS= read -r ligne; do
    [ -n "$ligne" ] || continue
    chemin=${ligne:3}
    printf '%s\n' "$permis" | grep -qxF -- "$chemin" || arret "modification hors de la bascule : $ligne — ne rien toucher, examiner à la main"
    case "$ligne" in
      '??'*) a_suppr="$a_suppr $chemin" ;;
      *) fichiers="$fichiers $chemin" ;;
    esac
  done <<EOF
$(git -C "$CIBLE_ARBRE" status --porcelain --untracked-files=all)
EOF
  for chemin in $fichiers; do
    if git -C "$CIBLE_ARBRE" cat-file -e "$tete:$chemin" 2>/dev/null; then
      git -C "$CIBLE_ARBRE" checkout -f "$tete" -- "$chemin" || arret "restauration de $chemin"
    else   # ajouté à l'index par l'avance interrompue, absent de HEAD
      git -C "$CIBLE_ARBRE" rm -q --cached --ignore-unmatch -- "$chemin" || arret "retrait de l'index : $chemin"
      rm -f -- "$CIBLE_ARBRE/$chemin" || arret "suppression de $chemin"
    fi
  done
  for chemin in $a_suppr; do rm -f -- "$CIBLE_ARBRE/$chemin" || arret "suppression de $chemin"; done
  git_propre || arret "l'arbre n'est toujours pas propre"
  ok "arbre remis à $tete, propre"
}

# --- Diagnostic -----------------------------------------------------------------------------------------------
e_etat () {
  etat_lire; charger_identifiants || arret
  info "état : $ETAT"
  info "nature $CIBLE_NATURE · base $CIBLE_BASE · arbre $CIBLE_ARBRE · étape atteinte $ETAPE · rouvert $REOUVERT"
  local tete; tete=$(git_tete)
  case "$tete" in "$AVANT_SHA") info "Git : HEAD = avant ($AVANT_SHA)" ;; "$APRES_SHA") info "Git : HEAD = après ($APRES_SHA)" ;; *) info "Git : HEAD inattendu ($tete)" ;; esac
  git_propre && info "Git : arbre propre" || info "Git : arbre NON propre → reparer-git"
  local b
  for b in "$CIBLE_BASE" "$REF_BASE" "$ECHEC_BASE"; do base_existe "$b" && info "base présente : $b" || info "base absente : $b"; done
  if base_existe "$CIBLE_BASE"; then
    info "régime en base (0009 | colonnes) : $(regime_en_base)"
    verifier_connexions "$CIBLE_BASE" || true
  fi
}

# --- Aiguillage --------------------------------------------------------------------------------------------------
commande=${1:-}; [ $# -gt 0 ] && shift
case "$commande" in
  ouvrir)
    BASCULE_H=$(date +%Y%m%d-%H%M%S)
    nature_d=""; dossier_d=""
    for ((i = 1; i <= $#; i++)); do
      case "${!i}" in --nature) j=$((i + 1)); nature_d=${!j} ;; --dossier) j=$((i + 1)); dossier_d=${!j} ;; esac
    done
    DOSSIER=${dossier_d:-$SAUV_DEFAUT/bascule_${nature_d:-inconnue}_$BASCULE_H}
    mkdir -p "$DOSSIER" && chmod 700 "$DOSSIER" || exit 1
    ETAT="$DOSSIER/etat.env"; JOURNAL="$DOSSIER/journal.log"
    { echo "=== $(date '+%Y-%m-%d %H:%M:%S') — ouvrir $*"; e_ouvrir "$@"; } 2>&1 | tee -a "$JOURNAL"
    rc=${PIPESTATUS[0]} ;;
  b1|b2|b3|b4|b5|b6|b7|r1|r2|r3|reparer-git|etat)
    ETAT=""; reste=()
    while [ $# -gt 0 ]; do
      case "$1" in --etat) ETAT=$2; shift 2 ;; *) reste+=("$1"); shift ;; esac
    done
    [ -n "$ETAT" ] && [ -r "$ETAT" ] || { echec "--etat <dossier>/etat.env requis"; exit 1; }
    JOURNAL="$(dirname "$ETAT")/journal.log"
    fonction="e_${commande//-/_}"
    { echo "=== $(date '+%Y-%m-%d %H:%M:%S') — $commande ${reste[*]:-}"; "$fonction" ${reste[@]+"${reste[@]}"}; } 2>&1 | tee -a "$JOURNAL"
    rc=${PIPESTATUS[0]} ;;
  *)
    echo "usage : bash $0 ouvrir … | <b1…b7|r1|r2|r3|reparer-git|etat> --etat <dossier>/etat.env [options]" >&2
    exit 2 ;;
esac
if [ "$rc" -eq 0 ]; then echo "=== $commande : OK" | tee -a "$JOURNAL"; else echo "=== $commande : ÉCHEC (code $rc)" | tee -a "$JOURNAL"; fi
exit "$rc"
