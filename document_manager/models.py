from django.db import models
from treebeard.mp_tree import MP_Node # Import MP_Node for Materialized Path tree

class DocumentNode(MP_Node): # Inherit from MP_Node
    """
    Modèle Django pour représenter un nœud dans une structure de document hiérarchique
    utilisant le concept de "nested sets" via django-treebeard (Materialized Path).
    """
    # treebeard gère automatiquement parent, path, depth, numchild, and siblings_ordering
    # Nous conservons 'parent' comme ForeignKey pour la clarté et l'intégration des formulaires,
    # mais treebeard utilisera son propre 'path' pour la structure.

    # NOUVEAU: Champ pour distinguer le type de nœud (ex: 'library', 'document', 'section', 'paragraph')
    NODE_TYPE_CHOICES = [
        ('library', 'Bibliothèque'),
        ('document', 'Document Principal'),
        ('section', 'Section'),
        ('paragraph', 'Paragraphe / Contenu'),
        ('root', 'Nœud Racine Générique') # Fallback ou pour des racines non-bibliothèque
    ]
    node_type = models.CharField(
        max_length=20,
        choices=NODE_TYPE_CHOICES,
        default='paragraph', # Type par défaut pour les nœuds de contenu
        help_text="Le type de ce nœud (ex: bibliothèque, document, section)."
    )

    item = models.CharField(
        max_length=555,
        help_text="Nom court ou titre du nœud (ex: 'requete', 'chapitre')."
    )
    text = models.TextField(
        blank=True,
        null=True,
        help_text="Le contenu textuel de ce nœud de document."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # treebeard requires a specific Meta class for ordering
    # node_order_by = ['item'] # Order children by 'item' by default

    class Meta(MP_Node.Meta): # Inherit Meta from MP_Node
        verbose_name = "Nœud de Document"
        verbose_name_plural = "Nœuds de Documents"
        # unique_together = ('parent', 'item') # This constraint might be tricky with treebeard's internal path management
                                            # treebeard's path ensures uniqueness within a branch.
                                            # We'll rely on treebeard's internal uniqueness.

    def __str__(self):
        # Use treebeard's get_depth() and get_parent() for consistency
        parent_item = self.get_parent().item if self.get_parent() else "Racine"
        return f"[{self.node_type.upper()}] {self.item} (Profondeur: {self.get_depth()}, Parent: {parent_item})"

    def get_absolute_url(self):
        """
        Retourne l'URL pour accéder à une instance particulière de DocumentNode.
        """
        from django.urls import reverse
        return reverse('document_manager:documentnode_detail', args=[str(self.id)])

    # treebeard provides methods like get_ancestors(), get_children(), get_descendants(), etc.
    # So, custom methods like get_ancestors() and get_level() are no longer needed.

