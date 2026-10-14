"""
Les anciennes cotes et les nouvelles : contrôler, puis traduire.

DEUX OPÉRATIONS QU'ON CONFOND FACILEMENT.

    CONTRÔLER   c'est demander « la base dit-elle du dépôt ce que le dépôt en
                dit ? ». La réponse se lit dans `cotes.lock.json`, gelé le
                27 juillet 2026, et nulle part ailleurs. Reconstituer ce
                contrôle depuis la base reviendrait à lui faire attester
                d'elle-même.

    TRADUIRE    c'est calculer, pour chaque pièce, la cote qu'elle porte dans
                l'ordre chronologique cible. C'est un CALCUL, refait à chaque
                lecture, et il n'a pas besoin du lock.

Les deux sont ici parce que la table livrée réunit les deux colonnes. Elles ne
se remplacent pas : une table traduite sans contrôle réussi n'est pas « fidèle
au dépôt », elle est seulement calculée.

CE QUI N'EST JAMAIS FAIT. Aucune écriture corrective silencieuse, ni dans le
lock ni dans le registre. Un écart se diagnostique et se rapporte ; le résoudre
est une décision, pas un effet de bord d'un rapport.
"""
import hashlib
import json
import os
import re

from django.contrib.contenttypes.models import ContentType

from case_manager.cotation_service import cotation_chronologique
from case_manager.models import BordereauDepotJuillet


class LockIndisponible(Exception):
    """Le lock n'est pas accessible : le contrôle historique est BLOQUÉ."""


# ---------------------------------------------------------------------------
# NORMALISATION DES IDENTITÉS
#
# Le lock écrit « Email:118 | Email:21 | … » dans `identites_attendues`, et
# « email:69,68,64 » dans `source_resolue`. La base, elle, désigne une pièce par
# (ContentType, object_id). Comparer des descriptions ou des libellés de cote ne
# prouverait rien : deux pièces peuvent porter la même description.
#
# L'identité retenue est donc le couple (modèle en minuscules, pk), seule chose
# que les deux côtés nomment sans ambiguïté.
# ---------------------------------------------------------------------------

RE_IDENTITE = re.compile(r"^\s*([A-Za-z_]+)\s*:\s*(\d+)\s*$")


def identites_du_lock(entree_lock):
    """`{('email', 118), …}` — ce que cette cote du dépôt réunit."""
    brut = entree_lock.get('identites_attendues') or ""
    out = set()
    for morceau in brut.split("|"):
        m = RE_IDENTITE.match(morceau)
        if m:
            out.add((m.group(1).lower(), int(m.group(2))))
    return out


def identite_de_lentree(entree, cts):
    ct = cts.get(entree.content_type_id)
    if ct is None or entree.object_id is None:
        return None
    return (ct.model.lower(), int(entree.object_id))


def charger_lock(chemin):
    if not chemin or not os.path.exists(chemin):
        raise LockIndisponible(
            f"cotes.lock.json introuvable : {chemin!r}. Le contrôle historique "
            f"est BLOQUÉ — il ne se reconstitue pas depuis la base."
        )
    with open(chemin, 'rb') as f:
        brut = f.read()
    data = json.loads(brut.decode('utf-8'))
    return data, hashlib.sha256(brut).hexdigest()



# ---------------------------------------------------------------------------
# ÉQUIVALENCES DE CONTENANT
#
# Le lock nomme « photo:4558 » ; le registre nomme « photodocument:14 », qui ne
# contient que cette photo-là. La matière est la même, désignée à deux niveaux :
# l'image, et la pièce d'un seul feuillet qui la présente.
#
# CE N'EST PAS UNE CONCORDANCE POUR AUTANT. Les tenir d'emblée pour égales
# reviendrait à décider, dans un rapport, une question d'identité documentaire —
# exactement la correction silencieuse que le cahier interdit. Elles sont donc
# rapportées à part, avec la preuve du contenant, et ne comptent comme
# concordantes que si l'appelant l'accepte explicitement.
#
# LES DEUX SENS SONT EXIGÉS. Que le conteneur ne porte que cette photo ne
# suffit pas : si la photo appartenait aussi à un second PhotoDocument, la
# désignation du lock ne tomberait plus sur un contenant unique et « la même
# matière désignée à deux niveaux » cesserait d'être vrai. La règle métier —
# une Photo appartient au plus à un PhotoDocument — n'est pas imposée par le
# schéma, qui est un ManyToManyField des deux côtés ; elle se vérifie donc à
# chaque contrôle, sur l'état examiné, et ne se présume jamais.
# ---------------------------------------------------------------------------

def _equivalence_contenant(attendues, observees):
    """
    `(True, preuve)` si les identités ne diffèrent que par le niveau de
    désignation : un conteneur d'un seul élément contre cet élément.
    """
    manque = attendues - observees
    en_trop = observees - attendues
    if not manque or not en_trop:
        return False, None
    paires = []
    restant_manque, restant_trop = set(manque), set(en_trop)
    for modele_c, pk_c in sorted(en_trop):
        if modele_c != 'photodocument':
            continue
        try:
            from photos.models import PhotoDocument
            doc = PhotoDocument.objects.filter(pk=pk_c).first()
        except Exception:                        # pragma: no cover
            doc = None
        if doc is None:
            continue
        contenues = set(doc.photos.values_list('pk', flat=True))
        vises = {pk for modele, pk in restant_manque if modele == 'photo'}
        couvertes = contenues & vises
        if not contenues or contenues != couvertes:
            continue
        # Le sens réciproque : aucune de ces photos n'appartient ailleurs.
        autres = sorted(set(
            PhotoDocument.objects.filter(photos__pk__in=contenues)
            .exclude(pk=pk_c).values_list('pk', flat=True)))
        if autres:
            continue
        paires.append({
            'au_registre': f"photodocument:{pk_c}",
            'au_lock': sorted(f"photo:{pk}" for pk in sorted(contenues)),
            'preuve': f"PhotoDocument {pk_c} ne contient que "
                      f"{sorted(contenues)}",
            'preuve_reciproque': f"photo(s) {sorted(contenues)} : aucun autre "
                                 f"PhotoDocument ne les contient",
            'contrainte_du_schema': "ManyToManyField — la réciproque est "
                                    "vérifiée sur l'état examiné, non garantie "
                                    "par le schéma",
        })
        restant_trop.discard((modele_c, pk_c))
        restant_manque -= {('photo', pk) for pk in contenues}
    if paires and not restant_manque and not restant_trop:
        return True, paires
    return False, None


# ---------------------------------------------------------------------------
# C13 / T24 — le contrôle historique
# ---------------------------------------------------------------------------

def reconcilier(chemin_lock, accepter_equivalences_contenant=False):
    """
    Compare les associations cote → source du lock à celles du registre.

    PAS LIGNE À LIGNE. Le lock porte 106 cotes PRINCIPALES ; le registre en
    détaille 334, liasses développées en sous-cotes. Une liasse du lock
    (« P-43 », 19 identités) répond donc à 19 lignes de registre portant
    `cote_racine = "P-43"`. Exiger une égalité de cardinal ferait échouer le
    contrôle sur une donnée parfaitement cohérente.

    Les pièces versées après le dépôt (`cote = NULL`) ne sont pas des manques du
    lock : elles n'ont jamais eu de cote de juillet.
    """
    data, sha = charger_lock(chemin_lock)
    cts = {ct.id: ct for ct in ContentType.objects.all()}

    registre = list(BordereauDepotJuillet.objects.all())
    par_racine = {}
    for e in registre:
        if e.cote_racine:
            par_racine.setdefault(e.cote_racine, []).append(e)

    rapport = {
        'lock': chemin_lock,
        'lock_sha256': sha,
        'lock_schema': data.get('schema'),
        'lock_genere_le': data.get('genere_le'),
        'cotes_au_lock': len(data.get('cotes', [])),
        'entrees_au_registre': len(registre),
        'ajouts_sans_cote_de_juillet': sum(1 for e in registre if e.cote is None),
        'normalisation': "identité = (modèle en minuscules, pk)",
        'controlees': 0,
        'concordantes': 0,
        'manquantes': [],       # cote du lock absente du registre
        'divergentes': [],      # mêmes cotes, sources différentes
        'ambigues': [],         # identité du lock illisible
        'equivalences_contenant': [],   # même matière, niveau de désignation différent
        'equivalences_acceptees': bool(accepter_equivalences_contenant),
        'manifeste': [],
    }

    for entree_lock in data.get('cotes', []):
        cote = entree_lock['cote']
        attendues = identites_du_lock(entree_lock)
        rapport['controlees'] += 1

        lignes = par_racine.get(cote, [])
        if not lignes:
            rapport['manquantes'].append({
                'cote': cote, 'description': entree_lock.get('description', '')[:70],
                'identites_attendues': sorted(attendues),
            })
            continue

        if not attendues:
            rapport['ambigues'].append({
                'cote': cote,
                'motif': "identites_attendues illisible ou vide dans le lock",
                'brut': entree_lock.get('identites_attendues', ''),
            })
            continue

        observees = set()
        for e in lignes:
            ident = identite_de_lentree(e, cts)
            if ident is None:
                rapport['ambigues'].append({
                    'cote': cote, 'entree': e.pk,
                    'motif': "ligne de registre sans source résolue",
                })
            else:
                observees.add(ident)

        manque = attendues - observees
        en_trop = observees - attendues

        equivalente, preuve = (False, None)
        if manque or en_trop:
            equivalente, preuve = _equivalence_contenant(attendues, observees)

        ligne_manifeste = {
            'cote': cote,
            'lignes_de_registre': len(lignes),
            'identites_attendues': sorted(attendues),
            'identites_observees': sorted(observees),
            'manquantes_au_registre': sorted(manque),
            'au_registre_hors_lock': sorted(en_trop),
            'verdict': ('CONCORDE' if not (manque or en_trop)
                        else ('EQUIVALENCE_CONTENANT' if equivalente else 'DIVERGE')),
        }
        if equivalente:
            ligne_manifeste['equivalences'] = preuve
        rapport['manifeste'].append(ligne_manifeste)

        if not (manque or en_trop):
            rapport['concordantes'] += 1
        elif equivalente:
            rapport['equivalences_contenant'].append(ligne_manifeste)
            if accepter_equivalences_contenant:
                rapport['concordantes'] += 1
            else:
                rapport['divergentes'].append(ligne_manifeste)
        else:
            rapport['divergentes'].append(ligne_manifeste)

    rapport['conforme'] = not (rapport['manquantes'] or rapport['divergentes']
                               or rapport['ambigues'])
    return rapport


# ---------------------------------------------------------------------------
# C15 / T24 — la table autonome des cotes
# ---------------------------------------------------------------------------

def etat_de_cotation(plancher_annee=None):
    """
    L'ordre chronologique courant, et de quoi l'identifier.

    L'EMPREINTE EST CE QUI REND UN EXPORT COMPARABLE. Les cotes se recalculent à
    chaque lecture ; une pièce ajoutée ou datée décale toute la suite. Un export
    qui ne dirait pas de quel état il provient serait incomparable au suivant, et
    deux tables du même dossier se contrediraient sans qu'on sache laquelle est
    périmée.
    """
    ordre = cotation_chronologique(plancher_annee)
    h = hashlib.sha256()
    lignes = []
    for rang, entree, dt, groupe in ordre:
        cote_cible = f"P-{rang}"
        lignes.append({
            'rang': rang,
            'nouvelle_cote': cote_cible,
            'ancienne_cote': entree.cote,
            'cote_racine_juillet': entree.cote_racine,
            'sous_rang_juillet': entree.sous_rang,
            'cote_pont': entree.cote_pont,
            'entree_pk': entree.pk,
            'source_type': entree.source_type,
            'object_id': entree.object_id,
            'groupe': groupe,
            'horodatage': dt.isoformat() if dt else None,
            'atemporel': entree.atemporel,
            'description': entree.description or "",
            'sans_cote_de_juillet': entree.cote is None,
        })
        h.update(f"{rang}|{entree.pk}|{entree.cote}|{dt}\n".encode('utf-8'))
    return {
        'lignes': lignes,
        'empreinte_etat': h.hexdigest(),
        'nombre': len(lignes),
        'plancher_annee': plancher_annee,
    }


def table_des_cotes(plancher_annee=None, rapport_lock=None):
    """
    « ancienne cote | nouvelle cote | source identifiable ».

    Livrable à part entière : elle ne dépend pas de la concordance des
    paragraphes et se produit avant que la réécriture soit finie.
    """
    etat = etat_de_cotation(plancher_annee)
    cts = {ct.id: ct for ct in ContentType.objects.all()}
    par_pk = {e.pk: e for e in BordereauDepotJuillet.objects.all()}

    lignes = []
    for l in etat['lignes']:
        e = par_pk[l['entree_pk']]
        ct = cts.get(e.content_type_id)
        lignes.append({
            'ancienne_cote': l['ancienne_cote'] or "(sans cote de juillet)",
            'nouvelle_cote': l['nouvelle_cote'],
            'source': (f"{ct.model}:{e.object_id}" if ct and e.object_id
                       else "(source non résolue)"),
            'source_modele': ct.model if ct else "",
            'source_pk': e.object_id,
            'cote_racine_juillet': l['cote_racine_juillet'],
            'sous_rang_juillet': l['sous_rang_juillet'],
            'liasse_de_juillet': bool(l['sous_rang_juillet']),
            'groupe_de_classement': l['groupe'],
            'horodatage': l['horodatage'],
            'sans_cote_de_juillet': l['sans_cote_de_juillet'],
            'description': l['description'][:120],
            'entree_pk': l['entree_pk'],
        })

    fidelite = "NON CONTRÔLÉE"
    if rapport_lock is not None:
        fidelite = "CONFORME AU LOCK" if rapport_lock.get('conforme') \
            else "DIVERGENCES — voir le rapport de réconciliation"

    return {
        'empreinte_etat': etat['empreinte_etat'],
        'nombre': etat['nombre'],
        'fidelite_historique': fidelite,
        'controle_lock': rapport_lock,
        'lignes': lignes,
    }


def dispersion_des_liasses(table):
    """
    Où chaque composant d'une liasse de juillet atterrit dans l'ordre cible.

    Une liasse est une commodité du dépôt : dix-neuf courriels sous « P-43 ».
    L'ordre chronologique la DISPERSE, puisque ses pièces n'ont pas la même
    date. La table doit le montrer, faute de quoi « P-43 » paraîtrait avoir
    disparu.
    """
    par_racine = {}
    for l in table['lignes']:
        racine = l['cote_racine_juillet']
        if not racine:
            continue
        par_racine.setdefault(racine, []).append(l)

    out = []
    for racine, lignes in sorted(par_racine.items()):
        if len(lignes) < 2:
            continue
        cibles = sorted(int(l['nouvelle_cote'].split('-')[1]) for l in lignes)
        out.append({
            'cote_racine_juillet': racine,
            'composants': len(lignes),
            'nouvelles_cotes': [l['nouvelle_cote'] for l in
                                sorted(lignes, key=lambda x: int(
                                    x['nouvelle_cote'].split('-')[1]))],
            'dispersee': (cibles[-1] - cibles[0]) >= len(cibles),
            'detail': [
                {'ancienne_cote': l['ancienne_cote'],
                 'nouvelle_cote': l['nouvelle_cote'],
                 'source': l['source'],
                 'horodatage': l['horodatage']}
                for l in sorted(lignes,
                                key=lambda x: int(x['nouvelle_cote'].split('-')[1]))
            ],
        })
    return out


def index_cote_cible():
    """`{entree_pk: "P-13"}` — pour résoudre les citations au rendu."""
    return {l['entree_pk']: l['nouvelle_cote']
            for l in etat_de_cotation()['lignes']}
