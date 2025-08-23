from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.exceptions import ValidationError

class DocumentNode(MP_Node):
    # ... (existing fields) ...
    NODE_TYPE_CHOICES = [
        ('library', 'Bibliothèque'),
        ('document', 'Document Principal'),
        ('section', 'Section'),
        ('paragraph', 'Paragraphe / Contenu'),
        ('root', 'Nœud Racine Générique')
    ]
    node_type = models.CharField(
        max_length=20,
        choices=NODE_TYPE_CHOICES,
        default='paragraph',
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

    # --- NEW FIELDS ---
    is_true = models.BooleanField(
        default=True,
        help_text="Indique si l'affirmation est considérée comme vraie."
    )
    is_falsifiable = models.BooleanField(
        null=True,  # Allows for NULL (unknown) state in the database
        blank=True, # Allows the field to be blank in forms
        default=None,
        help_text="Indique si une affirmation (qui est fausse) est falsifiable. Non applicable si l'affirmation est vraie."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Enforce model-level validation before saving."""
        # This is the business logic you requested.
        if self.is_true and self.is_falsifiable is not None:
            raise ValidationError(
                {'is_falsifiable': "Une affirmation vraie ne peut pas être marquée comme falsifiable ou non-falsifiable."}
            )
        super().clean()

    def save(self, *args, **kwargs):
        """Override save to enforce business logic."""
        self.full_clean() # Run model validation
        super().save(*args, **kwargs)

    class Meta(MP_Node.Meta):
        verbose_name = "Nœud de Document"
        verbose_name_plural = "Nœuds de Documents"

    def __str__(self):
        parent_item = self.get_parent().item if self.get_parent() else "Racine"
        return f"[{self.node_type.upper()}] {self.item} (Parent: {parent_item})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('document_manager:documentnode_detail', args=[str(self.id)])
