from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import LegalCase, PerjuryContestation
from document_manager.models import Statement, LibraryNode
from argument_manager.models import TrameNarrative

class LegalCaseForm(forms.ModelForm):
    class Meta:
        model = LegalCase
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Divorce Proceedings 2025'}),
        }

class PerjuryContestationForm(forms.ModelForm):
    class Meta:
        model = PerjuryContestation
        fields = ['title', 'targeted_statements', 'supporting_narratives']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # We will render these manually in the template, but we keep widgets for validation
            'targeted_statements': forms.CheckboxSelectMultiple,
            'supporting_narratives': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Filter Statements: False & Falsifiable
        statements_queryset = Statement.objects.filter(is_true=False, is_falsifiable=True)
        self.fields['targeted_statements'].queryset = statements_queryset

        # 2. Sort Narratives Alphabetically
        self.fields['supporting_narratives'].queryset = TrameNarrative.objects.all().order_by('titre')

        # 3. PREPARE DATA FOR TEMPLATE: Group Statements by Document
        self.statements_by_doc = {}
        
        if statements_queryset.exists():
            ct = ContentType.objects.get_for_model(Statement)
            # Get all nodes pointing to these statements, prefetching the Document
            nodes = LibraryNode.objects.filter(
                content_type=ct, 
                object_id__in=statements_queryset.values_list('id', flat=True)
            ).select_related('document')

            # Create a map: statement_id -> Document Object
            stmt_to_doc = {node.object_id: node.document for node in nodes}

            # Group them
            for stmt in statements_queryset:
                doc = stmt_to_doc.get(stmt.id)
                doc_title = doc.title if doc else "Documents non classés"
                
                if doc_title not in self.statements_by_doc:
                    self.statements_by_doc[doc_title] = []
                self.statements_by_doc[doc_title].append(stmt)
