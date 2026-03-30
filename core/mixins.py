from django.utils import timezone
from datetime import datetime

class ExhibitableMixin:
    """
    Mixin to provide a standard interface for objects that can be 
    registered as exhibits in a legal case.
    """
    
    def get_exhibit_date(self):
        """Returns a datetime or date object for sorting exhibits."""
        if hasattr(self, 'created_at'):
            return self.created_at
        return timezone.now()

    def get_exhibit_title(self):
        """Returns the main title for the exhibit list."""
        return str(self)

    def get_exhibit_type(self):
        """Returns a string representing the category (e.g., 'Email', 'Photo')."""
        return self._meta.verbose_name

    def get_exhibit_parties(self):
        """Returns a string describing the parties involved (From/To, Author)."""
        return ""

    def get_exhibit_description(self):
        """Returns a detailed description for the exhibit list."""
        return ""
    
    def get_exhibit_public_url(self):
        """Returns the public URL for viewing the file, if applicable."""
        if hasattr(self, 'get_public_url'):
            return self.get_public_url()
        return None
