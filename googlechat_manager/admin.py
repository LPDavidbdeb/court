from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import ChatParticipant, ChatThread, ChatMessage, ChatSubject, SubjectGroup, ChatSequence

class ChatSequenceAdminForm(forms.ModelForm):
    messages = forms.ModelMultipleChoiceField(
        queryset=ChatMessage.objects.all().order_by('-timestamp'),
        widget=FilteredSelectMultiple(
            verbose_name='Messages',
            is_stacked=False
        ),
        help_text="Use the filter to search for messages by content. Hold command/control to select multiple."
    )

    class Meta:
        model = ChatSequence
        fields = ['title', 'subject_group', 'messages']

@admin.register(ChatSequence)
class ChatSequenceAdmin(admin.ModelAdmin):
    form = ChatSequenceAdminForm
    list_display = ('title', 'start_timestamp', 'end_timestamp')
    search_fields = ('title',)
    
    def save_model(self, request, obj, form, change):
        # The save logic is in the model, but we call it here explicitly
        # after the initial save to ensure m2m relations are set.
        super().save_model(request, obj, form, change)
        if obj.pk:
            obj.save() # Calling the model's save() method to update timestamps

# Basic admin registrations for other models for browsability
admin.site.register(ChatParticipant)
admin.site.register(ChatThread)
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'sender', 'text_content')
    list_filter = ('sender', 'thread')
    search_fields = ('text_content',)
    ordering = ('-timestamp',)

admin.site.register(ChatSubject)
admin.site.register(SubjectGroup)