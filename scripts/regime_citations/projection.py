"""
La projection canonique : ce que l'empreinte retient d'une réponse ou d'un service.

Module pur (aucun import de Django) : les règles se testent seules
(`test_projection.py`).

TROIS SORTES DE COLLECTIONS, À NE JAMAIS CONFONDRE

- SÉQUENCE SÉMANTIQUE : l'ordre influence le rendu, une numérotation, une cote,
  une structure sérialisée ou un résultat métier. Conservée telle quelle,
  doublons compris, et comparée rang par rang. Exemples : les marqueurs de
  citation dans l'ordre du document, les pièces produites dans l'ordre de leur
  numérotation, les sous-cotes d'un affidavit.
- COLLECTION NON ORDONNÉE : seule la composition compte. Triée et dédoublonnée
  avant le hachage. Exemple : les PK des citations instanciées pendant une
  requête — l'oracle de l'isolation demande si une PK apparaît, pas à quel rang
  la base l'a rendue.
- COLLECTION NON CONSOMMÉE par la surface mesurée : présente dans le contexte,
  mais ni la vue ni le gabarit ne l'a évaluée. Sa présence et son contenu sont
  contrôlés (dans l'ensemble) ; l'ordre accidentel que la base lui donne quand
  l'instrument l'évalue n'est pas un comportement de la surface, et n'entre dans
  aucune séquence. Cas d'origine : `email_quotes` de la fiche de protagoniste.

`[12, 14, 18]` et `[14, 12, 18]` sont la même valeur comme ensemble, deux
valeurs distinctes comme séquence. Chaque champ de la projection est déclaré
dans l'une de ces sortes (README, « La projection ») ; aucun n'est trié « par
défaut ».

LES NORMALISATIONS AUTORISÉES — trois, aucune autre sans justification écrite
dans le README avant usage :

1. les jetons CSRF (64 caractères alphanumériques, tirés à chaque rendu) ;
2. l'anti-cache `?v=<time.time()>` du visionneur PDF (`argument_manager`,
   `ajax_get_pdf_viewer`) ;
3. la PK d'un objet temporaire créé pendant la requête et désigné par la
   redirection (`manage-perjury` crée un `PerjuryArgument` ; la transaction est
   annulée mais la séquence PostgreSQL avance quand même). Seule une PK qui
   n'existe plus après l'annulation est remplacée ; une PK existante est gardée.
"""
import hashlib
import json
import re


# --------------------------------------------------------------------------
# Ensembles et séquences
# --------------------------------------------------------------------------
def _cle(valeur):
    return canon(valeur)


def ensemble(valeurs):
    """Une collection dont seule la présence compte : triée, sans doublons."""
    vues = {}
    for v in valeurs:
        vues[_cle(v)] = v
    return [vues[k] for k in sorted(vues)]


def sequence(valeurs):
    """Une collection dont l'ordre est observable : telle quelle."""
    return list(valeurs)


def canon(obj):
    """JSON canonique. Les clés d'un objet n'ont pas d'ordre (triées) ; les listes
    gardent le leur : c'est à l'appelant de dire si une liste est un ensemble."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str, separators=(",", ":"))


def empreinte(obj):
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Normalisations
# --------------------------------------------------------------------------
CSRF = re.compile(r"[A-Za-z0-9]{64}")
ANTI_CACHE = re.compile(r"\?v=\d+")
# Redirections vers un objet que la requête peut créer (normalisation 3).
REDIRECTIONS_TEMPORAIRES = {
    "argument_manager.PerjuryArgument": re.compile(r"^/arguments/perjury-argument/(\d+)/update/$"),
}


def normaliser_texte(texte):
    """Normalisations 1 et 2."""
    return ANTI_CACHE.sub("?v=#", CSRF.sub("<csrf>", texte))


def normaliser_location(location, existe):
    """Normalisation 3. `existe(label_modele, pk)` dit si l'objet existe encore
    après l'annulation de la requête."""
    if not location:
        return None
    for label, motif in REDIRECTIONS_TEMPORAIRES.items():
        m = motif.match(location)
        if m and not existe(label, int(m.group(1))):
            return location[:m.start(1)] + "<temporaire>" + location[m.end(1):]
    return location


# --------------------------------------------------------------------------
# Marqueurs de citation dans un rendu (SÉQUENCE, ordre du document)
# --------------------------------------------------------------------------
MARQUEURS = re.compile(
    r"/emails/quote/(?P<eq>\d+)/"
    r"|/pdfs/quote/(?P<pq>\d+)/"
    r"|data-quote-id=\\?[\"'](?P<dq>\d+)\\?[\"'](?:\s+data-source=\\?[\"'](?P<ds>\w+))?"
    r"|data-evidence-id=\"(?P<ei>\d+)\"\s*data-evidence-type=\"(?P<et>\w+)\""
)


def marqueurs(texte):
    """Les citations désignées par le rendu, dans l'ordre du document :
    liens vers une fiche de citation, `data-quote-id` (avec sa source),
    boutons de preuve `data-evidence-id` / `data-evidence-type`."""
    sortie = []
    for m in MARQUEURS.finditer(texte):
        if m.group("eq"):
            sortie.append(f"email_quote:{m.group('eq')}")
        elif m.group("pq"):
            sortie.append(f"pdf_quote:{m.group('pq')}")
        elif m.group("dq"):
            sortie.append(f"data_quote:{m.group('ds') or '?'}:{m.group('dq')}")
        else:
            sortie.append(f"evidence:{m.group('et')}:{m.group('ei')}")
    return sequence(sortie)


# --------------------------------------------------------------------------
# Comparaison lisible
# --------------------------------------------------------------------------
def ecart(a, b):
    """Où deux projections divergent : {champ: description}."""
    if not isinstance(a, dict) or not isinstance(b, dict):
        return {} if a == b else {"valeur": _decrire(a, b)}
    out = {}
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            out[k] = _decrire(a.get(k), b.get(k))
    return out


def _decrire(a, b):
    if isinstance(a, list) and isinstance(b, list):
        if sorted(map(canon, a)) == sorted(map(canon, b)):
            i = next(i for i, (x, y) in enumerate(zip(a, b)) if x != y)
            return f"mêmes éléments, ordre différent dès le rang {i} : {a[i:i + 4]} … / {b[i:i + 4]} …"
        en_moins = [x for x in a if x not in b][:5]
        en_plus = [x for x in b if x not in a][:5]
        return f"{len(a)} → {len(b)} éléments ; en moins {en_moins} ; en plus {en_plus}"
    return f"{str(a)[:160]} → {str(b)[:160]}"
