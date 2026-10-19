#!/usr/bin/env bash
# Répétition générale P6 de la bascule de l'étape 1 du régime des citations — pilote.
#
#   bash scripts/regime_citations/p6.sh lancer [--source <sauvegarde .dump>] [--id <id>] [--dossier <d>] \
#                                              [--cible-git <réf.>]
#   bash scripts/regime_citations/p6.sh etat     --dossier <dossier d'une exécution P6>
#   bash scripts/regime_citations/p6.sh nettoyer --dossier <dossier d'une exécution P6>
#
# Sans --source, « lancer » prend une sauvegarde fraîche de la base réelle (pg_dump, lecture seule).
# --cible-git (défaut : origin/integration/quote-regime-step1) est la version de l'outil exigée.
#
# Étapes, dans l'ordre : preconditions, source, banc, mesure_a, migration, mesure_b, oracle,
# controle_final. Chacune vérifie son propre résultat ; la première qui échoue arrête P6, qui laisse
# ses ressources en place pour le diagnostic et rend le code 1 avec « P6 ÉCHEC — étape … ». Si tout
# réussit : nettoyage de ses seules ressources, « P6 RÉUSSIE », code 0. Le dossier de l'exécution
# (journal p6.log, étapes, sauvegarde source, mesures, rapports) n'est jamais supprimé.
#
# Ressources de l'exécution <id> (défaut p6_<AAMMJJ>_<HHMMSS>), inscrites dans <dossier>/ressources.env :
#   bases bascule_essai_<id>_* (base de mesure, et celles du banc <id>_b), arbre ../court-p6-<id>
#   (marqué), arbre ../court-bascule-essai-<id>_b et branche bascule-essai/<id>_b du banc.
# P6 ne touche ni court_quote_regime_clone ni aucune autre base, ni l'arbre principal, ni epic/E01.
#
# Essais du pilote seulement : P6_SIMULATION=1 remplace les opérations longues (banc, mesures,
# migration) par des substituts rapides, en gardant la création et la suppression réelles des
# ressources et les vrais oracles ; P6_ECHEC_SIMULE=<étape> y fait échouer une étape ; P6_PAUSE=<étape>
# y suspend l'exécution (essai d'interruption). Ces variables sont refusées hors simulation.
# Plan : docs/modele_preuve/BASCULE_REGIME_ETAPE1.md, § 12.

if [ -z "${BASH_VERSION:-}" ]; then echo "ÉCHEC   ce pilote exige bash" >&2; exit 1; fi
set -uo pipefail

OUTIL_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
. "$OUTIL_DIR/bascule_fonctions.sh" || exit 1
. "$OUTIL_DIR/ressources_essai.sh" || exit 1

DEPOT=/Users/Louis-Philippe/Documents/GitHub/court
REFERENCE_VALIDEE=4b53e831144c0d042b397d809f89321e23d557cd   # merge validé sur le clone
ETAT_A=5fa62ed6a076f43b3fcb67f878ef3b8ffc0e785c              # état A : historique + ordre des affidavits
CHEMINS_PERMIS_APRES_REFERENCE='^(docs/|scripts/regime_citations/)'
BRANCHE_INTEGRATION=integration/quote-regime-step1
CIBLE_GIT_DEFAUT=origin/integration/quote-regime-step1
PYTHON=/Users/Louis-Philippe/Documents/GitHub/court/.venv/bin/python
LANG_SERVEUR=en_CA.UTF-8
SAUV_DEFAUT=$HOME/Backups/court/regime_etape1
ESPACE_MIN_KO=$((2 * 1024 * 1024))
ETAPES="preconditions source banc mesure_a migration mesure_b oracle controle_final"

SIMULATION=${P6_SIMULATION:-0}
prefixe_verdict () { [ "$SIMULATION" = 1 ] && echo "SIMULATION — " || true; }

# --- Ressources de l'exécution ------------------------------------------------------------------
definir_ressources () {  # à partir de ID
  ID_BANC="${ID}_b"
  BASE_MESURE="$(prefixe_bases "$ID")_mesure"
  ARBRE_MESURE="/Users/Louis-Philippe/Documents/GitHub/court-p6-$ID"
  ARBRE_BANC="/Users/Louis-Philippe/Documents/GitHub/court-bascule-essai-$ID_BANC"
  BRANCHE_BANC="bascule-essai/$ID_BANC"
}

nettoyer_p6 () {  # seules les ressources de l'exécution ID ; le dossier reste
  local ko=0
  supprimer_bases_possedees "$ID" || ko=1          # couvre aussi les bases du banc (préfixe <id>_b_)
  supprimer_arbre_possede "$DEPOT" "$ARBRE_MESURE" "$ID" || ko=1
  supprimer_arbre_possede "$DEPOT" "$ARBRE_BANC" "$ID_BANC" || ko=1
  supprimer_branche_possedee "$DEPOT" "$BRANCHE_BANC" "$ID_BANC" || ko=1
  [ -z "$(bases_possedees "$ID")" ] && [ ! -e "$ARBRE_MESURE" ] && [ ! -e "$ARBRE_BANC" ] \
    && ! git -C "$DEPOT" show-ref --verify --quiet "refs/heads/$BRANCHE_BANC" || ko=1
  if [ "$ko" -eq 0 ]; then ok "ressources de l'exécution $ID supprimées ; dossier conservé : $DOSSIER"
  else echec "nettoyage incomplet de l'exécution $ID (voir ci-dessus)"; fi
  return $ko
}

ressources_existantes () {
  info "bases de l'exécution : $(bases_possedees "$ID" | tr '\n' ' ')"
  [ -e "$ARBRE_MESURE" ] && info "arbre de mesure : $ARBRE_MESURE"
  [ -e "$ARBRE_BANC" ] && info "arbre du banc : $ARBRE_BANC"
  git -C "$DEPOT" show-ref --verify --quiet "refs/heads/$BRANCHE_BANC" && info "branche du banc : $BRANCHE_BANC"
  return 0
}

# --- Python, environnement explicite (mesure) -------------------------------------------------------
_python_mesure () {  # cwd = arbre de mesure
  ( cd "$ARBRE_MESURE" && env -i HOME="$HOME" USER="${USER:-}" PATH="/usr/bin:/bin:/usr/sbin:/sbin" \
      LANG="$LANG_SERVEUR" PYTHONHASHSEED=0 PYTHONPATH="$OUTIL_DIR" DJANGO_SETTINGS_MODULE=settings_clone_regime \
      REGIME_CLONE_DB="$BASE_MESURE" "$PYTHON" "$@" )
}

# --- Étapes ------------------------------------------------------------------------------------------
e_preconditions () {
  local outil_depot cible_sha hors espace
  outil_depot=$(git -C "$OUTIL_DIR" rev-parse --show-toplevel) || { echec "l'outil n'est pas dans un dépôt Git"; return 1; }
  [ -z "$(git -C "$outil_depot" status --porcelain)" ] || { echec "l'arbre de l'outil ($outil_depot) n'est pas propre"; return 1; }
  [ "$(git -C "$outil_depot" rev-parse --abbrev-ref HEAD)" = "$BRANCHE_INTEGRATION" ] \
    || { echec "l'arbre de l'outil n'est pas sur $BRANCHE_INTEGRATION"; return 1; }
  cible_sha=$(git -C "$outil_depot" rev-parse --verify "$CIBLE_GIT^{commit}") || { echec "cible Git introuvable : $CIBLE_GIT"; return 1; }
  [ "$(git -C "$outil_depot" rev-parse HEAD)" = "$cible_sha" ] || { echec "l'outil ($(git -C "$outil_depot" rev-parse --short HEAD)) n'est pas la version exigée $CIBLE_GIT ($cible_sha)"; return 1; }
  [ "$CIBLE_GIT" = "$CIBLE_GIT_DEFAUT" ] || info "attention : version de l'outil non publiée exigée ($CIBLE_GIT) — valable pour un essai du pilote seulement"
  ok "outil : $outil_depot à $cible_sha ($CIBLE_GIT), propre"
  git -C "$DEPOT" merge-base --is-ancestor "$REFERENCE_VALIDEE" "$cible_sha" || { echec "la cible ne contient pas $REFERENCE_VALIDEE"; return 1; }
  hors=$(git -C "$DEPOT" diff --name-only "$REFERENCE_VALIDEE" "$cible_sha" | grep -Ev "$CHEMINS_PERMIS_APRES_REFERENCE" || true)
  [ -z "$hors" ] || { echec "depuis $REFERENCE_VALIDEE, la cible modifie des fichiers hors docs/ et scripts/regime_citations/ : $hors"; return 1; }
  git -C "$DEPOT" merge-base --is-ancestor "$ETAT_A" "$REFERENCE_VALIDEE" || { echec "état A $ETAT_A absent de l'historique"; return 1; }
  ok "Git : la cible contient la référence $REFERENCE_VALIDEE et n'y ajoute que docs/ et scripts/regime_citations/"
  if git -C "$DEPOT" merge-base --is-ancestor epic/E01-numerotation-concordance "$cible_sha"; then
    ok "avance rapide future : epic/E01 ($(git -C "$DEPOT" rev-parse --short epic/E01-numerotation-concordance)) est ancêtre de la cible"
  else
    echec "epic/E01 n'est plus ancêtre de la cible : refaire le merge d'intégration avant P6"; return 1
  fi
  espace=$(df -k "$SAUV_DEFAUT" | awk 'NR==2 {print $4}')
  [ "$espace" -ge "$ESPACE_MIN_KO" ] || { echec "espace libre insuffisant : $((espace / 1024)) Mio"; return 1; }
  ok "espace libre : $((espace / 1024 / 1024)) Gio"
  verifier_ressources_libres "$ID" "$DEPOT" "arbre:$ARBRE_MESURE" "arbre:$ARBRE_BANC" "branche:$BRANCHE_BANC" || return 1
  _psql -d postgres -c "select datname from pg_database order by 1" | while read -r b; do est_base_possedee "$b" "$ID" || echo "$b"; done > "$DOSSIER/bases_autres_avant.txt"
  git -C "$DEPOT" worktree list --porcelain | sed -n 's/^worktree //p' > "$DOSSIER/arbres_avant.txt"
  git -C "$DEPOT" for-each-ref --format='%(refname:short)' refs/heads > "$DOSSIER/branches_avant.txt"
  ok "inventaire des ressources étrangères : $(wc -l < "$DOSSIER/bases_autres_avant.txt" | tr -d ' ') bases, $(wc -l < "$DOSSIER/arbres_avant.txt" | tr -d ' ') arbres, $(wc -l < "$DOSSIER/branches_avant.txt" | tr -d ' ') branches"
  printf 'ID=%s\nCIBLE_SHA=%s\nSOURCE=%s\n' "$ID" "$cible_sha" "$SOURCE" > "$DOSSIER/ressources.env"
  CIBLE_SHA=$cible_sha
}

e_source () {
  if [ -n "$SOURCE_DONNEE" ]; then
    [ -r "$SOURCE" ] || { echec "sauvegarde source illisible : $SOURCE"; return 1; }
    info "sauvegarde existante, aucune nouvelle sauvegarde de la base réelle"
  else
    [ "$SIMULATION" = 1 ] && { echec "la simulation exige --source (aucune sauvegarde de la base réelle)"; return 1; }
    SOURCE="$DOSSIER/source.dump"
    "$PG_BIN/pg_dump" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -Fc -f "$SOURCE" "$BASE_REELLE" || { echec "pg_dump"; return 1; }
    sed -i '' "s|^SOURCE=.*|SOURCE=$SOURCE|" "$DOSSIER/ressources.env"
  fi
  local nom
  nom=$("$PG_BIN/pg_restore" -l "$SOURCE" | sed -n 's/^;[[:space:]]*dbname: //p') || { echec "pg_restore -l"; return 1; }
  [ "$nom" = "$BASE_REELLE" ] || { echec "la sauvegarde porte la base « $nom », attendu $BASE_REELLE"; return 1; }
  ok "source : $SOURCE (base $nom, $(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$SOURCE"), sha256 $(shasum -a 256 "$SOURCE" | cut -c1-16)…)"
}

e_banc () {
  local bilan
  if [ "$SIMULATION" = 1 ]; then
    echo "=== bilan : 0 réussi(s), 0 raté(s) [substitut de simulation]" > "$DOSSIER/banc.log"
  else
    env -i HOME="$HOME" PATH=/usr/bin:/bin:/usr/sbin:/sbin bash --noprofile --norc "$OUTIL_DIR/essai_bascule.sh" \
      --dossier "$DOSSIER/banc" --id "$ID_BANC" --source "$SOURCE" --vers "$CIBLE_SHA" > "$DOSSIER/banc.log" 2>&1 \
      || { echec "banc d'essai : code non nul ($(grep -cE '^RATÉ' "$DOSSIER/banc.log") raté(s), voir banc.log)"; return 1; }
  fi
  bilan=$(grep -E '^=== bilan' "$DOSSIER/banc.log" | tail -1)
  printf '%s' "$bilan" | grep -q ', 0 raté(s)' || { echec "banc d'essai : bilan absent ou non nul (« $bilan »)"; return 1; }
  ok "banc d'essai : $bilan"
}

e_mesure_a () {
  creer_base_possedee "$BASE_MESURE" "$ID" || return 1
  if [ "$SIMULATION" != 1 ]; then
    "$PG_BIN/pg_restore" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" -d "$BASE_MESURE" --no-owner --exit-on-error "$SOURCE" \
      || { echec "restauration dans $BASE_MESURE"; return 1; }
  fi
  ok "base de mesure : $BASE_MESURE"
  git -C "$DEPOT" worktree add -q --detach "$ARBRE_MESURE" "$ETAT_A" || { echec "arbre de mesure"; return 1; }
  marquer_arbre "$ARBRE_MESURE" "$ID"
  sed "s/^DB_NAME=.*/DB_NAME=$BASE_MESURE/" "$DEPOT/.env" > "$ARBRE_MESURE/.env" && chmod 600 "$ARBRE_MESURE/.env" || return 1
  ok "arbre de mesure : $ARBRE_MESURE à l'état A ($ETAT_A)"
  if [ "$SIMULATION" = 1 ]; then
    "$PYTHON" - "$OUTIL_DIR" "$DOSSIER/A.json" "$ARBRE_MESURE" "$BASE_MESURE" <<'EOF' || return 1
import json, sys
sys.path.insert(0, sys.argv[1]); import projection as P
s = {"/": {"statut": 200}}; sv = {"cause:1:pieces": {"n": 0}}; sec = {"/": {"html": "x"}}
e = {"surfaces": P.empreinte(s), "services": P.empreinte(sv), "secondaire": P.empreinte(sec)}
e["canonique"] = P.empreinte([e["surfaces"], e["services"]])
json.dump({"surfaces": s, "services": sv, "secondaire": sec, "empreintes": e, "liste_des_surfaces": P.empreinte(["/"]),
           "meta": {"arbre": sys.argv[3], "base": sys.argv[4], "surfaces": 1}}, open(sys.argv[2], "w"))
EOF
  else
    _python_mesure "$OUTIL_DIR/empreinte.py" --base "$BASE_MESURE" --sortie "$DOSSIER/A.json" > "$DOSSIER/mesure_a.log" 2>&1 \
      || { echec "mesure A (voir mesure_a.log)"; return 1; }
  fi
  ok "mesure A : $DOSSIER/A.json"
}

e_migration () {
  est_arbre_possede "$DEPOT" "$ARBRE_MESURE" "$ID" || { echec "arbre de mesure : propriété non établie"; return 1; }
  git -C "$ARBRE_MESURE" checkout -q --detach "$CIBLE_SHA" || { echec "passage de l'arbre de mesure à l'état B"; return 1; }
  ok "arbre de mesure à l'état B ($CIBLE_SHA)"
  if [ "$SIMULATION" = 1 ]; then
    printf '%s\n' '{"tables_identiques": 87, "tables_divergentes": [], "tables_nouvelles": [],' \
      '"colonnes_nouvelles": {"email_manager_quote": ["regime"], "pdf_manager_quote": ["regime"]},' \
      '"email_manager_quote : PK et updated_at identiques": true, "email_manager_quote : par régime": {"HERITE": 1},' \
      '"pdf_manager_quote : PK et updated_at identiques": true, "pdf_manager_quote : par régime": {"HERITE": 1},' \
      '"migrations_ajoutees": [["email_manager", "0009_quote_regime"], ["pdf_manager", "0009_quote_regime"]]}' > "$DOSSIER/t11.txt"
  else
    _python_mesure "$OUTIL_DIR/instantane_t11.py" --base "$BASE_MESURE" instantane "$DOSSIER/t11_avant.json" > "$DOSSIER/t11_instantane.log" 2>&1 \
      || { echec "instantané T1.1"; return 1; }
    _python_mesure manage.py migrate > "$DOSSIER/migration.log" 2>&1 || { echec "migration de la base de mesure (voir migration.log)"; return 1; }
    _python_mesure "$OUTIL_DIR/instantane_t11.py" --base "$BASE_MESURE" comparer "$DOSSIER/t11_avant.json" > "$DOSSIER/t11.txt" 2>&1 \
      || { echec "comparaison T1.1"; return 1; }
  fi
  "$PYTHON" "$OUTIL_DIR/verifier_ab.py" t11 "$DOSSIER/t11.txt" | tee "$DOSSIER/oracle_t11.txt" | sed 's/^/    /'
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echec "T1.1 : oracle non conforme"; return 1; }
  ok "T1.1 conforme"
}

e_mesure_b () {
  if [ "$SIMULATION" = 1 ]; then
    cp "$DOSSIER/A.json" "$DOSSIER/B.json" || return 1
  else
    _python_mesure "$OUTIL_DIR/empreinte.py" --base "$BASE_MESURE" --sortie "$DOSSIER/B.json" > "$DOSSIER/mesure_b.log" 2>&1 \
      || { echec "mesure B (voir mesure_b.log)"; return 1; }
  fi
  ok "mesure B : $DOSSIER/B.json"
}

e_oracle () {
  "$PYTHON" "$OUTIL_DIR/verifier_ab.py" ab "$DOSSIER/A.json" "$DOSSIER/B.json" | tee "$DOSSIER/oracle_ab.txt" | sed 's/^/    /'
  [ "${PIPESTATUS[0]}" -eq 0 ] || { echec "oracle A/B : non conforme (voir oracle_ab.txt)"; return 1; }
  ok "oracle A/B conforme"
}

e_controle_final () {
  local r manquantes
  r=$(_psql -d "$BASE_REELLE" -c "select (select count(*) from django_migrations where name='0009_quote_regime')||'|'||(select count(*) from information_schema.columns where column_name='regime' and table_schema='public')") \
    || { echec "lecture de la base réelle"; return 1; }
  [ "$r" = "0|0" ] || { echec "base réelle : $r (migrations 0009 | colonnes regime)"; return 1; }
  ok "base réelle intacte : aucune 0009, aucune colonne regime (lecture seule)"
  manquantes=$(comm -23 <(LC_ALL=C sort "$DOSSIER/bases_autres_avant.txt") <(_psql -d postgres -c "select datname from pg_database" | LC_ALL=C sort))
  [ -z "$manquantes" ] || { echec "bases étrangères disparues : $manquantes"; return 1; }
  manquantes=$(comm -23 <(LC_ALL=C sort "$DOSSIER/arbres_avant.txt") <(git -C "$DEPOT" worktree list --porcelain | sed -n 's/^worktree //p' | LC_ALL=C sort))
  [ -z "$manquantes" ] || { echec "arbres étrangers disparus : $manquantes"; return 1; }
  manquantes=$(comm -23 <(LC_ALL=C sort "$DOSSIER/branches_avant.txt") <(git -C "$DEPOT" for-each-ref --format='%(refname:short)' refs/heads | LC_ALL=C sort))
  [ -z "$manquantes" ] || { echec "branches étrangères disparues : $manquantes"; return 1; }
  ok "aucune base, aucun arbre, aucune branche étrangers touchés"
}

executer_etape () {  # $1 étape
  local e=$1
  echo "debut $e $(date '+%Y-%m-%d %H:%M:%S')" >> "$DOSSIER/etapes.txt"
  echo "--- étape $e"
  if [ "$SIMULATION" = 1 ] && [ "${P6_PAUSE:-}" = "$e" ]; then
    echo "pause $e" >> "$DOSSIER/etapes.txt"; info "pause simulée à l'étape $e"; sleep 600
  fi
  if [ "$SIMULATION" = 1 ] && [ "${P6_ECHEC_SIMULE:-}" = "$e" ]; then
    echec "échec simulé à l'étape $e"; echo "echec $e" >> "$DOSSIER/etapes.txt"; return 1
  fi
  if "e_$e"; then echo "ok $e" >> "$DOSSIER/etapes.txt"; return 0; fi
  echo "echec $e" >> "$DOSSIER/etapes.txt"; return 1
}

c_lancer () {
  local e
  echo "=== $(prefixe_verdict)P6 — exécution $ID, $(date '+%Y-%m-%d %H:%M:%S'), dossier $DOSSIER"
  charger_identifiants || { echo "$(prefixe_verdict)P6 ÉCHEC — identifiants"; return 1; }
  for e in $ETAPES; do
    if ! executer_etape "$e"; then
      echo; echo "$(prefixe_verdict)P6 ÉCHEC — étape $e"
      info "ressources laissées pour le diagnostic :"; ressources_existantes
      info "nettoyage, après examen : bash $OUTIL_DIR/p6.sh nettoyer --dossier $DOSSIER"
      return 1
    fi
  done
  echo "--- nettoyage des ressources de l'exécution"
  nettoyer_p6 || { echo "$(prefixe_verdict)P6 ÉCHEC — nettoyage"; return 1; }
  echo; echo "$(prefixe_verdict)P6 RÉUSSIE"
}

# --- Aiguillage ------------------------------------------------------------------------------------------
commande=${1:-}; [ $# -gt 0 ] && shift
ID=""; DOSSIER=""; SOURCE=""; SOURCE_DONNEE=""; CIBLE_GIT=$CIBLE_GIT_DEFAUT; CIBLE_SHA=""
while [ $# -gt 0 ]; do
  case "$1" in
    --id) ID=$2; shift 2 ;; --dossier) DOSSIER=$2; shift 2 ;;
    --source) SOURCE=$2; SOURCE_DONNEE=oui; shift 2 ;; --cible-git) CIBLE_GIT=$2; shift 2 ;;
    *) echo "option inconnue : $1" >&2; exit 2 ;;
  esac
done
if [ "$SIMULATION" != 1 ] && { [ -n "${P6_ECHEC_SIMULE:-}" ] || [ -n "${P6_PAUSE:-}" ]; }; then
  echo "ÉCHEC   P6_ECHEC_SIMULE et P6_PAUSE n'existent qu'en simulation (P6_SIMULATION=1)" >&2; exit 2
fi

case "$commande" in
  lancer)
    [ -n "$ID" ] || ID="p6_$(date +%y%m%d_%H%M%S)"
    id_valide "$ID" || { echo "identifiant invalide : $ID" >&2; exit 2; }
    [ -n "$DOSSIER" ] || DOSSIER="$SAUV_DEFAUT/$ID"
    [ ! -e "$DOSSIER" ] || { echo "ÉCHEC   le dossier $DOSSIER existe déjà : P6 exige un dossier neuf" >&2; exit 1; }
    mkdir -p "$DOSSIER" && chmod 700 "$DOSSIER" || exit 1
    definir_ressources
    c_lancer 2>&1 | tee -a "$DOSSIER/p6.log"
    exit "${PIPESTATUS[0]}" ;;
  etat|nettoyer)
    [ -n "$DOSSIER" ] && [ -r "$DOSSIER/ressources.env" ] || { echo "ÉCHEC   --dossier <dossier P6> avec ressources.env requis : rien n'est fait" >&2; exit 1; }
    . "$DOSSIER/ressources.env"
    id_valide "$ID" || { echo "ÉCHEC   identifiant invalide dans le manifeste" >&2; exit 1; }
    definir_ressources
    charger_identifiants || exit 1
    if [ "$commande" = etat ]; then
      info "exécution $ID — dossier $DOSSIER"
      sed 's/^/        étapes : /' "$DOSSIER/etapes.txt" 2>/dev/null
      ressources_existantes
      exit 0
    fi
    { echo "=== $(date '+%Y-%m-%d %H:%M:%S') — nettoyage de l'exécution $ID"; nettoyer_p6; } 2>&1 | tee -a "$DOSSIER/p6.log"
    exit "${PIPESTATUS[0]}" ;;
  *)
    echo "usage : bash $0 lancer [--source <dump>] [--id <id>] [--dossier <d>] [--cible-git <réf.>] | etat|nettoyer --dossier <d>" >&2
    exit 2 ;;
esac
