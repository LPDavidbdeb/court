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

    # --- la cote du pont ---
    # Entre le dépôt de juillet et la version à notifier, le dossier travaille
    # dans une troisième cotation : celle de juillet, REPRISE À L'IDENTIQUE,
    # étendue aux passages précis qu'un paragraphe invoque réellement. Le § 48 a
    # plaidé « P-98 » ; il s'appuie en fait sur une phrase de P-98, qui devient
    # « P-98.1 ».
    #
    # ELLE SE STOCKE, contrairement à la cotation chronologique. Celle-là
    # réordonne les pièces par date et vieillit dès qu'une pièce est ajoutée ou
    # datée — d'où son calcul à chaque lecture. Le pont, lui, hérite d'une
    # numérotation gelée : sa base ne bouge pas, donc rien ne s'y désynchronise,
    # et il doit rester lisible tel quel pour être cité, relu et amendé.
    cote_pont = models.CharField(
        max_length=20, unique=True, db_index=True, null=True, blank=True,
        help_text="Cote de travail : « P-98 » reprise de juillet, ou « P-98.1 » "
                  "pour un passage précis. NULL tant que la pièce n'entre pas au pont."
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='precisions',
        help_text="La pièce dont cette ligne précise un passage. NULL pour une "
                  "pièce entière."
    )
    rang_precision = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Rang du passage sous sa pièce mère (le .1 de P-98.1)."
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

    precision = models.ForeignKey(
        BordereauDepotJuillet, on_delete=models.PROTECT, null=True, blank=True,
        related_name='appuis_precision',
        help_text="Le passage précis sur lequel ce paragraphe s'appuie, quand il "
                  "est identifiable. `entree` continue de dire ce que juillet a "
                  "plaidé — « P-98 » ; celle-ci dit sur quoi, dans P-98, le "
                  "paragraphe repose réellement."
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



# ---------------------------------------------------------------------------
# LES TRANSMISSIONS — bordereaux de l'art. 134 C.p.c. et journal des envois
#
# Trois faits ont rendu ces modèles nécessaires, et aucun n'est théorique :
#
#   1. L'adresse de notification d'une défenderesse a changé DEUX FOIS en trois
#      semaines (domicile le 17 sept., étude le 29 sept., avocats le 5 oct.).
#      Écrire à une adresse périmée est une faute élémentaire que rien, dans un
#      fichier Markdown, ne signale.
#   2. L'art. 134 C.p.c. prescrit le contenu du bordereau poste par poste, y
#      compris « l'heure et les minutes de la transmission » — qu'un bordereau
#      rédigé AVANT l'envoi ne peut pas connaître. Le bordereau définitif se
#      produit donc APRÈS, depuis l'en-tête du message réellement envoyé.
#   3. « Ce bordereau n'est produit au greffe que si une partie le demande » :
#      il faut pouvoir le reproduire des mois plus tard. Généré depuis la base,
#      il est toujours reproductible ; tenu à la main, il dérive.
#
# Ces modèles n'envoient rien. L'envoi reste manuel, et c'est voulu : la règle
# n° 2 du dossier est « jamais de réponse sur le fond le jour même ».
# ---------------------------------------------------------------------------


class DestinataireInstance(models.Model):
    """Une partie à l'instance et l'adresse où elle reçoit, à une date donnée.

    L'historique est conservé : une adresse n'est jamais écrasée, elle est
    fermée par `valide_au` et une nouvelle ligne s'ouvre. C'est ce qui permet de
    répondre à « où fallait-il écrire le 29 septembre ? » aussi bien qu'à « où
    faut-il écrire aujourd'hui ? ».
    """

    QUALITE = [
        ("PARTIE", "Partie, non représentée"),
        ("AVOCAT", "Avocats d'une partie"),
    ]

    partie = models.CharField(
        max_length=120,
        help_text="Nom de la partie destinataire, tel qu'à l'intitulé.",
    )
    qualite = models.CharField(max_length=10, choices=QUALITE, default="PARTIE")
    pour_le_compte_de = models.CharField(
        max_length=120, blank=True,
        help_text="Si qualite=AVOCAT : la partie représentée.",
    )
    courriel = models.EmailField()
    adresse_postale = models.TextField(blank=True)
    valide_du = models.DateField()
    valide_au = models.DateField(
        null=True, blank=True,
        help_text="Vide = encore valide. Renseigné = adresse fermée à cette date.",
    )
    source = models.CharField(
        max_length=255, blank=True,
        help_text="L'acte qui établit cette adresse (réponse, avis de substitution…).",
    )

    class Meta:
        verbose_name = "Destinataire de l'instance"
        verbose_name_plural = "Destinataires de l'instance"
        ordering = ["partie", "-valide_du"]

    def __str__(self):
        fin = self.valide_au.isoformat() if self.valide_au else "—"
        return f"{self.partie} <{self.courriel}> ({self.valide_du} → {fin})"

    def est_valide_le(self, jour):
        if jour < self.valide_du:
            return False
        return self.valide_au is None or jour <= self.valide_au


class Transmission(models.Model):
    """Un acte sortant : son bordereau, ses vérifications, sa preuve d'envoi."""

    ETAT = [
        ("PREPAREE", "Préparée — vérifiée, pas encore envoyée"),
        ("ENVOYEE", "Envoyée — message retrouvé, bordereau définitif"),
        ("ABANDONNEE", "Abandonnée"),
    ]

    nature = models.CharField(
        max_length=255,
        help_text="Nature du document transmis, au sens de l'art. 134 C.p.c.",
    )
    dossier = models.CharField(max_length=60, default="505-17-016235-261")
    destinataire = models.ForeignKey(
        DestinataireInstance, on_delete=models.PROTECT, related_name="transmissions",
    )
    fichier_source = models.CharField(
        max_length=1024,
        help_text="Chemin du .md de `legal/instance/sortants/` dont l'acte est tiré.",
    )
    lieu = models.CharField(max_length=120, default="Saint-Lambert (Québec)")

    etat = models.CharField(max_length=12, choices=ETAT, default="PREPAREE")
    preparee_le = models.DateTimeField(auto_now_add=True)
    envoyee_le = models.DateTimeField(
        null=True, blank=True,
        help_text="Horodatage RÉEL, repris de l'en-tête Date du message envoyé.",
    )
    email = models.ForeignKey(
        "email_manager.Email", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="transmissions",
        help_text="Le message envoyé, une fois ingéré. C'est lui, la preuve.",
    )

    verification = models.JSONField(
        default=dict, blank=True,
        help_text="Rapport de la vérification préalable : blocages, signalements, attestations.",
    )
    bordereau = models.TextField(
        blank=True,
        help_text="Bordereau de l'art. 134. Provisoire avant l'envoi, définitif après.",
    )

    class Meta:
        verbose_name = "Transmission"
        verbose_name_plural = "Transmissions"
        ordering = ["-preparee_le"]

    def __str__(self):
        return f"{self.nature} → {self.destinataire.partie} [{self.etat}]"

    @property
    def bloquee(self):
        return bool(self.verification.get("blocages"))


class FichierTransmis(models.Model):
    """Une pièce jointe, et son empreinte.

    L'art. 134 exige que le bordereau contienne « l'information nécessaire pour
    permettre au destinataire de vérifier l'intégrité de la transmission ».
    L'empreinte SHA-256 est cette information — et c'est exactement ce que les
    lettres du dossier promettent déjà.
    """

    transmission = models.ForeignKey(
        Transmission, on_delete=models.CASCADE, related_name="fichiers",
    )
    chemin = models.CharField(max_length=1024)
    nom_transmis = models.CharField(
        max_length=255, help_text="Nom du fichier tel que joint au message.",
    )
    cote = models.CharField(max_length=20, blank=True)
    octets = models.PositiveBigIntegerField(default=0)
    sha256 = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Fichier transmis"
        verbose_name_plural = "Fichiers transmis"
        ordering = ["cote", "nom_transmis"]

    def __str__(self):
        return f"{self.cote or self.nom_transmis} — {self.sha256[:12]}…"


# ---------------------------------------------------------------------------
# LA CONFIRMATION DES APPUIS DE LA VERSION MODIFIÉE
#
# `AppuiDepotJuillet` enregistre ce que la demande DÉPOSÉE invoquait. Il ne se
# recopie pas pour un paragraphe réécrit : ce serait présenter comme déposé en
# juillet un énoncé qui ne l'a pas été.
#
# La version modifiée a donc sa propre couche. Elle répond à trois questions
# que la première ne peut plus porter :
#
#   — quelles pièces sont RETENUES pour ce nouvel énoncé, par opposition à
#     celles que son antécédent invoquait (consultables par la concordance) ;
#   — sur QUEL TEXTE la confirmation a été donnée, pour qu'une réécriture la
#     rende historique au lieu de la laisser valoir pour un énoncé qu'elle n'a
#     jamais examiné ;
#   — l'ABSENCE d'appui, lorsqu'elle est décidée. Une liste vide ne dit pas
#     cela : elle ne distingue pas « rien ne l'appuie, et c'est assumé » de
#     « personne n'a encore regardé ».
# ---------------------------------------------------------------------------

class EtatAppui(models.TextChoices):
    A_EXAMINER = 'A_EXAMINER', 'À examiner'
    CONFIRME = 'CONFIRME', 'Confirmé pour le texte examiné'
    A_REEXAMINER = 'A_REEXAMINER', 'À réexaminer (texte ou portée modifié)'
    SANS_APPUI = 'SANS_APPUI', 'Sans appui documenté — décision motivée'
    ECARTE = 'ECARTE', 'Candidat écarté'


class ConfirmationAppui(models.Model):
    """
    « Cette pièce appuie CE texte-ci, pour cette portée. »

    LA PORTÉE EST UN CHAMP, pas un sous-entendu. Une pièce peut appuyer la date
    d'un fait sans appuyer son interprétation ; confirmer « P-52 appuie le § 44 »
    sans dire pour quoi laisse la relecture croire qu'elle couvre tout l'énoncé.
    Changer la portée invalide donc la confirmation au même titre que changer le
    texte.
    """
    noeud = models.ForeignKey(
        'document_manager.LibraryNode', on_delete=models.CASCADE,
        related_name='confirmations_appui',
        help_text="L'OCCURRENCE cible — pas le Statement : un même énoncé "
                  "repris dans deux actes peut n'y être pas appuyé pareil."
    )
    entree = models.ForeignKey(
        BordereauDepotJuillet, on_delete=models.PROTECT,
        related_name='confirmations_appui', null=True, blank=True,
        help_text="La pièce retenue. NULL pour une absence d'appui documentée."
    )
    version_examinee = models.ForeignKey(
        'document_manager.VersionTexte', on_delete=models.PROTECT,
        related_name='confirmations_appui', null=True, blank=True,
        help_text="La version du texte sur laquelle la décision a été prise."
    )
    etat = models.CharField(
        max_length=14, choices=EtatAppui.choices, default=EtatAppui.A_EXAMINER
    )
    role = models.CharField(
        max_length=40, blank=True,
        help_text="À quel titre la pièce est retenue (attestation, illustration…)."
    )
    portee = models.TextField(
        blank=True,
        help_text="CE QUE la pièce établit de cet énoncé, et rien de plus."
    )
    portee_sha256 = models.CharField(
        max_length=64, blank=True,
        help_text="Empreinte de la portée au moment de la confirmation : la "
                  "modifier doit périmer la confirmation comme le ferait le texte."
    )
    motif = models.TextField(
        blank=True,
        help_text="Obligatoire pour SANS_APPUI : l'absence est une décision, "
                  "elle se motive."
    )
    issu_de = models.ForeignKey(
        AppuiDepotJuillet, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reprises',
        help_text="L'appui de juillet dont ce candidat procède, le cas échéant. "
                  "Informatif : il ne vaut pas confirmation."
    )
    decide_le = models.DateTimeField(null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    maj_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Appui de la version modifiée"
        verbose_name_plural = "Appuis de la version modifiée"
        ordering = ['noeud', 'pk']
        constraints = [
            models.UniqueConstraint(
                fields=['noeud', 'entree'],
                name='confirmation_appui_unique_par_piece',
            ),
        ]

    def __str__(self):
        cible = self.entree.cote if self.entree else "sans appui"
        return f"Nœud {self.noeud_id} — {cible} [{self.etat}]"

    @staticmethod
    def empreinte_portee(portee):
        import hashlib
        return hashlib.sha256((portee or "").encode('utf-8')).hexdigest()

    def etat_courant(self):
        """
        L'état réel, texte et portée d'aujourd'hui comparés à ceux examinés.

        Ne devine pas si le changement est « substantiel » : toute divergence
        d'empreinte fait retomber en réexamen, et la reconfirmation est explicite.
        """
        if self.etat not in (EtatAppui.CONFIRME, EtatAppui.SANS_APPUI):
            return self.etat
        if self.version_examinee and not self.version_examinee.est_courante:
            return EtatAppui.A_REEXAMINER
        if self.portee_sha256 and \
                self.portee_sha256 != self.empreinte_portee(self.portee):
            return EtatAppui.A_REEXAMINER
        return self.etat


# ---------------------------------------------------------------------------
# LES CITATIONS DE PIÈCES DANS LE TEXTE
#
# Un paragraphe écrit « tel qu'il appert de la pièce P-12 ». Si une pièce
# antérieure est versée, la même source devient P-13 — et le texte rendu doit
# citer P-13, SANS que la pièce qui occupe désormais P-12 soit citée à sa place.
#
# CE QUI EST INTERDIT : chercher « P-12 » dans Statement.text et le remplacer.
# Un nombre dans un texte juridique peut être une date, une somme, le numéro
# d'un paragraphe d'un acte adverse, ou la cote LITTÉRALE d'une citation
# historique — laquelle doit rester intacte, puisqu'elle rapporte ce qui a été
# écrit à l'époque.
#
# D'où un ANCRAGE : la citation est rattachée à une ligne de bordereau, donc à
# une SOURCE, et le libellé affiché se recalcule à la lecture depuis l'état de
# cotation retenu. Le texte stocké n'est jamais réécrit.
# ---------------------------------------------------------------------------

class AncrageCitation(models.Model):
    """
    « Cette occurrence de "P-12", à cet endroit du texte, désigne CETTE pièce. »

    La position est conservée pour le rendu ; l'identité de la pièce est ce qui
    fait foi. Une citation historique littérale ne reçoit pas d'ancrage : elle
    n'est pas une référence du document courant, et doit rester telle quelle.
    """
    noeud = models.ForeignKey(
        'document_manager.LibraryNode', on_delete=models.CASCADE,
        related_name='ancrages_citation',
        help_text="L'occurrence dont le texte porte la citation."
    )
    entree = models.ForeignKey(
        BordereauDepotJuillet, on_delete=models.PROTECT,
        related_name='ancrages_citation', null=True, blank=True,
        help_text="La pièce désignée. NULL = référence non rattachée : elle "
                  "bloque l'export strict (EX04) jusqu'à résolution."
    )
    libelle_ecrit = models.CharField(
        max_length=30,
        help_text="La cote telle qu'elle figure dans le texte stocké : « P-12 »."
    )
    debut = models.PositiveIntegerField(
        help_text="Index du premier caractère de l'occurrence dans le texte."
    )
    fin = models.PositiveIntegerField()
    version_texte = models.ForeignKey(
        'document_manager.VersionTexte', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ancrages',
        help_text="La version du texte où ces positions ont été relevées."
    )
    litterale = models.BooleanField(
        default=False,
        help_text="True si cette cote appartient à une citation rapportée : "
                  "elle est laissée telle quelle, jamais recalculée."
    )
    ambigu = models.BooleanField(
        default=False,
        help_text="Plusieurs pièces répondent au libellé, ou la source est "
                  "douteuse. Bloque l'export strict."
    )
    note = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ancrage de citation"
        verbose_name_plural = "Ancrages de citation"
        ordering = ['noeud', 'debut']
        constraints = [
            models.UniqueConstraint(
                fields=['noeud', 'debut', 'fin'],
                name='ancrage_citation_unique_par_position',
            ),
        ]

    def __str__(self):
        return f"Nœud {self.noeud_id} [{self.debut}:{self.fin}] → {self.libelle_ecrit}"

    @property
    def resolu(self):
        return self.entree_id is not None and not self.ambigu
