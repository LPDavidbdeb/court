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

class Document(models.Model, ExhibitableMixin):
    """
    Represents a single, complete document with its own metadata.
    This table acts as the "library" of all documents.
    """
    title = models.CharField(max_length=555, help_text="The official title of the document.")
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
