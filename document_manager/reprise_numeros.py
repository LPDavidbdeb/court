"""
Attribuer à chaque paragraphe le numéro que le papier lui donne.

CE QUE CE MODULE REFUSE DE FAIRE. Il ne recopie pas `item`. Sur la demande du
24 juillet 2026, `item` porte le numéro du Markdown de travail, qui diffère du
numéro imprimé pour 47 des 179 paragraphes à numéro simple : le recopier
produirait un acte qui se cite lui-même à côté. Le numéro vient exclusivement de
la colonne imprimée de la table de concordance.

`item` sert d'autre chose : de CLÉ. C'est par lui qu'on retrouve, dans la base,
le paragraphe que la table désigne par son numéro de Markdown. Une clé de
rapprochement n'est pas une preuve : c'est pourquoi le contenu est ensuite
comparé au texte complet archivé, et non au seul incipit de la table.

L'ORDRE EST IMPOSÉ. Le contrôle (`verifier`) précède l'application (`appliquer`),
et l'application le refait dans sa propre transaction. Un appariement vérifié
hier ne dit rien de la base d'aujourd'hui ; sans ce second passage, une
modification concurrente écrirait 198 numéros sur un arbre qui a changé.
"""
import hashlib
import json
import re
import unicodedata

from django.db import transaction

from document_manager.models import LibraryNode, NumberingMode
from document_manager.protection import metadonnees_autorisees


class RattachementRefuse(Exception):
    """Le contrôle préalable a échoué : aucune écriture n'est permise."""


# ---------------------------------------------------------------------------
# NORMALISATION — ce qu'on a le droit d'ignorer en comparant deux textes
#
# Strictement des différences de REPRÉSENTATION du même texte : la base
# conserve le balisage Markdown d'emphase (`**solidairement**`), la table de
# concordance a été produite depuis le rendu, qui ne le porte plus. Les
# apostrophes et guillemets typographiques, les espaces insécables et les
# retours à la ligne relèvent du même ordre.
#
# Aucune de ces règles ne supprime un mot, un chiffre ou une ponctuation de
# sens. Une différence substantielle reste une différence.
# ---------------------------------------------------------------------------

RE_EMPHASE = re.compile(r"\*{1,3}|_{2,3}|`")
RE_ESPACES = re.compile(r"\s+")
RE_LIEN_MD = re.compile(r"\[([^\]]*)\]\([^)]*\)")

REGLES_NORMALISATION = [
    "NFC Unicode",
    "apostrophes et guillemets typographiques ramenés à leurs formes ASCII",
    "marqueurs Markdown d'emphase (*, _, `) retirés",
    "liens Markdown réduits à leur libellé",
    "espaces, insécables et retours à la ligne réduits à une espace simple",
    "espaces de tête et de fin retirés",
]


def normaliser(texte):
    """Le texte réduit à ce qui en fait le sens."""
    t = unicodedata.normalize("NFC", texte or "")
    t = (t.replace("’", "'").replace("‘", "'")
          .replace("“", '"').replace("”", '"')
          .replace(" ", " ").replace(" ", " ")
          .replace("–", "-").replace("—", "-"))
    t = RE_LIEN_MD.sub(r"\1", t)
    t = RE_EMPHASE.sub("", t)
    t = RE_ESPACES.sub(" ", t)
    return t.strip()


def empreinte(texte):
    return hashlib.sha256((texte or "").encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Les sources
# ---------------------------------------------------------------------------

# Dans le Markdown archivé, un paragraphe numéroté commence sa ligne par son
# numéro : « 43. Le 26 juin 2013… », « 22-A. … ». Les paragraphes CITÉS d'actes
# adverses sont en bloc de citation (« > ») et portent leur propre numérotation :
# ils ne commencent donc pas une ligne de cette façon.
RE_PARA_MD = re.compile(r"^(\d+(?:-[A-Z])?)\.\s+(.*)$")


def lire_markdown_archive(chemin):
    """
    `{numero_md: texte_complet}` depuis le Markdown qui a servi à imprimer.

    C'est la pièce qui permet de vérifier le CONTENU. La table de concordance ne
    porte qu'un incipit de 120 caractères : deux paragraphes commençant pareil y
    seraient indiscernables, et un texte tronqué ne démontre pas son intégrité.

    UN PARAGRAPHE EST UNE LIGNE. Ce qui suit — la citation en bloc (« > ») qu'il
    annonce, la formule « tel qu'il appert de la pièce P-20 » qui la referme, le
    chapeau en gras d'une section — sont des blocs distincts, et la base les
    traite comme tels : le nœud du § 123 porte sa phrase d'annonce, pas la
    citation qu'elle introduit. Accumuler les lignes suivantes jusqu'au prochain
    titre ferait donc échouer le contrôle de contenu sur les paragraphes qui
    annoncent une citation, alors que rien ne diverge.
    """
    textes = {}
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            m = RE_PARA_MD.match(ligne.rstrip("\n"))
            if m:
                textes[m.group(1)] = m.group(2).strip()
    return textes


def lire_concordance(chemin):
    """Les 198 lignes de la table : numéro de travail → numéro imprimé."""
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)
    return data


# ---------------------------------------------------------------------------
# T01 — le contrôle préalable
# ---------------------------------------------------------------------------

class Rapport:
    """Le résultat d'un contrôle, et son manifeste."""

    def __init__(self):
        self.lignes_reference = 0
        self.lignes_appariees = 0
        self.noeuds_distincts = 0
        self.manquantes = []        # ligne sans occurrence
        self.ambigues = []          # ligne à plusieurs occurrences possibles
        self.doublons = []          # occurrence visée par plusieurs lignes
        self.oublies = []           # paragraphe admissible non apparié
        self.contenus_incompatibles = []
        self.etrangers = []         # occurrence hors du document visé
        self.conflits = []          # numéro déjà posé, et différent
        self.manifeste = []
        self.ecritures = 0

    @property
    def conforme(self):
        return not (self.manquantes or self.ambigues or self.doublons
                    or self.oublies or self.contenus_incompatibles
                    or self.etrangers or self.conflits)

    def resume(self):
        return {
            'lignes_reference': self.lignes_reference,
            'lignes_appariees': self.lignes_appariees,
            'noeuds_distincts': self.noeuds_distincts,
            'manquantes': len(self.manquantes),
            'ambigues': len(self.ambigues),
            'doublons': len(self.doublons),
            'oublies': len(self.oublies),
            'contenus_incompatibles': len(self.contenus_incompatibles),
            'etrangers': len(self.etrangers),
            'conflits': len(self.conflits),
            'ecritures': self.ecritures,
            'conforme': self.conforme,
        }


# Le périmètre admissible se lit sur la STRUCTURE, pas sur un total à atteindre.
# Un paragraphe du document est admissible s'il est, pour le résolveur, un
# « paragraphe » — ni titre, ni conclusion « C-n », ni mention de clôture, ni
# nœud transparent, ni énumération portant déjà sa puce.
def paragraphes_admissibles(document):
    """`[LibraryNode]` — les occurrences qu'un acte imprimé numérote."""
    from document_manager import numerotation
    return [r.noeud for r in numerotation.resoudre(document)
            if r.genre == "paragraphe"]


def verifier(document, chemin_concordance, chemin_markdown):
    """
    T01 — apparie les lignes de la table aux occurrences, sans rien écrire.

    Rend un `Rapport`. Il est conforme seulement si TOUTES les assertions
    passent : un total de 198 ne dit rien des associations.
    """
    rapport = Rapport()
    data = lire_concordance(chemin_concordance)
    lignes = data['lignes']
    textes_md = lire_markdown_archive(chemin_markdown)
    rapport.lignes_reference = len(lignes)

    admissibles = paragraphes_admissibles(document)
    par_item = {}
    for n in admissibles:
        par_item.setdefault((n.item or "").strip(), []).append(n)

    vus = {}
    for i, ligne in enumerate(lignes):
        cle = str(ligne['numero_md'])
        impr = str(ligne['numero_imprime'])
        candidats = par_item.get(cle, [])

        if not candidats:
            rapport.manquantes.append({'ligne': i, 'numero_md': cle,
                                       'numero_imprime': impr})
            continue
        if len(candidats) > 1:
            rapport.ambigues.append({'ligne': i, 'numero_md': cle,
                                     'noeuds': [n.pk for n in candidats]})
            continue

        noeud = candidats[0]
        if noeud.document_id != document.pk:
            rapport.etrangers.append({'ligne': i, 'noeud': noeud.pk,
                                      'document': noeud.document_id})
            continue
        if noeud.pk in vus:
            rapport.doublons.append({'noeud': noeud.pk,
                                     'lignes': [vus[noeud.pk], i]})
            continue
        vus[noeud.pk] = i

        # --- contrôle du contenu, sur le texte COMPLET du Markdown archivé ---
        texte_base = ""
        obj = noeud.content_object
        if obj is not None:
            texte_base = getattr(obj, 'text', None) or ""
        texte_source = textes_md.get(cle)
        if texte_source is None:
            rapport.contenus_incompatibles.append({
                'ligne': i, 'numero_md': cle, 'noeud': noeud.pk,
                'motif': "paragraphe absent du Markdown archivé",
            })
            continue
        nb, ns = normaliser(texte_base), normaliser(texte_source)
        if nb != ns:
            rapport.contenus_incompatibles.append({
                'ligne': i, 'numero_md': cle, 'noeud': noeud.pk,
                'motif': "texte différent du Markdown archivé",
                'base': nb[:160], 'source': ns[:160],
            })
            continue

        present = (noeud.paragraph_number or "").strip()
        if present and present != impr:
            rapport.conflits.append({'noeud': noeud.pk, 'present': present,
                                     'attendu': impr})

        rapport.lignes_appariees += 1
        rapport.manifeste.append({
            'ligne': i,
            'numero_md': cle,
            'numero_imprime_attendu': impr,
            'suffixe': bool(ligne.get('suffixe')),
            'concorde': bool(ligne.get('concorde')),
            'librarynode_pk': noeud.pk,
            'statement_pk': noeud.object_id,
            'controle_contenu': 'OK',
            'sha256_base': empreinte(nb),
            'sha256_source': empreinte(ns),
        })

    rapport.noeuds_distincts = len(vus)
    rapport.oublies = [{'noeud': n.pk, 'item': n.item}
                       for n in admissibles if n.pk not in vus]
    return rapport


def numeros_attendus(rapport):
    """`{noeud_pk: numero_imprime}` depuis un manifeste conforme."""
    return {m['librarynode_pk']: m['numero_imprime_attendu']
            for m in rapport.manifeste}


# ---------------------------------------------------------------------------
# T03 — l'application
# ---------------------------------------------------------------------------

@transaction.atomic
def appliquer(document, chemin_concordance, chemin_markdown, rapport_prealable=None):
    """
    Écrit les numéros imprimés, après avoir REFAIT le contrôle dans sa transaction.

    Le contrôle préalable passé en argument ne dispense pas du second : il
    atteste d'un état qui peut avoir changé depuis. Ce qui est comparé, ce sont
    les deux manifestes — pas leurs totaux.

    IDEMPOTENTE. Une seconde application ne touche rien, puisque les numéros
    déjà posés égalent ceux attendus.
    """
    rapport = verifier(document, chemin_concordance, chemin_markdown)
    if not rapport.conforme:
        raise RattachementRefuse(
            f"Contrôle de rattachement non conforme : {rapport.resume()}. "
            f"Aucune écriture."
        )
    if rapport_prealable is not None:
        avant = {m['librarynode_pk']: m['numero_imprime_attendu']
                 for m in rapport_prealable.manifeste}
        apres = numeros_attendus(rapport)
        if avant != apres:
            raise RattachementRefuse(
                "L'état des données a changé depuis le contrôle préalable : "
                "l'appariement n'est plus celui qui a été vérifié. Aucune écriture."
            )

    attendus = numeros_attendus(rapport)
    ecrits = 0
    with metadonnees_autorisees():
        for noeud in LibraryNode.objects.filter(pk__in=attendus).select_related('document'):
            valeur = attendus[noeud.pk]
            if (noeud.paragraph_number or "") == valeur:
                continue
            noeud.paragraph_number = valeur
            noeud.save(update_fields=['paragraph_number'])
            ecrits += 1
    rapport.ecritures = ecrits
    return rapport


def controler_apres_reprise(document, chemin_concordance, chemin_markdown):
    """
    T03 — compare les 198 valeurs enregistrées aux 198 valeurs attendues.

    Occurrence par occurrence, pas sur un échantillon : un résultat exact sur
    trois exemples ne dit rien des 195 autres.
    """
    rapport = verifier(document, chemin_concordance, chemin_markdown)
    attendus = numeros_attendus(rapport)
    verifies, ecarts, suffixes, divergents_md = 0, [], 0, 0
    for noeud in LibraryNode.objects.filter(pk__in=attendus):
        attendu = attendus[noeud.pk]
        obtenu = (noeud.paragraph_number or "").strip()
        if obtenu != attendu:
            ecarts.append({'noeud': noeud.pk, 'attendu': attendu, 'obtenu': obtenu})
        else:
            verifies += 1
        if not attendu.isdigit():
            suffixes += 1
        if (noeud.item or "").strip() != attendu:
            divergents_md += 1
    return {
        'controles': len(attendus),
        'verifies': verifies,
        'ecarts': ecarts,
        'suffixes': suffixes,
        'divergents_du_markdown': divergents_md,
        'rapport_appariement': rapport.resume(),
    }


def passer_en_stored(document):
    """Le document lit désormais les numéros conservés."""
    document.numbering_mode = NumberingMode.STORED
    document.save(update_fields=['numbering_mode'])
    return document
