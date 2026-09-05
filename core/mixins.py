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


class ChampsEditables:
    """
    Déclare les champs de texte qu'une page peut écrire en place.

    La clé est le nom du champ, la valeur le nom de son horodatage — ou `None`
    quand le modèle n'en porte pas. `core.views.ajax_maj_champ` ne lit que
    cela : rien n'est modifiable depuis une page sans être nommé ici.

    Pourquoi sur le modèle plutôt que dans une liste centrale : la route porte
    le couple modèle + champ, mais une liste par nom de champ ouvrirait tous
    les homonymes du projet. `note` existe aussi sur `RattachementAxe` et sur
    `AppuiFait`, `description` sur `Axe` et sur `SchemaNiveaux` — aucun de ces
    quatre n'est l'objet d'une page. Déclaré ici, ce qui est exposé se lit à
    côté du champ exposé, et un champ ajouté demain ne devient pas éditable
    par accident parce qu'il porte un nom déjà connu ailleurs.
    """

    champs_editables = {}
