from django.db import models
from pgvector.django import VectorField
from django.conf import settings
from treebeard.mp_tree import MP_Node
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from protagonist_manager.models import Protagonist
from django.utils import timezone
from django.urls import reverse
from core.mixins import ExhibitableMixin
from datetime import datetime


# NEW: Add choices for the document source
class DocumentSource(models.TextChoices):
    REPRODUCED = 'REPRODUCED', 'Reproduced (from external file)'
    PRODUCED = 'PRODUCED', 'Produced (created manually)'

class NumberingMode(models.TextChoices):
    """
    Comment un document répond à « quel numéro porte ce paragraphe ? ».

    AUTO   le numéro est RECALCULÉ depuis la structure et le schéma. C'est le
           régime de tous les documents dont la forme est encore en travail :
           insérer un paragraphe renumérote la suite, ce qui est précisément ce
           qu'on attend d'une version qui se rédige.

    STORED le numéro est CONSERVÉ, nœud par nœud. C'est le régime d'un acte déjà
           imprimé : son papier porte 41 là où le fichier de travail portait 43,
           et aucun recalcul ne retrouvera ce 41 — il n'obéit à aucune règle,
           il est le résultat d'un accident de conversion Word figé par le dépôt.

    Le défaut est AUTO, y compris après la migration : un document existant ne
    change pas de comportement parce qu'un champ est apparu.
    """
    AUTO = 'AUTO', 'Calculé depuis la structure et le schéma'
    STORED = 'STORED', 'Conservé sur chaque nœud (numéro imprimé)'


class Document(models.Model, ExhibitableMixin):
    """
    Represents a single, complete document with its own metadata.
    This table acts as the "library" of all documents.
    """
    title = models.CharField(max_length=555, help_text="The official title of the document.")
    cause_origine = models.ForeignKey(
        'cause_manager.Cause', on_delete=models.PROTECT,
        null=True, blank=True, related_name='documents_origine',
        verbose_name="cause d'origine",
        help_text="Cause dans laquelle ce document a été rédigé. Son utilisation comme preuve ailleurs est distincte.",
    )
    author = models.ForeignKey(
        Protagonist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_documents"
    )
    document_original_date = models.DateField(default=timezone.now, null=True, blank=True)
    solemn_declaration = models.TextField(blank=True, help_text="The solemn declaration text for this document.")
    
    # NEW: Add this field
    source_type = models.CharField(
        max_length=20,
        choices=DocumentSource.choices,
        default=DocumentSource.REPRODUCED, # Default to the existing behavior
        help_text="Indicates if the document was imported or created manually."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    embedding = VectorField(dimensions=768, null=True, blank=True)
    file_source = models.FileField(
        upload_to='evidence_files/',  # Changed to 'evidence_files/' for clarity
        null=True,
        blank=True,
        help_text="The original source file (PDF) if this is a REPRODUCED document."
    )

    # QUI DÉCIDE DU NUMÉRO. Le choix entre numérotation conservée et numérotation
    # calculée appartient au DOCUMENT, jamais au Statement — lequel peut être
    # partagé entre plusieurs documents et porterait alors deux numéros
    # contradictoires. Il ne se déduit pas non plus de `source_type` : la demande
    # déposée le 24 juillet 2026 est PRODUCED et doit pourtant afficher les
    # numéros de son papier.
    numbering_mode = models.CharField(
        max_length=10,
        choices=NumberingMode.choices,
        default=NumberingMode.AUTO,
        help_text="AUTO : le numéro se recalcule depuis la structure et le "
                  "schéma. STORED : le numéro lu est celui conservé sur chaque "
                  "nœud (LibraryNode.paragraph_number)."
    )

    # Comment lire la profondeur des nœuds de CE document. Facultatif : un document
    # sans schéma reste parfaitement stockable, il n'est simplement pas numérotable.
    # Le schéma n'est jamais consulté à l'écriture — c'est une lecture, pas une
    # contrainte. Voir SchemaNiveaux.
    schema = models.ForeignKey(
        'SchemaNiveaux',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='documents',
        help_text="Règle d'interprétation des niveaux. Laisser vide tant que la "
                  "forme du document n'est pas arrêtée."
    )

    # BLOC-NOTES, et rien d'autre. Le contexte qu'on a en tête en travaillant un
    # acte — ce qu'il est, pourquoi cette version existe, ce que l'acte adverse
    # fait — et qui se perd entre deux séances faute d'un endroit où le poser.
    #
    # Ce champ n'a pas de structure, et c'est voulu : une note qu'on hésite à
    # classer ne s'écrit pas. Il ne figure dans aucune sortie — ni gabarit, ni
    # formulaire, ni export — et ne doit pas y entrer : ce n'est ni une pièce,
    # ni une analyse de référence, ni un texte destiné à être communiqué.
    notes = models.TextField(
        blank=True, default="",
        help_text="Contexte général sur ce document, à usage d'analyse interne."
    )

    def get_absolute_url(self):
        return reverse('document_manager:document_detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return reverse('core:document_public', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    # --- Exhibitable Interface ---
    def get_exhibit_date(self):
        if self.document_original_date:
            return datetime.combine(self.document_original_date, datetime.min.time())
        return self.created_at

    def get_exhibit_title(self):
        return self.title

    def get_exhibit_type(self):
        return "Document (Général)"

    def get_exhibit_parties(self):
        return f"Auteur: {self.author.get_full_name_with_role()}" if self.author else ""

    def get_exhibit_description(self):
        return self.title

class Statement(models.Model):
    embedding = VectorField(dimensions=768, null=True, blank=True)
    """
    Represents a single, reusable block of content (an assertion, fact, or paragraph).
    """
    text = models.TextField(blank=True, null=True)
    is_true = models.BooleanField(default=True)
    is_falsifiable = models.BooleanField(null=True, blank=True, default=None)
    is_user_created = models.BooleanField(default=False, help_text="True if this statement was created by a user through the editor, False if imported.") # NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (self.text or "")[:80]

    class Meta:
        verbose_name = "Statement"
        verbose_name_plural = "Statements"

class LibraryNode(MP_Node):
    """
    New tree structure model. Each tree within this model corresponds to a single Document.
    This model connects the Document (metadata) and Statement (content) in a hierarchy.
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="nodes",
        help_text="The document this node belongs to."
    )
    item = models.CharField(
        max_length=555,
        help_text="Short name or title for this node in the tree."
    )
    # LE NUMÉRO DU PAPIER — à ne pas confondre avec `item`.
    #
    # `item` porte le numéro du fichier Markdown de travail ; sur la demande du
    # 24 juillet 2026, il diffère du numéro imprimé pour 47 des 179 paragraphes
    # à numéro simple. Recopier l'un dans l'autre ferait citer, sous le même
    # « § », deux paragraphes différents. Les deux champs coexistent donc, et
    # leur divergence est une donnée, non une incohérence à corriger.
    #
    # Le numéro appartient au NŒUD, c'est-à-dire à l'occurrence d'un contenu
    # dans un document, et non au Statement : un même énoncé cité dans deux
    # actes y porte deux numéros.
    #
    # Aucune contrainte d'unicité : une source peut légitimement répéter un
    # numéro, en sauter, ou en suffixer un (« 22-A »).
    paragraph_number = models.CharField(
        max_length=30, blank=True, default="",
        help_text="Numéro porté par ce paragraphe dans le document imprimé "
                  "(« 41 », « 22-A »), sans ponctuation de présentation. "
                  "Vide tant qu'il n'est pas repris d'une source vérifiée."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_evidence = models.BooleanField(default=False)

    # --- ADDED: Generic Relation Fields (nullable for transition) ---
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        null=True, # Allow null for existing rows
        help_text="The model class that this node points to (e.g., Statement or TrameNarrative)."
    )
    object_id = models.PositiveIntegerField(
        null=True, # Allow null for existing rows
        help_text="The primary key of the object this node points to."
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Library Node"
        verbose_name_plural = "Library Nodes"

    def __str__(self):
        return f"Node in '{self.document.title}'"


# ---------------------------------------------------------------------------
# Schémas de niveaux
#
# Un acte de procédure, une déclaration assermentée et un courriel reproduit
# n'ont pas la même grammaire de niveaux : le premier numérote ses paragraphes
# en continu, le dernier n'en numérote aucun. Une règle unique ne peut pas les
# décrire tous, et rien ne dit que les formes à venir ressembleront aux
# actuelles.
#
# Le schéma est donc une LECTURE de la profondeur, pas une contrainte de
# stockage. Il n'est consulté qu'au moment de numéroter ou de rendre ; l'arbre
# s'écrit sans lui. Un document peut donc entrer dans la base sous une forme
# imprévue, être observé, puis recevoir un schéma — ou en inspirer un nouveau.
#
# Corollaire à ne pas perdre de vue : un schéma est une AFFIRMATION sur un
# document, pas une garantie. Si l'arbre s'en écarte, rien ne le signale tant
# qu'on ne lance pas `verifier_schemas`.
# ---------------------------------------------------------------------------

class RoleNiveau(models.TextChoices):
    RACINE = 'RACINE', 'Racine du document'
    SECTION = 'SECTION', 'Section (§)'
    SOUS_SECTION = 'SOUS_SECTION', 'Sous-section'
    THEME = 'THEME', 'Thème'
    SOUS_THEME = 'SOUS_THEME', 'Sous-thème'
    CHAPEAU = 'CHAPEAU', 'Chapeau (annonce ses enfants)'
    PARAGRAPHE = 'PARAGRAPHE', 'Paragraphe numérotable'
    SOUS_ITEM = 'SOUS_ITEM', "Sous-item d'un paragraphe"
    ENUMERATION = 'ENUMERATION', "Élément d'énumération"
    LIBRE = 'LIBRE', 'Contenu libre, non numéroté'


class FormatNumero(models.TextChoices):
    AUCUN = 'AUCUN', 'Pas de numéro'
    DECIMAL = 'DECIMAL', '1, 2, 3'
    ROMAIN_MAJ = 'ROMAIN_MAJ', 'I, II, III'
    LETTRE_MAJ = 'LETTRE_MAJ', 'A, B, C'
    LETTRE_MIN = 'LETTRE_MIN', 'a), b), c)'


class PorteeNumero(models.TextChoices):
    AUCUNE = 'AUCUNE', 'Sans objet'
    DOCUMENT = 'DOCUMENT', 'Continue sur tout le document'
    PARENT = 'PARENT', 'Repart sous chaque parent'


class SchemaNiveaux(models.Model):
    """
    Une grammaire de niveaux, applicable à un ou plusieurs documents.
    """
    nom = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Schéma de niveaux"
        verbose_name_plural = "Schémas de niveaux"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def niveau(self, profondeur):
        return self.niveaux.filter(profondeur=profondeur).first()

    def profondeur_du_role(self, role):
        """Profondeur portant ce rôle, ou None. Sert à répondre à
        « où vivent les paragraphes de ce document ? »."""
        n = self.niveaux.filter(role=role).first()
        return n.profondeur if n else None


class Niveau(models.Model):
    """Ce qu'une profondeur signifie, dans un schéma donné."""
    schema = models.ForeignKey(SchemaNiveaux, on_delete=models.CASCADE,
                               related_name='niveaux')
    profondeur = models.PositiveIntegerField()
    role = models.CharField(max_length=20, choices=RoleNiveau.choices)
    format_numero = models.CharField(max_length=12, choices=FormatNumero.choices,
                                     default=FormatNumero.AUCUN)
    portee = models.CharField(max_length=12, choices=PorteeNumero.choices,
                              default=PorteeNumero.AUCUNE)
    libelle = models.CharField(max_length=120, blank=True,
                               help_text="Nom lisible, pour les rapports.")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['schema', 'profondeur']
        constraints = [
            models.UniqueConstraint(fields=['schema', 'profondeur'],
                                    name='niveau_unique_par_schema'),
        ]

    def __str__(self):
        return f"{self.schema.nom} — profondeur {self.profondeur} : {self.role}"


# ---------------------------------------------------------------------------
# LE RÉFÉRENT HISTORIQUE
#
# Un acte déposé cesse d'être un brouillon : il a été remis au greffe, il est
# cité, et la version qui se rédige après lui se compare à LUI. Rien dans la
# base ne disait cela. `source_type` ne le dit pas — la demande du 24 juillet
# 2026 est PRODUCED, comme les documents de travail. Le titre ne le dit pas, il
# se change. `numbering_mode` ne le dit pas non plus : il décrit comment lire un
# numéro, pas si l'acte est déposé.
#
# D'où une table dont c'est le seul objet. Un document y figure ou n'y figure
# pas ; tant qu'il y figure, les gardes de `protection.py` refusent toute
# écriture sur son contenu.
# ---------------------------------------------------------------------------

class ReferentHistorique(models.Model):
    """
    « Ce document est un acte déposé : son contenu ne se modifie plus. »

    À DISTINGUER DE L'INSTANTANÉ. L'instantané (`InstantaneReferent`) permet de
    CONSTATER une dérive après coup ; il ne l'empêche pas. C'est cette ligne-ci
    qui l'empêche, parce que les gardes la consultent avant d'écrire. Les deux
    sont nécessaires et ne se remplacent pas.
    """
    document = models.OneToOneField(
        Document, on_delete=models.PROTECT, related_name='referent_historique',
        help_text="Le document figé. PROTECT : on ne supprime pas un acte déposé "
                  "en supprimant la ligne qui le protège."
    )
    libelle = models.CharField(
        max_length=200,
        help_text="Ce que cet acte est : « Demande introductive — dépôt du "
                  "24 juillet 2026 »."
    )
    depose_le = models.DateField(
        null=True, blank=True,
        help_text="Date du dépôt au greffe, si l'acte a été déposé."
    )
    source_archivee = models.CharField(
        max_length=500, blank=True,
        help_text="Chemin du fichier qui fait foi du contenu, dans le dépôt gelé."
    )
    source_sha256 = models.CharField(
        max_length=64, blank=True,
        help_text="Empreinte de ce fichier, relevée à l'identification."
    )
    concordance_ref = models.CharField(
        max_length=500, blank=True,
        help_text="Chemin de la table de concordance qui porte les numéros "
                  "imprimés, lorsqu'elle existe."
    )
    concordance_sha256 = models.CharField(max_length=64, blank=True)
    note = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Référent historique"
        verbose_name_plural = "Référents historiques"

    def __str__(self):
        return f"{self.libelle} (document {self.document_id})"


class InstantaneReferent(models.Model):
    """
    L'état d'un référent à un instant donné : textes, arborescence, appuis.

    Sert à répondre « qu'est-ce qui a bougé ? », jamais à empêcher que quelque
    chose bouge. Voir ReferentHistorique.
    """
    referent = models.ForeignKey(
        ReferentHistorique, on_delete=models.CASCADE, related_name='instantanes'
    )
    motif = models.CharField(
        max_length=200,
        help_text="L'opération devant laquelle cet instantané a été pris."
    )
    pris_le = models.DateTimeField(auto_now_add=True)
    empreinte_globale = models.CharField(
        max_length=64,
        help_text="SHA-256 de la concaténation ordonnée des lignes de nœuds. "
                  "Deux instantanés d'empreintes égales décrivent le même état."
    )
    nombre_noeuds = models.PositiveIntegerField(default=0)
    nombre_appuis = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Instantané de référent"
        verbose_name_plural = "Instantanés de référent"
        ordering = ['-pris_le']

    def __str__(self):
        return f"{self.referent.libelle} — {self.pris_le:%Y-%m-%d %H:%M} ({self.motif})"


class InstantaneNoeud(models.Model):
    """Une ligne de l'instantané : ce qu'un nœud portait ce jour-là."""
    instantane = models.ForeignKey(
        InstantaneReferent, on_delete=models.CASCADE, related_name='noeuds'
    )
    noeud_pk = models.PositiveIntegerField()
    path = models.CharField(max_length=255)
    depth = models.PositiveIntegerField()
    item = models.CharField(max_length=555, blank=True)
    paragraph_number = models.CharField(max_length=30, blank=True)
    content_type_id_releve = models.PositiveIntegerField(null=True, blank=True)
    object_id_releve = models.PositiveIntegerField(null=True, blank=True)
    texte = models.TextField(blank=True)
    texte_sha256 = models.CharField(max_length=64, blank=True)
    cotes_appuyantes = models.TextField(
        blank=True,
        help_text="Cotes de juillet invoquées par ce paragraphe, séparées par "
                  "des virgules, dans l'ordre."
    )

    class Meta:
        verbose_name = "Instantané — nœud"
        verbose_name_plural = "Instantané — nœuds"
        ordering = ['instantane', 'path']
        indexes = [models.Index(fields=['instantane', 'noeud_pk'])]


# ---------------------------------------------------------------------------
# LES VERSIONS DE TEXTE
#
# Une confirmation — « cette pièce appuie ce paragraphe », « ce paragraphe est
# conservé tel quel » — porte sur un TEXTE PRÉCIS. Si le texte change, la
# confirmation n'est pas fausse : elle devient historique, et le nouveau texte
# est à réexaminer. Un booléen `confirme` seul ne sait pas dire cela, puisqu'il
# reste vrai après la réécriture.
#
# D'où une table de versions : chaque confirmation pointe la version qu'elle a
# examinée, et l'on compare cette version à l'actuelle pour savoir si elle vaut
# encore.
# ---------------------------------------------------------------------------

class VersionTexte(models.Model):
    """Une version conservée du texte d'un Statement."""
    statement = models.ForeignKey(
        Statement, on_delete=models.CASCADE, related_name='versions'
    )
    texte = models.TextField(blank=True)
    empreinte = models.CharField(max_length=64, db_index=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    motif = models.CharField(
        max_length=200, blank=True,
        help_text="Pourquoi cette version a été conservée."
    )

    class Meta:
        verbose_name = "Version de texte"
        verbose_name_plural = "Versions de texte"
        ordering = ['statement', 'cree_le']
        constraints = [
            models.UniqueConstraint(fields=['statement', 'empreinte'],
                                    name='version_texte_unique_par_empreinte'),
        ]

    def __str__(self):
        return f"Statement {self.statement_id} — {self.empreinte[:12]}"

    @staticmethod
    def empreinte_de(texte):
        import hashlib
        return hashlib.sha256((texte or "").encode('utf-8')).hexdigest()

    @classmethod
    def capter(cls, statement, motif=""):
        """La version courante du texte, créée si elle ne l'est pas déjà."""
        emp = cls.empreinte_de(statement.text)
        obj, _ = cls.objects.get_or_create(
            statement=statement, empreinte=emp,
            defaults={'texte': statement.text or "", 'motif': motif},
        )
        return obj

    @property
    def est_courante(self):
        return self.empreinte == self.empreinte_de(self.statement.text)


# ---------------------------------------------------------------------------
# LA CONCORDANCE DES PARAGRAPHES
#
# POURQUOI PAS UNE CLÉ ÉTRANGÈRE. « Ce paragraphe vient de celui-là » se
# modélise naturellement par un FK vers l'antécédent — et cette modélisation
# perd la FUSION : deux paragraphes réunis en un seul ont deux antécédents, et
# un FK unique en oublie un. La scission, elle, passerait (N cibles pointant la
# même source), mais rien ne dirait que les N forment ensemble le devenir de
# cette source.
#
# D'où un GROUPE : une correspondance réunit n sources et m cibles. 1→1 décrit
# une conservation ou une reformulation, 1→N une scission, N→1 une fusion, 1→0
# un retrait, 0→1 un ajout.
#
# LES LIENS PORTENT SUR LES OCCURRENCES, PAS SUR LES NUMÉROS. Un numéro
# d'affichage change dès qu'on insère un paragraphe au-dessus ; un LibraryNode.pk
# ne change pas. Déplacer une cible met donc à jour son numéro sans toucher au
# lien.
# ---------------------------------------------------------------------------

class TraitementEditorial(models.TextChoices):
    A_ETABLIR = 'A_ETABLIR', 'À établir'
    CONSERVE = 'CONSERVE', 'Conservé'
    DEPLACE = 'DEPLACE', 'Déplacé'
    REFORMULE = 'REFORMULE', 'Reformulé'
    SCINDE = 'SCINDE', 'Scindé'
    FUSIONNE = 'FUSIONNE', 'Fusionné'
    AJOUT = 'AJOUT', 'Ajout'
    RETRAIT = 'RETRAIT', 'Retrait'


class EtatConfirmation(models.TextChoices):
    A_ETABLIR = 'A_ETABLIR', 'À établir'
    CONFIRME = 'CONFIRME', 'Confirmé'
    A_REEXAMINER = 'A_REEXAMINER', 'À réexaminer'


class Correspondance(models.Model):
    """
    Un groupe de transformation entre deux versions d'un même acte.

    DÉPLACÉ **ET** REFORMULÉ. `traitement` nomme la transformation principale,
    `deplace` dit en plus si la position a changé. Les deux informations sont
    indépendantes : les enfermer dans un seul champ à valeurs exclusives
    obligerait à perdre l'une des deux pour un paragraphe réécrit ailleurs.
    """
    document_source = models.ForeignKey(
        Document, on_delete=models.PROTECT, related_name='concordances_source',
        help_text="La version d'origine — l'acte déposé."
    )
    document_cible = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='concordances_cible',
        help_text="La version en cours de rédaction."
    )
    traitement = models.CharField(
        max_length=12, choices=TraitementEditorial.choices,
        default=TraitementEditorial.A_ETABLIR
    )
    deplace = models.BooleanField(
        default=False,
        help_text="La position a changé, indépendamment du traitement du texte."
    )

    # --- confirmation du TRAITEMENT ÉDITORIAL ---
    # Distincte de la confirmation des APPUIS (case_manager.ConfirmationAppui).
    # Reconfirmer les pièces d'un paragraphe ne dit rien de la question « ce
    # texte est-il bien la reformulation de celui-là ? », et réciproquement.
    etat = models.CharField(
        max_length=14, choices=EtatConfirmation.choices,
        default=EtatConfirmation.A_ETABLIR
    )
    versions_source_examinees = models.ManyToManyField(
        VersionTexte, blank=True, related_name='correspondances_source_examinees'
    )
    versions_cible_examinees = models.ManyToManyField(
        VersionTexte, blank=True, related_name='correspondances_cible_examinees'
    )
    decide_le = models.DateTimeField(null=True, blank=True)
    motif = models.TextField(
        blank=True,
        help_text="Pourquoi ce traitement. Obligatoire en pratique pour un "
                  "ajout ou un retrait, qui sont des décisions."
    )
    note = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    maj_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Correspondance de paragraphes"
        verbose_name_plural = "Correspondances de paragraphes"
        ordering = ['document_source', 'document_cible', 'pk']

    def __str__(self):
        return (f"{self.get_traitement_display()} "
                f"[{self.document_source_id}→{self.document_cible_id}] #{self.pk}")

    # -- lecture --
    def noeuds_source(self):
        return [e.noeud for e in self.extremites.filter(role=RoleExtremite.SOURCE)]

    def noeuds_cible(self):
        return [e.noeud for e in self.extremites.filter(role=RoleExtremite.CIBLE)]

    @property
    def est_scission(self):
        return (self.extremites.filter(role=RoleExtremite.SOURCE).count() == 1
                and self.extremites.filter(role=RoleExtremite.CIBLE).count() > 1)

    @property
    def est_fusion(self):
        return (self.extremites.filter(role=RoleExtremite.SOURCE).count() > 1
                and self.extremites.filter(role=RoleExtremite.CIBLE).count() == 1)

    def versions_courantes_examinees(self):
        """
        La confirmation porte-t-elle encore sur les textes actuels ?

        Une confirmation acquise sur V1 cesse de confirmer V2 — elle reste
        consultable, mais le traitement courant redevient à réexaminer.
        """
        for v in list(self.versions_source_examinees.all()) + \
                 list(self.versions_cible_examinees.all()):
            if not v.est_courante:
                return False
        return True

    def etat_courant(self):
        """L'état tenant compte d'une éventuelle réécriture depuis la décision."""
        if self.etat == EtatConfirmation.CONFIRME and \
                not self.versions_courantes_examinees():
            return EtatConfirmation.A_REEXAMINER
        return self.etat


class RoleExtremite(models.TextChoices):
    SOURCE = 'SOURCE', 'Occurrence de la version source'
    CIBLE = 'CIBLE', 'Occurrence de la version cible'


class ExtremiteCorrespondance(models.Model):
    """Une occurrence engagée dans une correspondance, d'un côté ou de l'autre."""
    correspondance = models.ForeignKey(
        Correspondance, on_delete=models.CASCADE, related_name='extremites'
    )
    role = models.CharField(max_length=6, choices=RoleExtremite.choices)
    noeud = models.ForeignKey(
        LibraryNode, on_delete=models.PROTECT, related_name='extremites_concordance',
        null=True, blank=True,
        help_text="L'occurrence visée. PROTECT : une correspondance ne se perd "
                  "pas par la suppression d'un nœud — la suppression autorisée "
                  "archive d'abord et dénoue ensuite (voir NoeudArchive)."
    )
    archive = models.ForeignKey(
        'NoeudArchive', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='extremites',
        help_text="Renseigné lorsque l'occurrence a été supprimée : la "
                  "correspondance reste lisible après coup."
    )
    ordre = models.PositiveIntegerField(
        default=0, help_text="Rang de cette extrémité dans une scission ou fusion."
    )

    class Meta:
        verbose_name = "Extrémité de correspondance"
        verbose_name_plural = "Extrémités de correspondance"
        ordering = ['correspondance', 'role', 'ordre', 'pk']
        constraints = [
            models.UniqueConstraint(
                fields=['correspondance', 'role', 'noeud'],
                name='extremite_unique_par_noeud',
            ),
        ]

    def __str__(self):
        return f"{self.role} — nœud {self.noeud_id or '(archivé)'}"


class NoeudArchive(models.Model):
    """
    Ce qu'une occurrence PRODUCED portait avant sa suppression physique.

    Le cahier autorise à supprimer une occurrence PRODUCED, à condition que la
    concordance reste lisible. Un FK mis à NULL ne suffit pas : il dit qu'il y
    avait quelque chose, pas quoi. Cette table conserve le document, les
    identifiants, le texte et la décision.
    """
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='noeuds_archives'
    )
    noeud_pk = models.PositiveIntegerField(help_text="L'ancien LibraryNode.pk.")
    path = models.CharField(max_length=255, blank=True)
    depth = models.PositiveIntegerField(default=0)
    item = models.CharField(max_length=555, blank=True)
    paragraph_number = models.CharField(max_length=30, blank=True)
    statement_pk = models.PositiveIntegerField(null=True, blank=True)
    statement_supprime = models.BooleanField(
        default=False,
        help_text="True si le Statement lui-même a été supprimé, et non seulement "
                  "cette occurrence."
    )
    texte = models.TextField(blank=True)
    texte_sha256 = models.CharField(max_length=64, blank=True)
    motif = models.TextField(blank=True, help_text="La décision de suppression.")
    supprime_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Nœud archivé"
        verbose_name_plural = "Nœuds archivés"
        ordering = ['-supprime_le']
        indexes = [models.Index(fields=['document', 'noeud_pk'])]

    def __str__(self):
        return f"Nœud {self.noeud_pk} (doc {self.document_id}) — archivé"
