# Propriété des ressources temporaires d'une exécution (banc d'essai, P6).
#
# Sourcée après bascule_fonctions.sh (_psql, PG_*). Compatible bash 3.2.
#
# Une exécution a un identifiant ID (minuscules, chiffres, « _ »). Elle ne possède que :
#   - les bases dont le nom est exactement « bascule_essai_<ID> » ou commence par « bascule_essai_<ID>_ »
#     (comparaison exacte de préfixe, sans motif LIKE : « _ » n'y est pas un joker) ;
#   - les arbres de travail qui portent la marque .bascule-essai-proprietaire contenant ID et que Git
#     liste comme arbres du dépôt ;
#   - les branches dont le nom est exactement « bascule-essai/<ID> ».
# Avant toute création, l'absence de ces ressources est vérifiée ; rien n'est supprimé ni réinitialisé
# sans que sa propriété soit établie. Les dossiers de journaux et de résultats ne sont jamais supprimés.

MARQUE_ARBRE=.bascule-essai-proprietaire

id_valide () {  # $1 identifiant
  printf '%s' "$1" | grep -Eq '^[a-z0-9]+(_[a-z0-9]+)*$' && [ "${#1}" -le 24 ]
}

prefixe_bases () { echo "bascule_essai_$1"; }   # $1 ID

bases_possedees () {  # $1 ID -> noms des bases possédées, une par ligne
  local p; p=$(prefixe_bases "$1")
  _psql -d postgres -c "select datname from pg_database where datname='$p' or left(datname, length('$p') + 1)='${p}_' order by 1"
}

est_base_possedee () {  # $1 nom, $2 ID
  local p; p=$(prefixe_bases "$2")
  [ "$1" = "$p" ] || case "$1" in "${p}_"*) true ;; *) false ;; esac
}

creer_base_possedee () {  # $1 nom, $2 ID : refuse un nom hors de l'exécution ou une base existante
  est_base_possedee "$1" "$2" || { echec "la base $1 n'appartient pas à l'exécution $2"; return 1; }
  base_existe "$1" && { echec "la base $1 existe déjà : création refusée"; return 1; }
  "$PG_BIN/createdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" "$1" || return 1
  _psql -d postgres -c "comment on database \"$1\" is 'bascule-essai:$2'" > /dev/null
}

supprimer_bases_possedees () {  # $1 ID : termine les sessions et supprime ses seules bases
  local b n=0
  for b in $(bases_possedees "$1"); do
    est_base_possedee "$b" "$1" || { echec "propriété de $b non établie : laissée"; continue; }
    _psql -d postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where datname='$b' and pid<>pg_backend_pid()" > /dev/null
    "$PG_BIN/dropdb" -h "$PG_HOTE" -p "$PG_PORT" -U "$PG_UTILISATEUR" "$b" && { info "base supprimée : $b"; n=$((n + 1)); } \
      || { echec "suppression de $b"; return 1; }
  done
  info "bases supprimées pour l'exécution $1 : $n"
}

marquer_arbre () { printf '%s\n' "$2" > "$1/$MARQUE_ARBRE"; }   # $1 arbre, $2 ID

est_arbre_possede () {  # $1 dépôt, $2 arbre, $3 ID
  [ -f "$2/$MARQUE_ARBRE" ] && [ "$(cat "$2/$MARQUE_ARBRE")" = "$3" ] \
    && git -C "$1" worktree list --porcelain | grep -qxF "worktree $2"
}

supprimer_arbre_possede () {  # $1 dépôt, $2 arbre, $3 ID
  if [ ! -e "$2" ]; then git -C "$1" worktree prune; return 0; fi
  est_arbre_possede "$1" "$2" "$3" || { echec "l'arbre $2 n'appartient pas à l'exécution $3 : laissé"; return 1; }
  git -C "$1" worktree remove --force "$2" && info "arbre supprimé : $2"
}

supprimer_branche_possedee () {  # $1 dépôt, $2 branche, $3 ID
  [ "$2" = "bascule-essai/$3" ] || { echec "la branche $2 n'appartient pas à l'exécution $3 : laissée"; return 1; }
  git -C "$1" show-ref --verify --quiet "refs/heads/$2" || return 0
  git -C "$1" branch -q -D "$2" && info "branche supprimée : $2"
}

verifier_ressources_libres () {  # $1 ID, $2 dépôt, puis « arbre:<chemin> » ou « branche:<nom> »… : rien ne doit exister
  local id=$1 depot=$2 r ko=0; shift 2
  [ -z "$(bases_possedees "$id")" ] || { echec "des bases de l'exécution $id existent déjà : $(bases_possedees "$id" | tr '\n' ' ')"; ko=1; }
  for r in "$@"; do
    case "$r" in
      arbre:*) [ ! -e "${r#arbre:}" ] || { echec "le chemin ${r#arbre:} existe déjà"; ko=1; } ;;
      branche:*) ! git -C "$depot" show-ref --verify --quiet "refs/heads/${r#branche:}" || { echec "la branche ${r#branche:} existe déjà"; ko=1; } ;;
    esac
  done
  [ "$ko" -eq 0 ] && ok "aucune ressource préexistante pour l'exécution $id"
  return $ko
}
