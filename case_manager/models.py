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

    # === NOUVEAUX CHAMPS POUR LA POLICE ===
    police_report_data = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Contenu structuré de la plainte criminelle (Art 131)."
    )
    
    police_report_date = models.DateTimeField(null=True, blank=True)

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


class ProducedExhibit(models.Model):
    """
    A temporary, ordered representation of exhibits for a specific case.
    This table is wiped and recreated on demand ('recalculated').
    It serves as the source of truth for the 'Final Report' (Word) and AI Analysis.
    """
    case = models.ForeignKey(LegalCase, on_delete=models.CASCADE, related_name='produced_exhibits')
    
    # Sorting & Hierarchy
    sort_order = models.PositiveIntegerField(db_index=True, help_text="Integer for strict sorting (1, 2, 3...)")
    label = models.CharField(max_length=20, help_text="The display label (e.g., 'P-1', 'P-1-1')")
    
    # Content Content (The calculated columns)
    exhibit_type = models.CharField(max_length=100, blank=True, help_text="The user-friendly type of the exhibit (e.g., 'Courriel', 'Photo')")
    date_display = models.CharField(max_length=255, blank=True, help_text="The string to show in the Date column")
    description = models.TextField(help_text="The calculated description (Subject, Explanation, or Quote)")
    parties = models.CharField(max_length=500, blank=True, help_text="Calculated author/recipient information.")
    
    # NEW FIELD
    public_url = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="URL to the public view of the source document."
    )

    # Link back to the actual evidence (for AI context lookup)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Produced Exhibit"

    def __str__(self):
        return f"{self.label} - {self.date_display}"


class BordereauDepotJuillet(models.Model):
    """
    Constat de la cotation du dépôt du 24 juillet 2026.

    Cette table ENREGISTRE une correspondance pièce <-> cote telle qu'elle a été
    déposée. Elle ne la calcule pas et ne doit jamais être recalculée : c'est ce
    qui la sépare d'ExhibitRegistry, lequel attribue les numéros par ordre
    chronologique et supprime les entrées qui ne sont plus adossées à une trame
    (voir exhibit_service.refresh_case_exhibits).

    CE QUI EST IMMUABLE, c'est l'ASSOCIATION (modèle + pk) -> cote de juillet.
    Elle a été déposée, elle ne se corrige pas, et c'est elle qui permet de
    traduire l'ancienne cotation vers la nouvelle.

    CE QUI NE L'EST PAS, c'est le contenu de la table. Le dossier continue de
    vivre : des pièces sont versées après le dépôt, invoquées par les axes
    d'argumentation. Elles entrent ici avec `cote = NULL` — elles n'ont jamais
    reçu de cote en juillet, et ajouter ces lignes ne modifie aucune des
    correspondances existantes.

    La cotation chronologique (`traduire_cotes`) porte donc sur TOUTE la table :
    une pièce ajoutée prend son rang à sa date comme n'importe quelle autre, et
    la colonne `cote` reste le témoin de ce qui figurait au dépôt.

    ADRESSABILITÉ DES LIASSES — c'est ce que la table apporte sur le bordereau.
    Une liasse y occupe une seule ligne (« P-43 | Liasse de 19 courriels ») et
    ses sous-cotes P-43.1 à P-43.19 n'existent que dans la prose : aucun
    paragraphe ne peut donc les citer. Ici chaque pièce reçoit sa ligne :

        cote = "P-43.7"   cote_racine = "P-43"   rang = 43   sous_rang = 7

    Une pièce simple porte cote == cote_racine et sous_rang = None.
    """

    # --- la cote ---
    # NULL = pièce versée après le dépôt : elle n'a jamais reçu de cote en
    # juillet. Postgres traite chaque NULL comme distinct sous une contrainte
    # d'unicité, donc plusieurs pièces peuvent coexister sans cote.
    cote = models.CharField(
        max_length=20, unique=True, db_index=True, null=True, blank=True,
        help_text="Cote de juillet : « P-43 » ou « P-43.7 ». NULL si non déposée."
    )
    cote_racine = models.CharField(
        max_length=20, db_index=True, null=True, blank=True,
        help_text="Cote de la pièce mère : « P-43 », pour P-43.7 comme pour P-43."
    )
    rang = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Partie numérique de la cote racine, pour le tri (43)."
    )
    sous_rang = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Rang dans la liasse (7), ou NULL si la pièce est simple."
    )

    # --- la pièce visée ---
    # PROTECT plutôt que CASCADE : la disparition d'un ContentType ne doit pas
    # emporter un constat de dépôt.
    content_type = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, null=True, blank=True,
        help_text="Modèle de la pièce : Email, EmailThread, PDFDocument, Event, "
                  "Photo, PhotoDocument, ChatSequence, Document."
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # --- ce que le bordereau dit, mot pour mot ---
    source_type = models.CharField(
        max_length=30, blank=True,
        help_text="Type tel que résolu depuis le bordereau : email, thread, pdf, "
                  "event, photo, photodoc, chatsequence, document."
    )
    source_ref = models.CharField(
        max_length=500, blank=True,
        help_text="Colonne « Fichier d'appui » du bordereau, brute."
    )
    date_libelle = models.CharField(
        max_length=200, blank=True,
        help_text="Colonne « Date », telle quelle : « 16 juin–16 août 2013 »."
    )
    description = models.TextField(
        blank=True,
        help_text="Colonne « Pièce » du bordereau déposé."
    )

    # --- nature de la pièce ---
    atemporel = models.BooleanField(
        default=False,
        help_text="La pièce n'a pas de date PAR NATURE — capture d'un fait "
                  "permanent, grille horaire, définition. À distinguer d'une "
                  "date simplement manquante : celle-ci s'ajoutera, l'autre "
                  "jamais. Une pièce atemporelle se range en fin de cotation "
                  "chronologique sans qu'on la signale comme à corriger."
    )

    # --- qualité de l'import ---
    resolu = models.BooleanField(
        default=False,
        help_text="True si content_object a pu être rattaché à un objet existant."
    )
    note = models.TextField(
        blank=True,
        help_text="Motif de non-résolution ou remarque d'import."
    )

    importe_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bordereau — dépôt du 24 juillet 2026"
        verbose_name_plural = "Bordereau — dépôt du 24 juillet 2026"
        ordering = ['rang', 'sous_rang']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['cote_racine']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['cote_racine', 'sous_rang'],
                name='bordereau_juillet_souscote_unique',
            ),
        ]

    def __str__(self):
        return f"{self.cote} — {self.description[:60]}"

    @property
    def est_liasse(self):
        """La pièce appartient-elle à une liasse ?"""
        return self.sous_rang is not None

    def pieces_de_la_liasse(self):
        """Les autres pièces partageant la même cote racine."""
        return BordereauDepotJuillet.objects.filter(cote_racine=self.cote_racine)


class AppuiDepotJuillet(models.Model):
    """
    « Ce paragraphe de la demande de juillet est appuyé par cette pièce. »

    La demande déposée le 24 juillet 2026 allègue des faits ; chaque fait occupe
    un paragraphe (art. 99 C.p.c.) et se trouve appuyé par 0, 1 ou N pièces du
    bordereau. Cette relation est PLAIDÉE — elle figure en toutes lettres dans
    le texte, « tel qu'il appert de la pièce P-52 » — mais elle ne vivait que
    là, dans une chaîne de caractères. On ne pouvait ni demander « qu'est-ce qui
    appuie ce paragraphe ? », ni « quelle pièce n'appuie plus rien ? », ni
    détecter une cote devenue fantôme après un remaniement.

    CETTE TABLE EST UN CONSTAT, comme `BordereauDepotJuillet` dont elle est le
    pendant : celle-là enregistre quelle pièce a reçu quelle cote, celle-ci
    enregistre quel paragraphe l'invoque. Ni l'une ni l'autre ne se calcule à
    partir d'un état courant — elles décrivent un acte déposé.

    ELLE NE CONNAÎT PAS LES AXES. Les axes (`argument_manager`) sont une
    exploration en cours d'une présentation FUTURE de la preuve ; ils
    n'existaient pas au dépôt et ne s'y projettent pas. Écrire le dépôt dans
    `Fait`/`AppuiFait` mêlerait un acte figé à un chantier ouvert, et toute
    requête sur l'un renverrait du contenu de l'autre. Les deux couches se
    lisent ensemble quand on le veut, jamais par accident.

    LA PIÈCE EST DÉSIGNÉE PAR SA LIGNE DE BORDEREAU, pas par une clé générique.
    Ce qu'un paragraphe invoque n'est pas un objet de la base, c'est une PIÈCE
    COTÉE : « P-49.2 ». Une clé étrangère vers le bordereau dit exactement cela,
    et la pièce elle-même reste atteignable par `entree.content_object`.

    LES LIASSES. Une liasse est la façon dont le dépôt organise N pièces sous
    une cote unique. Un paragraphe qui écrit « P-48.1 à P-48.3 » cite trois
    sous-cotes ; un paragraphe qui écrit « P-43 » cite la liasse entière et
    invoque donc ses dix-neuf pièces. Les deux produisent une ligne par pièce —
    c'est ce qui rend la liasse adressable — et `via_liasse` retient laquelle
    des deux formes le texte employait, car seule la seconde est une expansion.
    """

    statement = models.ForeignKey(
        'document_manager.Statement', on_delete=models.CASCADE,
        related_name='appuis_depot',
        help_text="Le paragraphe de la demande déposée qui invoque la pièce."
    )
    entree = models.ForeignKey(
        BordereauDepotJuillet, on_delete=models.PROTECT,
        related_name='appuis_depot',
        help_text="La ligne du bordereau, c'est-à-dire la pièce sous sa cote."
    )

    cote_citee = models.CharField(
        max_length=20,
        help_text="La cote telle qu'ÉCRITE dans le paragraphe : « P-48.1 », ou "
                  "« P-43 » lorsque le texte invoque la liasse en bloc."
    )
    via_liasse = models.BooleanField(
        default=False,
        help_text="True si la ligne provient du développement d'une cote racine. "
                  "Le paragraphe n'a pas nommé cette pièce : il a nommé sa liasse."
    )

    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Appui — dépôt du 24 juillet 2026"
        verbose_name_plural = "Appuis — dépôt du 24 juillet 2026"
        ordering = ['statement', 'entree']
        indexes = [
            models.Index(fields=['entree']),
            models.Index(fields=['statement']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['statement', 'entree'],
                name='appui_depot_unique',
            ),
        ]

    def __str__(self):
        return f"{self.cote_citee} → statement {self.statement_id}"

