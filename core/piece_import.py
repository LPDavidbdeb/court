"""
Noyau d'import du corpus de fichiers pièce vers la base.

Un fichier pièce est une analyse écrite sur une source qui existe déjà en base.
L'importer, c'est le convertir en HTML et le ranger sur l'objet qu'il décrit,
pour qu'il se relise et se modifie là où vivent les preuves plutôt qu'à côté.

LE REGISTRE

Ce module ne connaît aucune famille de fichiers : il ne connaît que le registre.
Une entrée dit, pour une famille, quel motif de nom de fichier la désigne, quel
modèle elle vise, et si un fichier de cette famille peut être importé.

Le registre sert à deux choses, et c'est ce qui justifie sa forme. Il route un
fichier vers son objet ; et il résout un lien vers ce même objet. Intégrer une
nouvelle famille est donc une entrée de plus — jamais une modification du
noyau — et cette entrée fait aussitôt s'allumer tous les liens du corpus qui
visaient cette famille.

`accueille=False` marque les familles dont les fichiers ne sont pas importés :
elles servent quand même à résoudre les liens, parce qu'un lien ne demande pas
que la famille soit importée, seulement que l'objet visé existe en base.
"""

import re
from dataclasses import dataclass
from urllib.parse import unquote

from django.apps import apps


@dataclass(frozen=True)
class Adaptateur:
    nom: str
    motif: str          # regex sur le nom de fichier, avec un groupe nommé 'pk'
    modele: str         # 'application.Modele'
    accueille: bool     # un fichier de cette famille peut-il être importé ?
    remonte: str = ''   # relation à remonter pour atteindre l'unité citable
    contenu: str = ''   # relation inverse, pour vérifier que la remontée est fidèle

    def correspond(self, nom_fichier):
        return re.fullmatch(self.motif, nom_fichier)

    def objet(self, correspondance, pour_import=False):
        """
        L'objet visé, remonté jusqu'à l'unité citable quand il y a lieu.

        Une photo est un fichier ; ce qui se cite, c'est le document qui la
        contient et qui porte la cote — la photo 4551 est le fichier de la
        pièce P-4, et un renvoi doit mener à P-4, pas à une image isolée. La
        remontée n'a lieu que si le fichier appartient effectivement à un
        document : une photo qui n'en a aucun reste elle-même l'unité
        disponible, et un renvoi vers elle vaut mieux qu'un renvoi vers rien.

        `pour_import` distingue les deux usages, parce qu'ils ne tolèrent pas la
        même approximation. Pour un LIEN, remonter est toujours juste : le
        lecteur doit arriver sur la pièce cotée, quel que soit le nombre de
        photos qu'elle rassemble. Pour un IMPORT, non : ranger l'analyse d'une
        photo dans le champ d'un document qui en contient cinq ferait passer ce
        qui vaut pour une page pour ce qui vaut pour l'ensemble. La remontée
        n'est donc admise à l'import que si le document se réduit à cette
        photo — sinon le fichier reste hors périmètre, et la commande le dit.
        """
        modele = apps.get_model(self.modele)
        objet = modele.objects.filter(pk=int(correspondance.group('pk'))).first()
        if objet is None or not self.remonte:
            return objet
        parent = getattr(objet, self.remonte).first()
        if parent is None:
            return objet
        if pour_import and getattr(parent, self.contenu).count() > 1:
            return None
        return parent


# L'ordre compte : le motif du fil accepte n'importe quel suffixe et avalerait
# les fichiers de courriel s'il passait avant eux.
REGISTRE = (
    Adaptateur("courriel d'un fil", r'piece_thread-\d+_email-(?P<pk>\d+)\.md',
               'email_manager.Email', accueille=True),
    Adaptateur("plusieurs courriels d'un fil", r'piece_thread-(?P<pk>\d+)_emails-[\d-]+\.md',
               'email_manager.EmailThread', accueille=True),
    Adaptateur("fil", r'piece_thread-(?P<pk>\d+)(?:_[^.]*)?\.md',
               'email_manager.EmailThread', accueille=True),

    Adaptateur("document PDF", r'piece_pdf-(?P<pk>\d+)\.md',
               'pdf_manager.PDFDocument', accueille=True),
    Adaptateur("document photo", r'piece_photodoc-(?P<pk>\d+)\.md',
               'photos.PhotoDocument', accueille=True),

    # Familles non importées : présentes pour que les liens qui les visent
    # résolvent dès aujourd'hui.
    #
    # `piece_photo-*` en fait partie et n'en sortira pas : une photo n'est pas
    # une unité de preuve. Ce qui se verse au dossier est un évènement ou un
    # document photo ; une image seule n'est qu'un fichier de l'un des deux.
    # L'adaptateur reste pour qu'un renvoi écrit sous cette forme mène quand
    # même au document — jamais à l'image — mais aucun fichier de cette famille
    # n'est importé. Les deux qui existaient ont été renommés à la convention
    # du document qu'ils décrivaient.
    Adaptateur("photo", r'piece_photo-(?P<pk>\d+)\.md',
               'photos.Photo', accueille=False,
               remonte='photo_documents', contenu='photos'),
    Adaptateur("séquence de chat", r'piece_chatsequence-(?P<pk>\d+)\.md',
               'googlechat_manager.ChatSequence', accueille=False),
    Adaptateur("évènement", r'piece_event-(?P<pk>\d+)\.md',
               'events.Event', accueille=False),
)


def resoudre(nom_fichier, pour_import=False):
    """
    (adaptateur, objet) pour ce nom de fichier, ou (adaptateur, None) si la
    famille est connue mais l'objet introuvable ou inadmissible à l'import, ou
    (None, None) si aucune famille ne reconnaît ce nom.
    """
    for adaptateur in REGISTRE:
        correspondance = adaptateur.correspond(nom_fichier)
        if correspondance:
            return adaptateur, adaptateur.objet(correspondance, pour_import=pour_import)
    return None, None


# --- conversion -----------------------------------------------------------

def _markdown():
    import mistune
    # Pas de greffon `url` : il transforme en lien `mailto:` toute adresse
    # écrite en clair, et le corpus en cite beaucoup — celle d'une avocate dans
    # un en-tête de pièce n'est pas un lien, c'est une donnée du document.
    # Convertir ne doit rien ajouter que le fichier ne dise.
    return mistune.create_markdown(
        escape=False,
        plugins=['table', 'strikethrough', 'footnotes'],
    )


RE_LIEN = re.compile(r'<a href="(?P<cible>[^"]+)"[^>]*>(?P<texte>.*?)</a>', re.S)


def reecrire_liens(html):
    """
    Remplace chaque lien vers un fichier du corpus par l'URL de l'objet visé.

    Un lien entre deux fichiers ne meurt pas à la conversion, il meurt au
    déplacement : il désignait un voisin sur le disque, et la base n'a pas de
    voisins. Résolu, il redevient une adresse de l'application.

    Non résolu, il n'est ni supprimé ni laissé en href mort : le texte reste
    visible et le nom du fichier visé le suit entre parenthèses, pour que
    « ici il y avait un renvoi vers ce fichier » ne disparaisse jamais en
    silence. Retourne (html, résolus, morts).
    """
    resolus, morts = [], []

    def remplacer(m):
        cible = m.group('cible')
        texte = m.group('texte')
        if '.md' not in cible:
            return m.group(0)                        # lien externe, laissé tel quel
        fichier = unquote(cible.split('#')[0].split('/')[-1])
        ancre = '#' + cible.split('#')[1] if '#' in cible else ''
        _, objet = resoudre(fichier)
        if objet is not None:
            resolus.append(fichier)
            return f'<a href="{objet.get_absolute_url()}{ancre}">{texte}</a>'
        morts.append(fichier)
        return (f'{texte} <span class="lien-corpus" title="renvoi non résolu">'
                f'({fichier})</span>')

    return RE_LIEN.sub(remplacer, html), resolus, morts


def convertir(markdown_source):
    """Markdown → HTML, liens réécrits. Retourne (html, résolus, morts)."""
    html = _markdown()(markdown_source)
    return reecrire_liens(html)


# --- contrôle de fidélité -------------------------------------------------

def _sans_code(source):
    """Le texte hors blocs de code : ce que le convertisseur voit comme structure."""
    return re.sub(r'^```.*?^```', '', source, flags=re.M | re.S)


def compter_markdown(source):
    """
    Les structures du fichier, comptées avant conversion.

    `liens_corpus` ne compte que les renvois explicites vers un autre fichier du
    corpus — ceux dont la survie est en jeu. Les liens automatiques du markdown
    (`<adresse@exemple.com>` entre chevrons, dont les en-têtes de pièce sont
    pleins) sont délibérément hors du compte : le convertisseur n'en rend
    qu'une partie, selon qu'ils tombent ou non dans du code ou du texte
    échappé, et aucune expression régulière ne reproduit cette règle. Les
    compter reviendrait à mesurer l'écart entre mon compteur et l'analyseur, pas
    la fidélité de la conversion.
    """
    texte = _sans_code(source)
    lignes_tableau = re.findall(r'^\|.*\|\s*$', texte, re.M)
    separateurs = [l for l in lignes_tableau if re.fullmatch(r'\|[\s:|-]+\|\s*', l)]
    return {
        'titres': len(re.findall(r'^#{1,6} ', texte, re.M)),
        'lignes_tableau': len(lignes_tableau) - len(separateurs),
        'liens_corpus': len(re.findall(r'\[[^\]]+\]\([^)]*\.md[^)]*\)', texte)),
        'lignes_citation': len(re.findall(r'^> ', texte, re.M)),
    }


def compter_html(html, morts):
    """
    Les mêmes structures après conversion.

    `liens_corpus` additionne les renvois réécrits en URL et ceux laissés en
    texte : chaque lien du corpus doit se retrouver sous l'une des deux formes,
    et le total doit être celui du fichier. C'est l'invariant qui garantit
    qu'aucun renvoi ne s'est évaporé.
    """
    reecrits = len(re.findall(r'<a href="/', html))
    return {
        'titres': len(re.findall(r'<h[1-6][ >]', html)),
        'lignes_tableau': len(re.findall(r'<tr[ >]', html)),
        'liens_corpus': reecrits + len(morts),
        'lignes_citation': len(re.findall(r'<blockquote[ >]', html)),
    }
