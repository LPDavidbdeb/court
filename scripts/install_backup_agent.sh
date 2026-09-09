#!/bin/bash
#
# Installe (ou reinstalle) la sauvegarde quotidienne de la base a 01h00.
#
# Pourquoi une copie hors du depot : le projet vit dans ~/Documents, que macOS
# protege (TCC). Une tache launchd n'a pas le droit d'y lire le script ni le
# .env, ni d'y ecrire le dump -- elle echouerait chaque nuit avec
# "Operation not permitted". Tout ce que la tache planifiee touche est donc
# place dans ~/Backups/court/, hors de ~/Documents.
#
# Le depot reste la source de verite : relancer ce script apres toute
# modification de scripts/backup_db.sh pour redeployer.
#
# Usage : ./scripts/install_backup_agent.sh
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$HOME/Backups/court"
CREDS="$HOME/.court-backup.env"
PLIST="$HOME/Library/LaunchAgents/com.court.backup-db.plist"
LABEL="com.court.backup-db"

mkdir -p "$BACKUP_DIR" "$HOME/Library/LaunchAgents"

# 1. Identifiants : extraits du .env du projet, en 600, hors de ~/Documents.
if [ ! -r "$PROJECT_ROOT/.env" ]; then
    echo "ERREUR : $PROJECT_ROOT/.env introuvable." >&2
    exit 1
fi
umask 077
{
    echo "# Genere par scripts/install_backup_agent.sh -- ne pas editer a la main."
    echo "# Relancer ce script apres tout changement des DB_* dans le .env du projet."
    grep -E '^\s*DB_(ENGINE|NAME|USER|PASSWORD|HOST|PORT)=' "$PROJECT_ROOT/.env"
} > "$CREDS"
chmod 600 "$CREDS"
echo "Identifiants  -> $CREDS (600)"

# 2. Copie du script executee par launchd.
cp "$PROJECT_ROOT/scripts/backup_db.sh" "$BACKUP_DIR/backup_db.sh"
chmod +x "$BACKUP_DIR/backup_db.sh"
echo "Script        -> $BACKUP_DIR/backup_db.sh"

# 3. LaunchAgent : tous les jours a 01h00.
cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$BACKUP_DIR/backup_db.sh</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$BACKUP_DIR</string>

    <!-- Tous les jours a 01h00. Si le Mac dort a cette heure, launchd lance la
         tache des le reveil (contrairement a cron qui l'aurait sautee). -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>1</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>$BACKUP_DIR/launchd.out.log</string>
    <key>StandardErrorPath</key>
    <string>$BACKUP_DIR/launchd.err.log</string>

    <!-- La sauvegarde ne doit pas ralentir une session de travail. -->
    <key>ProcessType</key>
    <string>Background</string>
    <key>LowPriorityIO</key>
    <true/>
</dict>
</plist>
PLIST_EOF
plutil -lint "$PLIST" >/dev/null
echo "LaunchAgent   -> $PLIST"

# 4. (Re)chargement.
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo
echo "Tache chargee. Prochaine execution : 01h00."
echo "Test immediat : launchctl kickstart -k gui/\$(id -u)/$LABEL"
