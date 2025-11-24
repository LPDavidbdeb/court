from django.contrib import admin
from .models import ChatParticipant, ChatThread, ChatMessage, ChatSubject, SubjectGroup

@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'original_id', 'protagonist')
    search_fields = ('name', 'email', 'original_id')
    list_filter = ('protagonist',)

@admin.register(ChatThread)
class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ('original_thread_id', 'space_id', 'created_at')
    search_fields = ('original_thread_id', 'space_id')

class SubjectGroupInline(admin.TabularInline):
    model = SubjectGroup.messages.through
    extra = 1

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'sender', 'thread', 'text_content_snippet', 'is_processed_by_ai')
    list_filter = ('is_processed_by_ai', 'sender', 'thread__space_id')
    search_fields = ('text_content', 'sender__name')
    date_hierarchy = 'timestamp'
    inlines = [SubjectGroupInline]

    def text_content_snippet(self, obj):
        return obj.text_content[:50] + '...' if obj.text_content and len(obj.text_content) > 50 else obj.text_content
    text_content_snippet.short_description = 'Text Snippet'

@admin.register(ChatSubject)
class ChatSubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'keywords')

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('subject', 'start_date', 'end_date')
    list_filter = ('subject',)
    filter_horizontal = ('messages',)
