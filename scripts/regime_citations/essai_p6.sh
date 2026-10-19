#!/usr/bin/env bash
# Essais du pilote P6 en simulation (P6_SIMULATION=1) : les opérations longues sont remplacées par des
# substituts, mais les ressources sont réellement créées et supprimées, et les oracles sont les vrais.
#
#   env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin bash --noprofile --norc \
#       scripts/regime_citations/essai_p6.sh --dossier <dossier neuf> [--source <dump>] [--cible-git <réf.>]
#
# Éprouve : l'arrêt de P6 à chacune de ses étapes ; la survie des ressources étrangères (dont une base
# au nom de l'ancien motif global bascule_essai_*, une base au préfixe voisin, une branche et un arbre
# étrangers) ; le refus d'une ressource préexistante au nom de l'exécution ; la reprise après
# interruption ; le refus d'un dossier déjà utilisé et des variables de simulation hors simulation.
# Ne nomme la base réelle qu'en lecture, pour vérifier qu'elle est intacte.

if [ -z "${BASH_VERSION:-}" ]; then echo "ÉCHEC   bash requis" >&2; exit 1; fi
set -uo pipefail

OUTIL=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
. "$OUTIL/bascule_fonctions.sh" || exit 1
. "$OUTIL/ressources_essai.sh" || exit 1
DEPOT=/Users/Louis-Philippe/Documents/GitHub/court
SOURCE=$HOME/Backups/court/court_project_pg.dump
CIBLE_GIT=HEAD
RACINE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dossier) RACINE=$2; shift 2 ;; --source) SOURCE=$2; shift 2 ;; --cible-git) CIBLE_GIT=$2; shift 2 ;;
    *) echo "option inconnue : $1" >&2; exit 2 ;;
  esac
done
[ -n "$RACINE" ] && [ ! -e "$RACINE" ] || { echo "--dossier <dossier neuf> requis" >&2; exit 2; }
mkdir -p "$RACINE" || exit 1
charger_identifiants || exit 1

REUSSIS=0; RATES=0
etape () {
  local libelle=$1 attendu=$2 rc; shift 2
  "$@"; rc=$?
  if [ "$rc" = "$attendu" ]; then echo "RÉUSSI  $libelle (code $rc)"; REUSSIS=$((REUSSIS + 1))
  else echo "RATÉ    $libelle (code $rc, attendu $attendu)"; RATES=$((RATES + 1)); fi
}
p6 () {  # $1 nom du journal, reste : arguments de p6.sh
  local j=$1; shift
  bash "$OUTIL/p6.sh" "$@" > "$RACINE/$j.log" 2>&1; local rc=$?
  sed 's/^/    | /' "$RACINE/$j.log" | grep -E "ÉCHEC|RÉUSSIE|étape|supprimée|supprimé|laissée|laissé|existent|existe" | head -12
  return $rc
}
simul () { P6_SIMULATION=1 p6 "$@"; }

# --- Ressources étrangères ---------------------------------------------------------------------------
ETR_BASE=bascule_essai_etranger                 # nom de l'ancien motif global
ETR_VOISINE=bascule_essai_ps_nominalx           # préfixe voisin de l'exécution ps_nominal
ETR_BRANCHE=bascule-essai/etranger
ETR_ARBRE=/Users/Louis-Philippe/Documents/GitHub/court-bascule-essai-etranger
for b in "$ETR_BASE" "$ETR_VOISINE"; do
  base_existe "$b" && { echo "ÉCHEC   la base $b existe déjà : essai annulé" >&2; exit 1; }
  "$PG_BIN/createdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" "$b" || exit 1
  _psql -d postgres -c "comment on database \"$b\" is 'essai-p6:etranger'" > /dev/null
done
git -C "$DEPOT" show-ref --verify --quiet "refs/heads/$ETR_BRANCHE" && { echo "ÉCHEC   $ETR_BRANCHE existe déjà" >&2; exit 1; }
[ ! -e "$ETR_ARBRE" ] || { echo "ÉCHEC   $ETR_ARBRE existe déjà" >&2; exit 1; }
git -C "$DEPOT" worktree add -q -b "$ETR_BRANCHE" "$ETR_ARBRE" epic/E01-numerotation-concordance || exit 1
marquer_arbre "$ETR_ARBRE" etranger
echo "=== ressources étrangères posées : $ETR_BASE, $ETR_VOISINE, $ETR_BRANCHE, $ETR_ARBRE"

etrangeres_intactes () {
  base_existe "$ETR_BASE" && base_existe "$ETR_VOISINE" && [ -d "$ETR_ARBRE" ] \
    && git -C "$DEPOT" show-ref --verify --quiet "refs/heads/$ETR_BRANCHE"
}
ressources_absentes () {  # $1 ID
  [ -z "$(bases_possedees "$1")" ] && [ ! -e "/Users/Louis-Philippe/Documents/GitHub/court-p6-$1" ] \
    && [ ! -e "/Users/Louis-Philippe/Documents/GitHub/court-bascule-essai-$1_b" ]
}
etapes_suivantes_absentes () {  # $1 dossier, $2 étape échouée : aucune étape ultérieure commencée
  local apres=0 e
  for e in preconditions source banc mesure_a migration mesure_b oracle controle_final; do
    [ "$apres" = 1 ] && grep -q "^debut $e " "$1/etapes.txt" 2>/dev/null && return 1
    [ "$e" = "$2" ] && apres=1
  done
  return 0
}

# --- 1. Échec à chaque étape -----------------------------------------------------------------------------
for e in preconditions source banc mesure_a migration mesure_b oracle controle_final; do
  echo; echo "=== échec simulé à l'étape $e"
  id="ps_$(printf '%s' "$e" | tr -d '_' | cut -c1-12)"; d="$RACINE/echec_$e"
  P6_ECHEC_SIMULE=$e simul "echec_$e" lancer --id "$id" --dossier "$d" --source "$SOURCE" --cible-git "$CIBLE_GIT"; rc=$?
  etape "$e : P6 s'arrête avec le code 1" 0 test "$rc" = 1
  etape "$e : verdict « P6 ÉCHEC — étape $e »" 0 grep -q "P6 ÉCHEC — étape $e$" "$d/p6.log"
  etape "$e : aucune étape ultérieure commencée" 0 etapes_suivantes_absentes "$d" "$e"
  case "$e" in migration|mesure_b|oracle|controle_final)
    etape "$e : ressources laissées pour le diagnostic (base et arbre de mesure présents)" 0 bash -c \
      ". '$OUTIL/bascule_fonctions.sh'; . '$OUTIL/ressources_essai.sh'; charger_identifiants; bases_possedees '$id' | grep -qx '$(prefixe_bases "$id")_mesure' && test -d /Users/Louis-Philippe/Documents/GitHub/court-p6-$id" ;;
  esac
  if [ -r "$d/ressources.env" ]; then
    simul "nettoyer_$e" nettoyer --dossier "$d"; rc=$?; etape "$e : nettoyage après échec" 0 test "$rc" = 0
  else
    simul "nettoyer_$e" nettoyer --dossier "$d"; rc=$?
    etape "$e : sans manifeste, le nettoyage refuse de toucher quoi que ce soit" 0 test "$rc" = 1
  fi
  etape "$e : plus aucune ressource de l'exécution" 0 ressources_absentes "$id"
  etape "$e : journaux conservés" 0 test -s "$d/p6.log"
  etape "$e : ressources étrangères intactes" 0 etrangeres_intactes
done

# --- 2. Parcours nominal simulé ----------------------------------------------------------------------------
echo; echo "=== parcours nominal (simulation)"
d="$RACINE/nominal"
simul nominal lancer --id ps_nominal --dossier "$d" --source "$SOURCE" --cible-git "$CIBLE_GIT"; rc=$?
etape "nominal : code 0" 0 test "$rc" = 0
etape "nominal : verdict « P6 RÉUSSIE »" 0 grep -q "P6 RÉUSSIE$" "$d/p6.log"
etape "nominal : les 8 étapes réussies" 0 test "$(grep -c '^ok ' "$d/etapes.txt")" = 8
etape "nominal : ressources de l'exécution supprimées" 0 ressources_absentes ps_nominal
etape "nominal : journaux et résultats conservés" 0 bash -c "test -s '$d/p6.log' && test -s '$d/A.json' && test -s '$d/oracle_ab.txt'"
etape "nominal : base au préfixe voisin (bascule_essai_ps_nominalx) intacte" 0 base_existe "$ETR_VOISINE"
etape "nominal : ressources étrangères intactes" 0 etrangeres_intactes

# --- 3. Interruption puis reprise -----------------------------------------------------------------------------
echo; echo "=== interruption pendant l'étape migration, nettoyage, relance"
d="$RACINE/interrompu"
( P6_SIMULATION=1 P6_PAUSE=migration bash "$OUTIL/p6.sh" lancer --id ps_interrompu --dossier "$d" --source "$SOURCE" \
    --cible-git "$CIBLE_GIT" > "$RACINE/interrompu.log" 2>&1 ) &
for i in $(seq 1 120); do grep -q "^pause migration" "$d/etapes.txt" 2>/dev/null && break; sleep 1; done
etape "interruption : P6 en pause à l'étape migration" 0 grep -q "^pause migration" "$d/etapes.txt"
etape "interruption : ressources de l'exécution présentes avant l'arrêt" 0 \
  bash -c ". '$OUTIL/bascule_fonctions.sh'; . '$OUTIL/ressources_essai.sh'; charger_identifiants; test -n \"\$(bases_possedees ps_interrompu)\" && test -d /Users/Louis-Philippe/Documents/GitHub/court-p6-ps_interrompu"
for p in $(pgrep -f "p6.sh lancer --id ps_interrompu"); do pkill -P "$p" 2> /dev/null; kill "$p" 2> /dev/null; done
sleep 2
etape "interruption : processus arrêtés" 0 test -z "$(pgrep -f 'p6.sh lancer --id ps_interrompu')"
simul interrompu_etat etat --dossier "$d"; rc=$?; etape "interruption : « etat » lit le manifeste" 0 test "$rc" = 0
simul interrompu_nettoyer nettoyer --dossier "$d"; rc=$?; etape "interruption : nettoyage" 0 test "$rc" = 0
etape "interruption : plus aucune ressource de l'exécution" 0 ressources_absentes ps_interrompu
simul relance lancer --id ps_relance --dossier "$RACINE/relance" --source "$SOURCE" --cible-git "$CIBLE_GIT"; rc=$?
etape "relance après interruption : P6 RÉUSSIE" 0 test "$rc" = 0
etape "relance : ressources supprimées" 0 ressources_absentes ps_relance
etape "interruption : ressources étrangères intactes" 0 etrangeres_intactes

# --- 4. Refus ----------------------------------------------------------------------------------------------------
echo; echo "=== refus"
"$PG_BIN/createdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" bascule_essai_ps_collision_mesure \
  && _psql -d postgres -c "comment on database bascule_essai_ps_collision_mesure is 'essai-p6:etranger'" > /dev/null
simul collision lancer --id ps_collision --dossier "$RACINE/collision" --source "$SOURCE" --cible-git "$CIBLE_GIT"; rc=$?
etape "base préexistante au nom de l'exécution : P6 refuse de démarrer (code 1)" 0 test "$rc" = 1
etape "base préexistante : refus à l'étape preconditions" 0 grep -q "P6 ÉCHEC — étape preconditions$" "$RACINE/collision/p6.log"
etape "base préexistante : laissée intacte" 0 base_existe bascule_essai_ps_collision_mesure
"$PG_BIN/dropdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" bascule_essai_ps_collision_mesure
simul dossier_existant lancer --id ps_autre --dossier "$RACINE/nominal" --source "$SOURCE" --cible-git "$CIBLE_GIT"; rc=$?
etape "dossier déjà utilisé : refus (code 1)" 0 test "$rc" = 1
P6_ECHEC_SIMULE=banc p6 hors_simulation lancer --id ps_hors --dossier "$RACINE/hors_simulation" --source "$SOURCE" --cible-git "$CIBLE_GIT"; rc=$?
etape "variables de simulation hors simulation : refus (code 2)" 0 test "$rc" = 2
etape "variables de simulation hors simulation : aucun dossier créé" 0 test ! -e "$RACINE/hors_simulation"

# --- Fin : ressources étrangères, base réelle, retrait des seules ressources posées par cet essai ------------------
echo; echo "=== fin"
etape "ressources étrangères intactes au terme des essais" 0 etrangeres_intactes
etape "base réelle intacte (lecture seule)" 0 test "$(_psql -d "$BASE_REELLE" -c "select (select count(*) from django_migrations where name='0009_quote_regime')||'|'||(select count(*) from information_schema.columns where column_name='regime' and table_schema='public')")" = "0|0"
for b in "$ETR_BASE" "$ETR_VOISINE"; do
  [ "$(_psql -d postgres -c "select shobj_description(oid, 'pg_database') from pg_database where datname='$b'")" = "essai-p6:etranger" ] \
    && "$PG_BIN/dropdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" "$b"
done
[ "$(cat "$ETR_ARBRE/$MARQUE_ARBRE" 2>/dev/null)" = etranger ] && git -C "$DEPOT" worktree remove --force "$ETR_ARBRE" \
  && git -C "$DEPOT" branch -q -D "$ETR_BRANCHE"
echo "    | ressources posées par cet essai retirées"
echo; echo "=== bilan : $REUSSIS réussi(s), $RATES raté(s)"
[ "$RATES" -eq 0 ]
