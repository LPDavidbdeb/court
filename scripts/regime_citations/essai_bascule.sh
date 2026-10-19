#!/usr/bin/env bash
# Banc d'essai de la bascule du régime des citations : rejoue le chemin nominal et les scénarios
# d'échec sur des bases jetables et un arbre de travail temporaire, qui appartiennent à cette seule
# exécution (ressources_essai.sh). Ne vise jamais la base réelle : les seuls appels qui la nomment
# sont des refus attendus, avant toute connexion, et une lecture finale qui vérifie qu'elle est intacte.
#
#   env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin bash --noprofile --norc \
#       scripts/regime_citations/essai_bascule.sh --dossier <dossier neuf> [--id <identifiant>] \
#       [--vers <réf. Git>] [--source <sauvegarde .dump>]
#   … essai_bascule.sh --nettoyer --dossier <dossier d'une exécution>     (après interruption)
#
# Ressources de l'exécution <id> (défaut : e<AAMMJJ>_<HHMMSS>) : les bases bascule_essai_<id>_*, l'arbre
# ../court-bascule-essai-<id> (marqué dans ses métadonnées Git) et la branche bascule-essai/<id>, inscrits dans
# <dossier>/ressources.env. Leur absence est vérifiée avant création ; seules elles sont supprimées ;
# le dossier (journaux, instantanés, résultats) est toujours conservé.
#
# Préalables : une sauvegarde de la base (défaut : la sauvegarde nocturne
# ~/Backups/court/court_project_pg.dump ; en P6, une sauvegarde fraîche), le
# dépôt avec epic/E01-numerotation-concordance et la cible d'intégration.
# Sortie : une ligne RÉUSSI/RATÉ par contrôle, un bilan, code 0 si tout a réussi.

if [ -z "${BASH_VERSION:-}" ]; then echo "ÉCHEC   bash requis" >&2; exit 1; fi
set -uo pipefail

OUTIL=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
. "$OUTIL/bascule_fonctions.sh" || exit 1
. "$OUTIL/ressources_essai.sh" || exit 1

DEPOT=/Users/Louis-Philippe/Documents/GitHub/court
SOURCE_DUMP=$HOME/Backups/court/court_project_pg.dump
PYTHON=/Users/Louis-Philippe/Documents/GitHub/court/.venv/bin/python
DEPOTS_PREFIXE=/Users/Louis-Philippe/Documents/GitHub/court
VERS=integration/quote-regime-step1
RACINE=""; ID=""; NETTOYER=non
while [ $# -gt 0 ]; do
  case "$1" in
    --dossier) RACINE=$2; shift 2 ;; --vers) VERS=$2; shift 2 ;; --source) SOURCE_DUMP=$2; shift 2 ;;
    --id) ID=$2; shift 2 ;; --nettoyer) NETTOYER=oui; shift ;;
    *) echo "option inconnue : $1" >&2; exit 2 ;;
  esac
done
[ -n "$RACINE" ] || { echo "--dossier requis" >&2; exit 2; }
charger_identifiants || exit 1

nettoyer_execution () {  # supprime les seules ressources de l'exécution ID ; garde le dossier
  local ko=0
  supprimer_bases_possedees "$ID" || ko=1
  supprimer_arbre_possede "$DEPOT" "$ARBRE" "$ID" || ko=1
  supprimer_branche_possedee "$DEPOT" "$BRANCHE" "$ID" || ko=1
  return $ko
}

if [ "$NETTOYER" = oui ]; then
  [ -r "$RACINE/ressources.env" ] || { echo "ÉCHEC   aucun manifeste $RACINE/ressources.env : rien n'est supprimé" >&2; exit 1; }
  . "$RACINE/ressources.env"
  echo "=== nettoyage de l'exécution $ID (dossier conservé : $RACINE)"
  nettoyer_execution; exit $?
fi

[ -r "$SOURCE_DUMP" ] || { echo "sauvegarde source illisible : $SOURCE_DUMP" >&2; exit 2; }
[ -n "$ID" ] || ID="e$(date +%y%m%d_%H%M%S)"
id_valide "$ID" || { echo "identifiant invalide : $ID (minuscules, chiffres, « _ », 24 caractères au plus)" >&2; exit 2; }
[ ! -e "$RACINE/ressources.env" ] || { echo "ÉCHEC   $RACINE contient déjà une exécution : prendre un dossier neuf" >&2; exit 1; }
BASE="$(prefixe_bases "$ID")_cible"
ARBRE="/Users/Louis-Philippe/Documents/GitHub/court-bascule-essai-$ID"
BRANCHE="bascule-essai/$ID"
verifier_ressources_libres "$ID" "$DEPOT" "arbre:$ARBRE" "branche:$BRANCHE" || exit 1
mkdir -p "$RACINE" || exit 1
printf 'ID=%s\nARBRE=%s\nBRANCHE=%s\nBASE=%s\n' "$ID" "$ARBRE" "$BRANCHE" "$BASE" > "$RACINE/ressources.env"

REUSSIS=0; RATES=0
# etape LIBELLÉ ATTENDU commande… : ATTENDU = un code précis, ou « non-nul »
etape () {
  local libelle=$1 attendu=$2 rc; shift 2
  "$@"; rc=$?
  if { [ "$attendu" = non-nul ] && [ "$rc" -ne 0 ]; } || [ "$rc" = "$attendu" ]; then
    echo "RÉUSSI  $libelle (code $rc)"; REUSSIS=$((REUSSIS + 1))
  else
    echo "RATÉ    $libelle (code $rc, attendu $attendu)"; RATES=$((RATES + 1))
  fi
}
pilote () {
  bash "$OUTIL/bascule.sh" "$@" > "$RACINE/derniere_sortie.log" 2>&1; local rc=$?
  sed 's/^/    | /' "$RACINE/derniere_sortie.log"; return $rc
}
enchainer () {  # étapes… : rend le code de la première qui échoue
  local e
  for e in "$@"; do pilote "$e" --etat "$ETAT" || return $?; done
}

AVANT=$(git -C "$DEPOT" rev-parse epic/E01-numerotation-concordance)
APRES=$(git -C "$DEPOT" rev-parse --verify "$VERS^{commit}")
echo "=== banc d'essai — avant $AVANT, cible $VERS = $APRES, $(date '+%Y-%m-%d %H:%M:%S')"
echo "=== environnement : DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-<absent>} PYTHONPATH=${PYTHONPATH:-<absent>} LANG=${LANG:-<absent>}"
echo "=== source des bases d'essai : $SOURCE_DUMP ($(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$SOURCE_DUMP"))"
echo "=== exécution $ID : bases $(prefixe_bases "$ID")_*, arbre $ARBRE, branche $BRANCHE"

# --- Mise en place et nettoyage ----------------------------------------------------------------------
base_fraiche () {  # la base cible de l'exécution, restaurée ; les bases du scénario précédent supprimées
  supprimer_bases_possedees "$ID" > /dev/null || return 1
  creer_base_possedee "$BASE" "$ID" &&
    "$PG_BIN/pg_restore" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -d "$BASE" --no-owner --exit-on-error "$SOURCE_DUMP"
}
arbre_frais () {
  if [ ! -e "$ARBRE" ]; then
    git -C "$DEPOT" worktree add -q -b "$BRANCHE" "$ARBRE" "$AVANT" || return 1
    marquer_arbre "$ARBRE" "$ID"
    # .env propre à l'arbre d'essai : DB_NAME vise la base d'essai, même pour une commande lancée à la main
    sed "s/^DB_NAME=.*/DB_NAME=$BASE/" "$DEPOT/.env" > "$ARBRE/.env" && chmod 600 "$ARBRE/.env" || return 1
  fi
  est_arbre_possede "$DEPOT" "$ARBRE" "$ID" || { echec "l'arbre $ARBRE n'appartient pas à l'exécution $ID"; return 1; }
  git -C "$ARBRE" checkout -q -f "$BRANCHE" && git -C "$ARBRE" reset -q --hard "$AVANT" \
    && git -C "$ARBRE" clean -q -fd -e .env
}
mise_en_place () { base_fraiche && arbre_frais; }
ouvrir_scenario () {  # $1 nom -> ETAT
  local d="$RACINE/$1"; rm -rf "$d"; ETAT="$d/etat.env"
  pilote ouvrir --nature essai --base "$BASE" --arbre "$ARBRE" --branche "$BRANCHE" --vers "$APRES" --dossier "$d" --python "$PYTHON"
}
tenir_connexion () {  # $1 base, $2 secondes, [$3 sql] : session « essai_teneur » en arrière-plan
  PGAPPNAME="essai_teneur_$ID" "$PG_BIN/psql" -X -q -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -d "$1" \
    -c "begin; ${3:-select 1}; select pg_sleep($2); commit;" > /dev/null 2>&1 &
  TENEUR=$!; sleep 2
}
lacher_connexion () {  # côté serveur : pg_sleep ne voit pas la fermeture du client
  _psql -d postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where application_name='essai_teneur_$ID'" > /dev/null
  kill "$TENEUR" 2> /dev/null; wait "$TENEUR" 2> /dev/null; sleep 1
}
fumee_directe () {  # $1 mode, reste : arguments — environnement explicite, comme le pilote
  ( cd "$ARBRE" && env -i HOME="$HOME" PATH=/usr/bin:/bin LANG=en_CA.UTF-8 DJANGO_SETTINGS_MODULE=settings_bascule \
      PYTHONPATH="$OUTIL" BASCULE_BASE="$BASE" BASCULE_PORT="$CIBLE_PORT" BASCULE_SYSID="$CIBLE_SYSID" \
      "$PYTHON" "$OUTIL/bascule_fumee.py" "$@" > "$RACINE/fumee_directe.log" 2>&1 )
}

# --- S-A : chemin nominal, avance rapide interrompue (S-F), R2 puis R1 -------------------------------------
echo; echo "=== S-A — nominal B1 → B6 ; S-F avance rapide interrompue ; retour R2 puis R1"
mise_en_place || { echo "mise en place impossible"; exit 1; }
etape "S-A ouvrir" 0 ouvrir_scenario S-A
etape "S-A B1" 0 pilote b1 --etat "$ETAT"
etape "S-A B2 sauvegarde et restauration prouvée" 0 pilote b2 --etat "$ETAT"
git -C "$ARBRE" checkout -q "$APRES" -- core/quote_regime.py email_manager/models.py   # avance « interrompue »
etape "S-F B3 refuse un arbre non propre" 1 pilote b3 --etat "$ETAT"
echo "contenu étranger" >> "$ARBRE/manage.py"
etape "S-F reparer-git refuse une modification étrangère" 1 pilote reparer-git --etat "$ETAT"
git -C "$ARBRE" checkout -q -- manage.py
etape "S-F reparer-git remet l'arbre propre" 0 pilote reparer-git --etat "$ETAT"
etape "S-A B3 avance rapide" 0 pilote b3 --etat "$ETAT"
etape "S-A B4" 0 pilote b4 --etat "$ETAT"
etape "S-A B5 migrations" 0 pilote b5 --etat "$ETAT"
etape "S-A B6 vérifications, fumée, absence de trace durable" 0 pilote b6 --etat "$ETAT"
. "$ETAT"
etape "S-A fumée avec des comptes faux → échec" 1 fumee_directe fumee --courriel 1 --pdf 1
etape "S-A fumée sans environnement explicite → refus" 2 \
  bash -c "cd '$ARBRE' && env -i HOME='$HOME' PATH=/usr/bin:/bin '$PYTHON' '$OUTIL/bascule_fumee.py' cible > '$RACINE/fumee_sans_env.log' 2>&1"
etape "S-A R1 refusé tant que la base porte le régime" 1 pilote r1 --etat "$ETAT"
etape "S-A R2" 0 pilote r2 --etat "$ETAT"
etape "S-A R1" 0 pilote r1 --etat "$ETAT"
etape "S-A arbre revenu à l'état d'avant" 0 test "$(git -C "$ARBRE" rev-parse HEAD)" = "$AVANT"

# --- S-B : R3, connexion résiduelle, R3 interrompu ----------------------------------------------------------------
echo; echo "=== S-B — R3 (connexion résiduelle, puis reprise après interruption)"
mise_en_place || exit 1
etape "S-B ouvrir" 0 ouvrir_scenario S-B
etape "S-B B1 → B6" 0 enchainer b1 b2 b3 b4 b5 b6
. "$ETAT"
tenir_connexion "$REF_BASE" 120
etape "S-B R3 refusé (connexion ouverte sur la référence)" 1 pilote r3 --etat "$ETAT"
lacher_connexion
etape "S-B interruption simulée après le premier renommage" 0 _psql -d postgres -c "ALTER DATABASE \"$BASE\" RENAME TO \"$ECHEC_BASE\""
etape "S-B R3 reprend et restaure la référence" 0 pilote r3 --etat "$ETAT"
etape "S-B R1 après R3" 0 pilote r1 --etat "$ETAT"

# --- S-C : migration partielle --------------------------------------------------------------------------------------
echo; echo "=== S-C — migration partielle (email_manager seule), puis R2 et R1"
mise_en_place || exit 1
etape "S-C ouvrir" 0 ouvrir_scenario S-C
etape "S-C B1 → B4" 0 enchainer b1 b2 b3 b4
etape "S-C B5 partiel" 0 pilote b5 --seulement email_manager --etat "$ETAT"
etape "S-C B6 refusé après une migration partielle" 1 pilote b6 --etat "$ETAT"
etape "S-C R2 après migration partielle" 0 pilote r2 --etat "$ETAT"
etape "S-C R1" 0 pilote r1 --etat "$ETAT"

# --- S-D : connexions et verrous --------------------------------------------------------------------------------------
echo; echo "=== S-D — connexion ouverte, puis verrou tenu pendant la migration"
mise_en_place || exit 1
etape "S-D ouvrir" 0 ouvrir_scenario S-D
etape "S-D B1 → B4" 0 enchainer b1 b2 b3 b4
tenir_connexion "$BASE" 120 "lock table email_manager_quote in access share mode"
etape "S-D B5 refusé (connexion ouverte)" 1 pilote b5 --etat "$ETAT"
debut=$(date +%s)
etape "S-D B5 sans contrôle de connexion : arrêté par le délai de verrou" 1 pilote b5 --sans-verif-connexions --etat "$ETAT"
echo "    | durée : $(( $(date +%s) - debut )) s (délai de verrou : 10 s, plus le démarrage de Django)"
grep -q "lock timeout" "$RACINE/derniere_sortie.log"; etape "S-D cause : « lock timeout »" 0 test $? = 0
lacher_connexion
etape "S-D aucune 0009 appliquée après l'échec" 0 \
  test "$(_psql -d "$BASE" -c "select count(*) from django_migrations where name='0009_quote_regime'")" = 0
etape "S-D B5 une fois le verrou levé" 0 pilote b5 --etat "$ETAT"
etape "S-D R2" 0 pilote r2 --etat "$ETAT"
etape "S-D R1" 0 pilote r1 --etat "$ETAT"

# --- S-E : incident après réouverture -------------------------------------------------------------------------------------
echo; echo "=== S-E — incident après réouverture : l'écriture légitime est conservée"
mise_en_place || exit 1
etape "S-E ouvrir" 0 ouvrir_scenario S-E
etape "S-E B1 → B6" 0 enchainer b1 b2 b3 b4 b5 b6
etape "S-E B7 (réouverture simulée)" 0 pilote b7 --simuler --etat "$ETAT"
legit=$(_psql -d "$BASE" -c "insert into email_manager_quote (quote_text, created_at, updated_at, email_id, regime) select 'écriture légitime après réouverture', now(), now(), min(id), 'HERITE' from email_manager_email returning id")
etape "S-E écriture légitime après réouverture (id $legit)" 0 test -n "$legit"
etape "S-E R3 refusé sans décision explicite" 1 pilote r3 --etat "$ETAT"
etape "S-E R2 après réouverture (structure seulement)" 0 pilote r2 --etat "$ETAT"
etape "S-E écriture légitime conservée après R2" 0 \
  test "$(_psql -d "$BASE" -c "select count(*) from email_manager_quote where id=$legit")" = 1
etape "S-E R1" 0 pilote r1 --etat "$ETAT"

# --- S-G : contrôles unitaires ---------------------------------------------------------------------------------------------
echo; echo "=== S-G — contrôles unitaires"
printf 'table_inexistante\tx.id\n' > "$RACINE/colonnes_fausses.tsv"
etape "S-G md5_tables échoue sur une table inexistante" non-nul \
  bash -c ". '$OUTIL/bascule_fonctions.sh' && charger_identifiants && md5_tables '$BASE' '$RACINE/colonnes_fausses.tsv' > /dev/null 2>&1"
etape "S-G verifier_cible détecte un serveur différent" 1 \
  bash -c ". '$OUTIL/bascule_fonctions.sh' && charger_identifiants && CIBLE_PORT=5432 CIBLE_SYSID=1 verifier_cible '$BASE' 2> /dev/null"
etape "S-G réglages : base réelle refusée sans confirmation (avant toute connexion)" 0 bash -c \
  "cd '$ARBRE' && ! env -i HOME='$HOME' PATH=/usr/bin:/bin DJANGO_SETTINGS_MODULE=settings_bascule PYTHONPATH='$OUTIL' BASCULE_BASE=court_project_pg '$PYTHON' -c 'import django; django.setup()' > '$RACINE/reglages_reelle.log' 2>&1 && grep -q 'BASCULE_REELLE_CONFIRMEE=oui' '$RACINE/reglages_reelle.log'"
etape "S-G ouvrir --nature reelle refusé sans BASCULE_REELLE_CONFIRMEE" 1 \
  pilote ouvrir --nature reelle --base court_project_pg --arbre "$DEPOT" --branche epic/E01-numerotation-concordance --vers "$APRES" --dossier "$RACINE/refus_reelle"
procs=$(processus_projet)
etape "S-G processus_projet détecte les processus Python des arbres du projet" 0 test -n "$procs"
printf '%s\n' "$procs" | sed 's/^/    | /'

# --- Nettoyage et contrôle final ---------------------------------------------------------------------------------------------
echo; echo "=== nettoyage des seules ressources de l'exécution $ID (dossier conservé)"
nettoyer_execution 2>&1 | sed 's/^/    | /'
etape "nettoyage : aucune base de l'exécution $ID restante" 0 test -z "$(bases_possedees "$ID")"
etape "nettoyage : arbre et branche de l'exécution supprimés" 0 \
  bash -c "[ ! -e '$ARBRE' ] && ! git -C '$DEPOT' show-ref --verify --quiet 'refs/heads/$BRANCHE'"
etape "base réelle intacte : aucune 0009, aucune colonne regime (lecture seule)" 0 \
  test "$(_psql -d "$BASE_REELLE" -c "select (select count(*) from django_migrations where name='0009_quote_regime')||'|'||(select count(*) from information_schema.columns where column_name='regime' and table_schema='public')")" = "0|0"
echo; echo "=== bilan : $REUSSIS réussi(s), $RATES raté(s)"
[ "$RATES" -eq 0 ]
