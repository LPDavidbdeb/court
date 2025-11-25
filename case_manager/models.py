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
    """
    Ensures that Email #104 is always 'P-5' throughout the entire LegalCase,
    no matter how many times it appears in different contestations.
    """
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='exhibits')
    
    # Generic Relation to ANY evidence type (Email, PDF, Photo, Event)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # The permanent P-Number (e.g., 10 for 'P-10')
    exhibit_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('case', 'content_type', 'object_id') # One ID per document per case
        ordering = ['exhibit_number']

    def get_label(self):
        return f"P-{self.exhibit_number}"

# --- LEVEL 3: THE ARGUMENT (MASTER) ---
class PerjuryContestation(models.Model):
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='contestations')
    title = models.CharField(max_length=255)
    
    # The Inputs
    targeted_statements = models.ManyToManyField(Statement, related_name='contestations')
    supporting_narratives = models.ManyToManyField(TrameNarrative, related_name='supported_contestations')

    # The FINAL Curated Content (The "Real" answers)
    final_sec1_declaration = models.TextField(verbose_name="1. Déclaration", blank=True)
    final_sec2_proof = models.TextField(verbose_name="2. Preuve", blank=True)
    final_sec3_mens_rea = models.TextField(verbose_name="3. Mens Rea", blank=True)
    final_sec4_intent = models.TextField(verbose_name="4. Intention", blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# --- LEVEL 4: THE AI SUGGESTIONS (DRAFTS) ---
class AISuggestion(models.Model):
    """
    Stores a specific 'Run' from the AI. 
    The user can look at 3 different suggestions and copy/paste bits into the Parent Contestation.
    """
    contestation = models.ForeignKey(PerjuryContestation, on_delete=models.CASCADE, related_name='ai_suggestions')
    created_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default="gemini-pro")

    # The Suggestions
    suggestion_sec1 = models.TextField(blank=True)
    suggestion_sec2 = models.TextField(blank=True)
    suggestion_sec3 = models.TextField(blank=True)
    suggestion_sec4 = models.TextField(blank=True)

    def __str__(self):
        return f"Suggestion du {self.created_at.strftime('%H:%M')}"
