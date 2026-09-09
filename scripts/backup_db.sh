#!/bin/bash
#
# Sauvegarde de la base PostgreSQL du projet.
#
# Ecrit toujours le meme fichier (court_project_pg.dump), donc chaque execution
# ecrase la precedente. Le dump est d'abord ecrit dans un fichier temporaire puis
# verifie ; il ne remplace la sauvegarde existante que s'il est valide, pour ne
# jamais detruire une bonne sauvegarde avec un dump rate.
#
# Format : pg_dump -Fc (custom, compresse) -> restaurer avec pg_restore.
#
# Emplacement de la sauvegarde : ~/Backups/court/ (hors du depot, et hors de
# ~/Documents que macOS protege : une tache launchd n'y a pas acces).
#
# Identifiants lus dans, par ordre de priorite :
#   1. ~/.court-backup.env   (genere par scripts/install_backup_agent.sh, mode 600)
#   2. le .env du projet     (seulement pour une execution manuelle depuis le depot)
#
# Usage : ./scripts/backup_db.sh
#

set -euo pipefail

BACKUP_DIR="${COURT_BACKUP_DIR:-$HOME/Backups/court}"
TARGET="$BACKUP_DIR/court_project_pg.dump"
LOG="$BACKUP_DIR/backup_db.log"
PG_BIN="/Library/PostgreSQL/18/bin"

mkdir -p "$BACKUP_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

CREDS=""
if [ -r "$HOME/.court-backup.env" ]; then
    CREDS="$HOME/.court-backup.env"
else
    PROJECT_ENV="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." 2>/dev/null && pwd)/.env"
    [ -r "$PROJECT_ENV" ] && CREDS="$PROJECT_ENV"
fi

if [ -z "$CREDS" ]; then
    log "ERREUR : aucun fichier d'identifiants (~/.court-backup.env ni .env du projet)."
    log "         Lancer scripts/install_backup_agent.sh depuis le depot."
    exit 1
fi

set -a
# shellcheck disable=SC1090
. "$CREDS"
set +a

: "${DB_NAME:?DB_NAME absent de $CREDS}"
: "${DB_USER:?DB_USER absent de $CREDS}"
: "${DB_HOST:?DB_HOST absent de $CREDS}"
: "${DB_PORT:?DB_PORT absent de $CREDS}"
: "${DB_PASSWORD:?DB_PASSWORD absent de $CREDS}"

TMP="$(mktemp "$BACKUP_DIR/.court_project_pg.dump.XXXXXX")"
trap 'rm -f "$TMP"' EXIT

log "Debut de la sauvegarde de $DB_NAME ($DB_HOST:$DB_PORT)."

export PGPASSWORD="$DB_PASSWORD"
if ! "$PG_BIN/pg_dump" \
        --host="$DB_HOST" --port="$DB_PORT" --username="$DB_USER" \
        --dbname="$DB_NAME" \
        --format=custom --compress=9 --no-owner --no-privileges \
        --file="$TMP" 2>>"$LOG"; then
    log "ECHEC : pg_dump a retourne une erreur. La sauvegarde precedente est conservee."
    exit 1
fi
unset PGPASSWORD

# Verification : un dump illisible ne doit pas ecraser le precedent.
if ! "$PG_BIN/pg_restore" --list "$TMP" >/dev/null 2>>"$LOG"; then
    log "ECHEC : le dump produit est illisible. La sauvegarde precedente est conservee."
    exit 1
fi

mv -f "$TMP" "$TARGET"
trap - EXIT
chmod 600 "$TARGET"

log "OK : $TARGET ($(du -h "$TARGET" | cut -f1))."

# Le journal ne grossit pas indefiniment.
if [ "$(wc -l < "$LOG")" -gt 2000 ]; then
    tail -n 1000 "$LOG" > "$LOG.tmp" && mv -f "$LOG.tmp" "$LOG"
fi
