#!/bin/bash
# Lit un ou plusieurs articles d'une loi, depuis le PDF local.
#   scripts/loi/lire.sh C-25.01 249 264
#   scripts/loi/lire.sh I-16 61
# Le texte extrait est mis en cache à côté du PDF (.txt), et le binaire Swift
# est compilé à la première utilisation seulement.
set -euo pipefail
ici="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
racine="$(cd "$ici/../.." && pwd)"
dossier="$racine/legal/analyse/textes_de_loi"

if [ $# -lt 2 ]; then
  echo "usage: $(basename "$0") <code> <no_article> [no_article ...]" >&2
  echo "codes disponibles :" >&2
  ls "$dossier"/*.pdf 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/^/  /' >&2 || echo "  (aucun — voir le README du dossier)" >&2
  exit 2
fi

code="$1"; shift
pdf=$(ls "$dossier/${code}"*.pdf 2>/dev/null | head -1 || true)
if [ -z "$pdf" ]; then
  echo "Aucun PDF pour « $code » dans $dossier" >&2
  echo "Voir $dossier/README.md pour l'obtenir." >&2
  exit 1
fi

bin="$ici/.pdftxt"
if [ ! -x "$bin" ] || [ "$ici/pdftxt.swift" -nt "$bin" ]; then
  swiftc -O "$ici/pdftxt.swift" -o "$bin"
fi

txt="${pdf%.pdf}.txt"
if [ ! -f "$txt" ] || [ "$pdf" -nt "$txt" ]; then
  "$bin" "$pdf" > "$txt"
fi

echo "— source : $(basename "$pdf")"
grep -o -m1 "À jour au[^|]\{0,30\}" "$txt" | head -1 | sed 's/^/— /' || true
echo
python3 "$ici/article.py" "$txt" "$@"
