"""
La restitution : « paragraphe déposé | paragraphe modifié | ancienne cote | nouvelle cote ».

DEUX MODES, ET LEUR DIFFÉRENCE EST TOUT L'OBJET DU MODULE.

    DIAGNOSTIQUE   toujours disponible. Il montre l'état réel, y compris ce qui
                   manque : les liens à établir, les traitements à réexaminer,
                   les appuis périmés, les citations non rattachées. C'est
                   l'outil de travail.

    STRICT         refusé tant qu'une seule des conditions EX01–EX07 n'est pas
                   satisfaite, avec le nom de celle qui bloque. C'est ce qui
                   permet de dire « cette concordance est complète » sans que
                   la phrase soit une opinion.

CE QUI N'EST JAMAIS FABRIQUÉ. Un rapprochement de pièces par produit de
relations — « ce paragraphe vient de celui-là, qui invoquait P-52, donc le
nouveau est appuyé par P-52 ». L'appui d'origine est présenté COMME tel, et
l'appui retenu n'existe que s'il a été confirmé pour le texte courant.
"""
import csv
import io
import json

from django.contrib.contenttypes.models import ContentType

from document_manager import numerotation
from document_manager.models import (
    Correspondance, EtatConfirmation, LibraryNode, RoleExtremite, Statement,
)


# ---------------------------------------------------------------------------
# Les conditions de l'export strict
# ---------------------------------------------------------------------------

LIBELLES_EX = {
    'EX01': "Périmètre et sources identifiés ; contrôles du référent réussis",
    'EX02': "Correspondances et traitements éditoriaux confirmés pour les textes courants",
    'EX03': "Tous les numéros requis sont résolus, aucun suppléé",
    'EX04': "Citations et correspondances de pièces résolues vers les bonnes sources",
    'EX05': "Appuis confirmés pour le texte, la source et la portée courants",
    'EX06': "Suppressions autorisées sans perte ; éléments protégés intacts",
    'EX07': "Aucun conflit ; un seul état de cotation pour tout l'export",
}


class Verdict:
    def __init__(self, code, satisfait, motifs=None):
        self.code = code
        self.satisfait = satisfait
        self.motifs = motifs or []

    def as_dict(self):
        return {'condition': self.code, 'libelle': LIBELLES_EX[self.code],
                'satisfait': self.satisfait, 'motifs': self.motifs[:50],
                'nombre_de_motifs': len(self.motifs)}


def _ex01(source, cible, controle_referent):
    motifs = []
    from document_manager.referent import referent_de
    ref = referent_de(source)
    if ref is None:
        motifs.append(f"Le document source {source.pk} n'est pas déclaré "
                      f"référent historique : il n'est pas protégé.")
    if controle_referent is None:
        motifs.append("Aucun contrôle du référent n'accompagne cet export.")
    elif not controle_referent.get('intact'):
        motifs.append(f"Le contenu du référent a dérivé : {controle_referent}")
    return Verdict('EX01', not motifs, motifs)


def _ex02(source, cible):
    """
    Chaque occurrence admissible a une décision, et elle porte sur le texte actuel.

    `etat_courant()` est ce qui distingue « confirmé » de « confirmé pour une
    version qui n'existe plus ».
    """
    motifs = []
    corrs = list(Correspondance.objects
                 .filter(document_source=source, document_cible=cible)
                 .prefetch_related('extremites__noeud',
                                   'versions_source_examinees',
                                   'versions_cible_examinees'))
    couverts_source, couverts_cible = set(), set()
    for c in corrs:
        etat = c.etat_courant()
        if etat != EtatConfirmation.CONFIRME:
            motifs.append(
                f"Correspondance #{c.pk} ({c.traitement}) : traitement "
                f"éditorial « {etat} ».")
            continue
        for e in c.extremites.all():
            if e.noeud_id is None:
                continue
            (couverts_source if e.role == RoleExtremite.SOURCE
             else couverts_cible).add(e.noeud_id)

    for doc, couverts, cote in ((source, couverts_source, "source"),
                                (cible, couverts_cible, "cible")):
        for r in numerotation.resoudre(doc):
            if r.genre != 'paragraphe':
                continue
            if r.noeud.pk not in couverts:
                motifs.append(
                    f"Occurrence {cote} {r.noeud.pk} (§ {r.numero or '?'}) : "
                    f"aucune décision — « à établir ».")
    return Verdict('EX02', not motifs, motifs)


def _ex03(source, cible):
    motifs = []
    for doc, nom in ((source, "source"), (cible, "cible")):
        for r in numerotation.numeros_manquants(doc):
            motifs.append(
                f"Occurrence {nom} {r.noeud.pk} (item {r.noeud.item!r}) : "
                f"numéro conservé manquant en mode STORED.")
    return Verdict('EX03', not motifs, motifs)


def _ex04(cible, rapport_lock):
    from case_manager import citations
    motifs = [f"Nœud {b['noeud']} — « {b['libelle']} » : {b['motif']}"
              for b in citations.citations_non_resolues(cible)]
    if rapport_lock is None:
        motifs.append("Le contrôle historique des cotes (lock) n'a pas été exécuté.")
    elif not rapport_lock.get('conforme'):
        motifs.append(
            f"Réconciliation lock → bordereau non conforme : "
            f"{len(rapport_lock.get('divergentes', []))} divergence(s), "
            f"{len(rapport_lock.get('manquantes', []))} manque(s).")
    return Verdict('EX04', not motifs, motifs)


def _ex05(cible):
    from case_manager.models import ConfirmationAppui, EtatAppui
    motifs = []
    noeuds = {r.noeud.pk: r for r in numerotation.resoudre(cible)
              if r.genre == 'paragraphe'}
    confirmations = (ConfirmationAppui.objects
                     .filter(noeud_id__in=noeuds)
                     .select_related('version_examinee', 'entree'))
    par_noeud = {}
    for c in confirmations:
        par_noeud.setdefault(c.noeud_id, []).append(c)

    for pk, r in noeuds.items():
        liste = par_noeud.get(pk, [])
        if not liste:
            motifs.append(
                f"Occurrence {pk} (§ {r.numero or '?'}) : aucun appui examiné. "
                f"« Sans appui documenté » est une décision, pas un vide.")
            continue
        for c in liste:
            etat = c.etat_courant()
            if etat in (EtatAppui.A_EXAMINER, EtatAppui.A_REEXAMINER):
                motifs.append(
                    f"Occurrence {pk} — {c.entree.cote if c.entree else 'sans appui'} : "
                    f"état « {etat} ».")
            if etat == EtatAppui.SANS_APPUI and not (c.motif or "").strip():
                motifs.append(
                    f"Occurrence {pk} : « sans appui documenté » sans motif "
                    f"consultable.")
    return Verdict('EX05', not motifs, motifs)


def _ex06(source, cible):
    from document_manager.models import NoeudArchive
    motifs = []
    for a in NoeudArchive.objects.filter(document__in=[source.pk, cible.pk]):
        if not (a.texte or "").strip() and a.statement_pk:
            motifs.append(
                f"Archive {a.pk} (ancien nœud {a.noeud_pk}) : texte non conservé.")
        if not (a.motif or "").strip():
            motifs.append(
                f"Archive {a.pk} (ancien nœud {a.noeud_pk}) : suppression sans "
                f"décision consignée.")
    ct = ContentType.objects.get_for_model(Statement)
    orphelins = (LibraryNode.objects.filter(document__in=[source.pk, cible.pk],
                                            content_type=ct)
                 .exclude(object_id__in=Statement.objects.values_list('pk', flat=True)))
    for n in orphelins:
        motifs.append(f"Nœud {n.pk} désigne un Statement disparu ({n.object_id}).")
    return Verdict('EX06', not motifs, motifs)


def _ex07(empreintes_etat):
    motifs = []
    distinctes = {e for e in empreintes_etat if e}
    if len(distinctes) > 1:
        motifs.append(
            f"Plusieurs états de cotation dans le même export : {sorted(distinctes)}. "
            f"Demande, bordereau et concordance doivent partager le même.")
    return Verdict('EX07', not motifs, motifs)


# ---------------------------------------------------------------------------
# La restitution
# ---------------------------------------------------------------------------

def construire(source, cible, rapport_lock=None, controle_referent=None,
               plancher_annee=None):
    """
    Les lignes de la concordance, et les verdicts EX01–EX07.

    Une scission produit N lignes, une fusion N lignes également : chaque couple
    (antécédent, cible) est une ligne, pour que la table reste lisible sans
    déplier une structure.
    """
    from case_manager import citations
    from case_manager.cotes_concordance import etat_de_cotation, index_cote_cible
    from case_manager.models import ConfirmationAppui
    from document_manager import concordance as svc

    etat = etat_de_cotation(plancher_annee)
    index_cible = index_cote_cible()

    num_source = numerotation.index_par_noeud(source)
    num_cible = numerotation.index_par_noeud(cible)

    corrs = list(Correspondance.objects
                 .filter(document_source=source, document_cible=cible)
                 .prefetch_related('extremites__noeud', 'extremites__archive',
                                   'versions_source_examinees',
                                   'versions_cible_examinees'))

    lignes = []
    vus_source, vus_cible = set(), set()

    for c in corrs:
        exts_s = [e for e in c.extremites.all() if e.role == RoleExtremite.SOURCE]
        exts_c = [e for e in c.extremites.all() if e.role == RoleExtremite.CIBLE]
        etat_courant = c.etat_courant()
        for es in (exts_s or [None]):
            for ec in (exts_c or [None]):
                ns = es.noeud if es else None
                nc = ec.noeud if ec else None
                if ns is not None:
                    vus_source.add(ns.pk)
                if nc is not None:
                    vus_cible.add(nc.pk)
                lignes.append(_ligne(c, es, ec, ns, nc, num_source, num_cible,
                                     index_cible, etat_courant, citations,
                                     ConfirmationAppui, svc))

    # Les occurrences sans aucune décision : « à établir », jamais « ajout » ni
    # « retrait » — l'absence de lien ne décide de rien.
    for doc, vus, role in ((source, vus_source, 'SOURCE'),
                           (cible, vus_cible, 'CIBLE')):
        for r in numerotation.resoudre(doc):
            if r.genre != 'paragraphe' or r.noeud.pk in vus:
                continue
            lignes.append({
                'correspondance': None,
                'traitement': TRAITEMENT_A_ETABLIR,
                'etat_traitement': EtatConfirmation.A_ETABLIR,
                'deplace': None,
                'paragraphe_depose': r.numero if role == 'SOURCE' else None,
                'noeud_source': r.noeud.pk if role == 'SOURCE' else None,
                'paragraphe_modifie': r.numero if role == 'CIBLE' else None,
                'noeud_cible': r.noeud.pk if role == 'CIBLE' else None,
                'ancienne_cote': None, 'nouvelle_cote': None,
                'appuis_origine': [], 'appuis_retenus': [],
                'texte_rendu': None, 'citations_non_resolues': [],
                'motif': "", 'note': "aucune décision enregistrée",
            })

    verdicts = [
        _ex01(source, cible, controle_referent),
        _ex02(source, cible),
        _ex03(source, cible),
        _ex04(cible, rapport_lock),
        _ex05(cible),
        _ex06(source, cible),
        _ex07([etat['empreinte_etat']]),
    ]

    return {
        'perimetre': {
            'document_source': source.pk,
            'titre_source': source.title,
            'mode_source': source.numbering_mode,
            'document_cible': cible.pk,
            'titre_cible': cible.title,
            'mode_cible': cible.numbering_mode,
            'empreinte_etat_cotation': etat['empreinte_etat'],
            'entrees_au_registre': etat['nombre'],
            'controle_lock': (rapport_lock or {}).get('conforme'),
            'controle_referent': controle_referent,
        },
        'lignes': lignes,
        'verdicts': [v.as_dict() for v in verdicts],
        'strict_possible': all(v.satisfait for v in verdicts),
    }


TRAITEMENT_A_ETABLIR = 'A_ETABLIR'


def _ligne(c, es, ec, ns, nc, num_source, num_cible, index_cible, etat_courant,
           citations, ConfirmationAppui, svc):
    appuis_origine, appuis_retenus = [], []
    texte_rendu, non_resolues = None, []

    if nc is not None:
        for a in svc.appuis_dorigine(nc):
            appuis_origine.append({
                'origine': a['origine'],
                'antecedent_noeud': a['antecedent'].pk,
                'cote_de_juillet': a['cote_de_juillet'],
                'cote_citee_au_depot': a['cote_citee'],
                'via_liasse': a['via_liasse'],
                'nouvelle_cote': index_cible.get(a['entree'].pk),
                'entree_pk': a['entree'].pk,
            })
        for conf in (ConfirmationAppui.objects.filter(noeud=nc)
                     .select_related('entree', 'version_examinee')):
            appuis_retenus.append({
                'etat_enregistre': conf.etat,
                'etat_courant': conf.etat_courant(),
                'ancienne_cote': conf.entree.cote if conf.entree else None,
                'nouvelle_cote': (index_cible.get(conf.entree_id)
                                  if conf.entree_id else None),
                'role': conf.role,
                'portee': conf.portee,
                'motif': conf.motif,
                'entree_pk': conf.entree_id,
            })
        rendu = citations.rendre(nc, index_cible)
        texte_rendu = rendu['texte_rendu']
        non_resolues = rendu['non_resolus']

    # Les cotes de la ligne : celle du dépôt vient de l'antécédent, la nouvelle
    # de l'état de cotation courant. Elles ne sont jamais déduites l'une de
    # l'autre par égalité de libellé.
    anciennes = sorted({a['cote_de_juillet'] for a in appuis_origine
                        if a['cote_de_juillet']})
    nouvelles = sorted({a['nouvelle_cote'] for a in appuis_retenus
                        if a['nouvelle_cote']})

    return {
        'correspondance': c.pk,
        'traitement': c.traitement,
        'etat_traitement': etat_courant,
        'deplace': c.deplace,
        'paragraphe_depose': num_source.get(ns.pk) if ns is not None else None,
        'noeud_source': ns.pk if ns is not None else None,
        'source_archivee': (es.archive_id if es and es.noeud_id is None else None),
        'paragraphe_modifie': num_cible.get(nc.pk) if nc is not None else None,
        'noeud_cible': nc.pk if nc is not None else None,
        'cible_archivee': (ec.archive_id if ec and ec.noeud_id is None else None),
        'ancienne_cote': ", ".join(anciennes) or None,
        'nouvelle_cote': ", ".join(nouvelles) or None,
        'appuis_origine': appuis_origine,
        'appuis_retenus': appuis_retenus,
        'texte_rendu': texte_rendu,
        'citations_non_resolues': non_resolues,
        'motif': c.motif,
        'note': c.note,
    }


def en_json(restitution, strict=False):
    """
    Le JSON de la concordance. En mode strict, échoue si une condition manque.

    Le mode diagnostique reste disponible dans tous les cas : c'est lui qui
    permet de savoir CE QUI manque.
    """
    if strict and not restitution['strict_possible']:
        manquantes = [v for v in restitution['verdicts'] if not v['satisfait']]
        raise ExportStrictRefuse(manquantes)
    return json.dumps({**restitution, 'mode': 'STRICT' if strict else 'DIAGNOSTIQUE'},
                      ensure_ascii=False, indent=2)


COLONNES_CSV = [
    'paragraphe_depose', 'paragraphe_modifie', 'ancienne_cote', 'nouvelle_cote',
    'traitement', 'etat_traitement', 'deplace', 'noeud_source', 'noeud_cible',
    'source_archivee', 'cible_archivee', 'appuis_origine', 'appuis_retenus',
    'citations_non_resolues', 'motif', 'note',
]


def en_csv(restitution, strict=False):
    """CSV UTF-8. Accents, guillemets et sauts de ligne passent par le module csv."""
    if strict and not restitution['strict_possible']:
        manquantes = [v for v in restitution['verdicts'] if not v['satisfait']]
        raise ExportStrictRefuse(manquantes)

    tampon = io.StringIO()
    w = csv.DictWriter(tampon, fieldnames=COLONNES_CSV, extrasaction='ignore')
    w.writeheader()
    for l in restitution['lignes']:
        ligne = dict(l)
        ligne['appuis_origine'] = "; ".join(
            f"{a['cote_de_juillet']}→{a['nouvelle_cote']}" for a in l['appuis_origine'])
        ligne['appuis_retenus'] = "; ".join(
            f"{a['ancienne_cote'] or '(ajout)'}→{a['nouvelle_cote']} [{a['etat_courant']}]"
            for a in l['appuis_retenus'])
        ligne['citations_non_resolues'] = "; ".join(
            f"{c['libelle']}:{c['motif']}" for c in l['citations_non_resolues'])
        w.writerow(ligne)
    return tampon.getvalue()


class ExportStrictRefuse(Exception):
    """Une ou plusieurs conditions EX01–EX07 ne sont pas satisfaites."""

    def __init__(self, verdicts_manquants):
        self.verdicts = verdicts_manquants
        noms = ", ".join(v['condition'] for v in verdicts_manquants)
        super().__init__(
            f"Export strict refusé — conditions non satisfaites : {noms}. "
            f"La sortie diagnostique reste disponible."
        )
