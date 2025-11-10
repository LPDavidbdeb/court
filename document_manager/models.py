from django.db import models
from django.conf import settings
from treebeard.mp_tree import MP_Node
from django.core.exceptions import ValidationError

# --- NEW MODELS FOR REFACTORING ---

class Document(models.Model):
    """
    Represents a single, complete document with its own metadata.
    This table acts as the "library" of all documents.
    """
    title = models.CharField(max_length=555, help_text="The official title of the document.")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authored_documents"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

class Statement(models.Model):
    """
    Represents a single, reusable block of content (an assertion, fact, or paragraph).
    """
    text = models.TextField(blank=True, null=True)
    is_true = models.BooleanField(default=True)
    is_falsifiable = models.BooleanField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_true and self.is_falsifiable is not None:
            raise ValidationError(
                {'is_falsifiable': "A true statement cannot also be marked as falsifiable."}
            )
        super().clean()

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
    statement = models.ForeignKey(
        Statement,
        on_delete=models.SET_NULL,
        related_name="nodes",
        null=True,
        blank=True,
        help_text="The content this node represents."
    )
    item = models.CharField(
        max_length=555,
        help_text="Short name or title for this node in the tree."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Library Node"
        verbose_name_plural = "Library Nodes"

    def __str__(self):
        return f"Node in '{self.document.title}'"
