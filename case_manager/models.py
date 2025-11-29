from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from document_manager.models import Statement
from argument_manager.models import TrameNarrative

# --- LEVEL 1: THE CONTAINER ---
class LegalCase(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# --- LEVEL 2: THE EXHIBIT REGISTRY ---
class ExhibitRegistry(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='exhibits')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    exhibit_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('case', 'content_type', 'object_id')
        ordering = ['exhibit_number']

    def get_label(self):
        return f"P-{self.exhibit_number}"

# --- LEVEL 3: THE ARGUMENT (MASTER) ---
class PerjuryContestation(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='contestations')
    title = models.CharField(max_length=255)
    targeted_statements = models.ManyToManyField(Statement, related_name='contestations')
    supporting_narratives = models.ManyToManyField(TrameNarrative, related_name='supported_contestations')
    final_sec1_declaration = models.TextField(verbose_name="1. Déclaration", blank=True)
    final_sec2_proof = models.TextField(verbose_name="2. Preuve", blank=True)
    final_sec3_mens_rea = models.TextField(verbose_name="3. Mens Rea", blank=True)
    final_sec4_intent = models.TextField(verbose_name="4. Intention", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# --- LEVEL 4: THE AI SUGGESTIONS (DRAFTS) ---
class AISuggestion(models.Model):
    contestation = models.ForeignKey(PerjuryContestation, on_delete=models.CASCADE, related_name='ai_suggestions')
    created_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default="gemini-pro")
    
    content = models.JSONField(default=dict)
    
    raw_response = models.TextField(
        blank=True, 
        null=True, 
        help_text="Réponse brute de l'IA avant traitement JSON"
    )
    
    parsing_success = models.BooleanField(default=False)

    @property
    def suggestion_sec1(self):
        return self.content.get('content_sec1', self.content.get('suggestion_sec1', ''))

    @property
    def suggestion_sec2(self):
        return self.content.get('content_sec2', self.content.get('suggestion_sec2', ''))

    @property
    def suggestion_sec3(self):
        return self.content.get('content_sec3', self.content.get('suggestion_sec3', ''))

    @property
    def suggestion_sec4(self):
        return self.content.get('content_sec4', self.content.get('suggestion_sec4', ''))

    def __str__(self):
        return f"Suggestion du {self.created_at.strftime('%H:%M')}"
