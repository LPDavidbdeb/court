"""Génération documentaire des seules vues C0-A, sans import applicatif ni DB."""
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
GLOBAL = BASE / 'modele_global'
GLOBAL.mkdir(exist_ok=True)
STYLE = '''skinparam backgroundColor #FFFFFF
skinparam defaultFontName SansSerif
skinparam defaultFontSize 15
skinparam shadowing false
skinparam roundcorner 8
skinparam ArrowColor #334155
skinparam classBackgroundColor #EFF6FF
skinparam classBorderColor #2563EB
skinparam activityBackgroundColor #EFF6FF
skinparam activityBorderColor #2563EB
skinparam noteBackgroundColor #FFFBEB
skinparam noteBorderColor #D97706
skinparam maxMessageSize 240
hide empty members
'''
(GLOBAL / 'style.iuml').write_text(STYLE)

ENTITIES = {
    'Document': ['* id : PK', 'source_type : PRODUCED / REPRODUCED', 'title'],
    'ContentType': ['* id : PK technique', 'app_label; model'],
    'LibraryNode': ['* id : PK occurrence', 'document_id : FK CASCADE', 'content_type_id : FK nullable', 'object_id : entier nullable', 'item; paragraph_number', 'path; depth; numchild'],
    'Statement': ['* id : PK', 'text', 'is_true; is_falsifiable', 'is_user_created'],
    'VersionTexte': ['* id : PK', 'statement_id : FK CASCADE', 'texte; empreinte; motif', 'UQ(statement_id, empreinte)'],
    'Correspondance': ['* id : PK', 'document_source_id : FK PROTECT', 'document_cible_id : FK CASCADE', 'etat; traitement; motif', 'versions_source_examinees : M2M', 'versions_cible_examinees : M2M'],
    'ExtremiteCorrespondance': ['* id : PK', 'correspondance_id : FK CASCADE', 'role : SOURCE / CIBLE; ordre', 'noeud_id : FK PROTECT nullable', 'archive_id : FK SET_NULL nullable', 'UQ(correspondance, role, noeud)'],
    'NoeudArchive': ['* id : PK', 'document_id : FK CASCADE', 'noeud_pk; statement_pk : anciens IDs', 'texte; texte_sha256; motif', 'statement_supprime; supprime_le'],
    'ReferentHistorique': ['* id : PK', 'document_id : FK unique PROTECT'],
    'ConfirmationAppui': ['* id : PK', 'noeud_id : FK CASCADE', 'version_examinee_id : FK PROTECT nullable', 'entree_id : FK PROTECT nullable', 'etat; portee; portee_sha256'],
    'AncrageCitation': ['* id : PK', 'noeud_id : FK CASCADE', 'version_texte_id : FK SET_NULL nullable', 'entree_id : FK PROTECT nullable'],
    'AppuiDepotJuillet': ['* id : PK', 'statement_id : FK CASCADE', 'entree_id : FK PROTECT', 'cote_citee; via_liasse'],
    'BordereauDepotJuillet': ['* id : PK', 'cote; rang'],
}
LINKS = [
    ('ContentType','LibraryNode','ContentType |o--o{ LibraryNode : type déclaré (nullable)'),
    ('Document','LibraryNode','Document ||--o{ LibraryNode : contient'),
    ('LibraryNode','Statement','LibraryNode }o..o| Statement : GFK si type vérifié'),
    ('Statement','VersionTexte','Statement ||--o{ VersionTexte : captures'),
    ('Document','Correspondance','Document ||--o{ Correspondance : source / cible'),
    ('Correspondance','ExtremiteCorrespondance','Correspondance ||--o{ ExtremiteCorrespondance : extrémités'),
    ('LibraryNode','ExtremiteCorrespondance','LibraryNode |o--o{ ExtremiteCorrespondance : noeud actif'),
    ('NoeudArchive','ExtremiteCorrespondance','NoeudArchive |o--o{ ExtremiteCorrespondance : archive'),
    ('Document','NoeudArchive','Document ||--o{ NoeudArchive : conserve'),
    ('ReferentHistorique','Document','Document ||--o| ReferentHistorique : référent'),
    ('LibraryNode','ConfirmationAppui','LibraryNode ||--o{ ConfirmationAppui : décisions'),
    ('VersionTexte','ConfirmationAppui','VersionTexte |o--o{ ConfirmationAppui : examinée'),
    ('LibraryNode','AncrageCitation','LibraryNode ||--o{ AncrageCitation : insertions E01'),
    ('VersionTexte','AncrageCitation','VersionTexte |o--o{ AncrageCitation : texte ancré'),
    ('Statement','AppuiDepotJuillet','Statement ||--o{ AppuiDepotJuillet : références historiques'),
    ('BordereauDepotJuillet','AppuiDepotJuillet','BordereauDepotJuillet ||--o{ AppuiDepotJuillet : pièce historique'),
    ('BordereauDepotJuillet','ConfirmationAppui','BordereauDepotJuillet |o--o{ ConfirmationAppui : pièce retenue'),
    ('BordereauDepotJuillet','AncrageCitation','BordereauDepotJuillet |o--o{ AncrageCitation : référence'),
    ('Correspondance','VersionTexte','Correspondance }o--o{ VersionTexte : M2M SOURCE et CIBLE'),
]

def write(folder, filename, title, body, local=True):
    folder.mkdir(parents=True, exist_ok=True)
    inc = '../../modele_global/style.iuml' if local else 'style.iuml'
    source = (f'@startuml\n!include {inc}\ntitle {title}\n'
              'caption C0A-UML-R1 • socle proposé 515666e • cible non implantée • approbation utilisateur absente\n'
              + body.strip() + '\n@enduml\n')
    (folder / filename).write_text(source)

def erd(names, extra):
    lines=['left to right direction']
    for name in names:
        lines += [f'entity "{name}" as {name} <<EXISTANT>> {{', *('  '+x for x in ENTITIES[name]), '}']
    for a,b,line in LINKS:
        if a in names and b in names: lines.append(line)
    lines += ['legend bottom', 'ERD logique partiel : aucun nouveau champ ou nouvelle table en C0-A.',
              'Les jointures M2M existantes sont représentées comme associations.',
              'Les liens GFK et anciens IDs ne sont pas des FK vers Statement.',
              'CASCADE / SET_NULL restent le schéma observé; les refus C0-A sont applicatifs.',
              'endlegend', extra]
    return '\n'.join(lines)

common_erd_note = '''note bottom of VersionTexte
ERD-CAP : capture avant réécriture.
ERD-FRESH : occurrence actuelle + Statement + empreinte.
Gardes applicatives sur les captures utilisées.
Aucune garantie SQL/bulk globale ajoutée par C0-A.
end note'''
write(GLOBAL,'erd_consolide.puml','Modèle global cible G-C0A-R1 — périmètre C0-A',
      erd(list(ENTITIES), common_erd_note + '''
note top of NoeudArchive
ERD-ARCH : anciens identifiants et texte conservés.
Type historique complet et journal : L1-A / C0-B.
end note'''),False)

CLASSES = '''
class "produced_views" as V <<module, MODIF_PATCH>> {
  ajax_edit_node(request, node_pk)
  ajax_delete_node(request, node_pk)
}
class "concordance" as S <<module, MODIF_PATCH>> {
  detacher_pour_edition(noeud, texte, motif)
  supprimer_occurrence(noeud, motif)
  appuis_dorigine(noeud, document_source, document_cible)
}
class "protection" as P <<module, MODIF_PATCH>> {
  est_reproduit(document)
  est_referent(document_pk)
  statement_protege(statement_pk)
  captures_utilisees(statement_pk)
  verifier_suppression_noeud(noeud)
  archiver_noeud(noeud, motif)
  gardes pre_save / pre_delete
}
class LibraryNode <<modèle existant>> {
  id; document_id; content_type_id; object_id
  get_descendants()
  save(update_fields)
}
class Statement <<modèle existant>> {
  id; text
  save(update_fields)
}
class VersionTexte <<modèle existant>> {
  capter(statement, motif)
  empreinte_de(texte)
}
class Correspondance <<modèle, MODIF_PATCH>> {
  versions_courantes_examinees()
  etat_courant()
}
class ConfirmationAppui <<modèle, MODIF_PATCH>> {
  etat_courant()
}
V --> S : CLS-VUE : édition / suppression
V --> P : refus avant mutation
S --> P : CLS-GARDE : précontrôles / archives
S --> LibraryNode : repointage / suppression
S --> Statement : duplication ou modification privée
S --> VersionTexte : CLS-CAP : conserver avant / après
Correspondance --> LibraryNode : relire les extrémités actuelles
Correspondance --> VersionTexte : comparer identités et empreintes
ConfirmationAppui --> LibraryNode : recharger occurrence actuelle
ConfirmationAppui --> VersionTexte : CLS-FRESH : décision conservée
note bottom of P
Les gardes locales et transaction.atomic existent dans la cible du patch.
Pas de nouveau schéma, ExamenEditorial, nature, verrou global ou stockage.
La sérialisation des écritures concurrentes n'est pas démontrée par C0-A.
end note
'''
reader_classes = '''
class "export_concordance" as E <<module, MODIF_PATCH>> {
  _ligne(...)
}
class LectureAppuis <<résultat en mémoire, PROPOSE_CORRECTION>> {
  appuis_valides[]
  anomalies[] : corr / extremite / motif
}
E --> S : CLS-LECTURE : couple explicite
S ..> LectureAppuis : résultat partiel qualifié
E ..> LectureAppuis : garder appuis + diagnostics
note bottom of LectureAppuis
Aucune table ni persistance nouvelle.
API précise à implanter par A après autorisation.
Le patch actuel lève ValueError et perd les appuis valides : C0A-REV-01.
Une erreur globale de couple reste bloquante avant lecture.
end note
'''
write(GLOBAL,'classes_consolidees.puml','Classes et composants G-C0A-R1 — responsabilités C0-A',
      CLASSES+reader_classes,False)

ACT13 = r'''
start
:ACT-01 Recevoir occurrence et formulaire;
if (Formulaire valide ?) then (non)
  :400 sans écriture;
  stop
endif
:ACT-02 Transaction HTTP;
if (Document reproduit ou référent ?) then (oui)
  :ACT-REFUS Interdire même le renommage;
  stop
endif
if (Statement vérifié ?) then (oui)
  if (Texte identique ?) then (oui)
    :ACT-NOOP Garder le même Statement;
  else (non)
    :ACT-CAP Capter le texte avant modification;
    if (Partagé ou protégé ?) then (oui)
      :ACT-COW Créer un Statement privé;
      :Repointage de cette occurrence seulement;
    else (non)
      :Modifier le Statement privé;
    endif
    :Capter le texte résultant;
  endif
else (non)
  if (Contenu structurel vide ?) then (oui)
    :Créer le premier Statement de cette occurrence;
  else (non)
    :ACT-REFUS Type incompatible : annuler;
    stop
  endif
endif
:ACT-ITEM Sauver item dans la même transaction;
if (Erreur pendant les écritures ?) then (oui)
  :ACT-ROLLBACK Annuler toutes les écritures;
  stop
endif
:ACT-FRESH À la lecture : comparer occurrence actuelle,\nStatement et empreinte aux captures;
:Anciennes décisions conservées; état courant à réexaminer si divergence;
:Succès; autres occurrences et numéros historiques inchangés;
stop
'''
SEQ13 = r'''
actor Rédacteur as U
participant "Vue ajax_edit_node\nmodule produced_views" as V
participant "Service\nconcordance" as S
participant "Gardes\nprotection" as G
database "ORM / PostgreSQL\nexistant" as DB
participant "Lecteurs\nCorrespondance / ConfirmationAppui" as F
U -> V : SEQ-01 POST texte + item + node_pk
group transaction.atomic HTTP
V -> DB : occurrence + type + Document
V -> V : NodeForm.is_valid()
V -> G : SEQ-02 est_reproduit / est_referent
alt formulaire invalide / occurrence interdite
  break refus sans mutation
    V --> U : 400 / refus; aucune écriture
  end
else Statement vérifié
  V -> S : SEQ-03 detacher_pour_edition(occurrence, texte)
  group transaction.atomic service imbriquée
    S -> G : refus document; statement_protege
    alt texte identique
      S --> V : même Statement, aucune capture supplémentaire
    else texte différent
      S -> DB : SEQ-04 VersionTexte.capter(ancien)
      S -> DB : existe une autre occurrence du Statement ?
      alt partagé ou protégé
        S -> DB : SEQ-05 créer Statement privé; repointer cette occurrence
      else privé mutable
        S -> DB : SEQ-06 modifier seulement ce Statement
      end
      S -> DB : SEQ-07 capter texte résultant
    end
  end
  V -> DB : SEQ-08 save(item)
else aucun type et aucun objet
  V -> DB : SEQ-09 créer premier Statement + association + item
else autre type ou GFK incohérente
  break refus de type
    V --> U : refus; rollback
  end
end
alt échec écriture / garde
  DB --> V : exception
  note over V,DB : SEQ-ROLLBACK : annuler capture, nouveau Statement, repointage et item
else succès
  note over V,DB : Retour de la vue : sortie du décorateur atomique puis réponse
end
end
V --> U : JSON succès si transaction validée, sinon refus / erreur
U -> F : SEQ-10 consulter état courant de la décision
F -> DB : occurrence actuelle (rechargée pour ConfirmationAppui)\n+ Statement réellement associé + empreinte
F --> U : décision passée intacte; à réexaminer si identité / texte divergent
note over S,DB : Pas de select_for_update ou verrou global ajouté par le patch.\nC0-A ne promet pas de contrôle universel des éditions simultanées.
'''

ACT14 = r'''
start
:ACT-01 POST suppression occurrence;
if (Méthode POST ?) then (non)
  :405 sans mutation;
  stop
endif
:ACT-BLOC Lister occurrence et descendants;
:ACT-PRE Contrôler chaque membre du bloc;
if (Reproduit / référent / décision ou ancrage à détruire ?) then (oui)
  :ACT-REFUS Refuser tout le bloc avant archive;
  stop
endif
:ACT-TX Transaction du service;
:ACT-ARCH Archiver chaque membre et son texte disponible;
:ACT-REL Basculer les extrémités actives vers leurs archives;
:Supprimer les occurrences du bas vers le haut;
:ACT-PURGE Examiner uniquement les candidats de type Statement;
:Conserver tout Statement partagé, protégé,\nlié à un appui historique ou à une capture utilisée;
:Supprimer seulement les candidats devenus inutiles;
if (Échec archive / garde / écriture ?) then (oui)
  :ACT-ROLLBACK Restaurer tout le bloc et ses relations;
  :Réponse d'erreur; aucun effet partiel;
else (non)
  :Succès; archives et captures conservées consultables;
endif
stop
'''
SEQ14 = r'''
actor Rédacteur as U
participant "ajax_delete_node" as V
participant "concordance" as S
participant "protection" as G
database "ORM / PostgreSQL" as DB
U -> V : SEQ-01 POST node_pk
V -> S : SEQ-02 supprimer_occurrence(noeud, motif)
group transaction.atomic service (dans transaction HTTP)
S -> DB : bloc = occurrence + descendants
loop chaque occurrence
  S -> G : SEQ-03 verifier_suppression_noeud
end
alt bloc interdit
  G --> S : SuppressionRefusee avant toute archive
else bloc autorisé
  loop chaque occurrence
    S -> G : SEQ-04 archiver_noeud
    G -> DB : créer NoeudArchive (texte, anciens IDs, motif)
    S -> DB : SEQ-05 extrémité : archive = nouvelle; noeud = NULL
  end
  S -> DB : SEQ-06 supprimer occurrences par profondeur décroissante
  loop candidats dont ContentType == Statement
    S -> G : SEQ-07 statement_protege / captures_utilisees
    S -> DB : autres occurrences / appuis_depot ?
    alt candidat sans usage ni histoire utile
      S -> DB : supprimer Statement; archive.statement_supprime = true
    else candidat encore nécessaire
      note over S,DB : Conserver Statement et captures
    end
  end
end
alt échec dans le service
  note over S,DB : SEQ-ROLLBACK : savepoint annulé avant retour à la vue
  S --> V : exception; aucune archive ni suppression partielle
else succès
  S --> V : IDs supprimés / archives / Statements supprimés
end
end
V --> U : succès / refus 403 / erreur 500
note over V,DB : Le catch HTTP n'absorbe pas l'exception à l'intérieur du service atomique.
'''

ACT15 = r'''
start
:ACT-01 Demander cible + couple documentaire;
if (Couple invalide ou origine ambiguë sans couple ?) then (oui)
  :ACT-GLOBAL Refus global explicite;
  stop
endif
:Restreindre les correspondances au couple;
:Initialiser appuis valides et anomalies;
while (Une extrémité source reste ?) is (oui)
  if (Archive / absence / mauvais Document / type incompatible ?) then (oui)
    :ACT-DIAG Ajouter diagnostic local identifiable;
  else (non)
    if (Groupe structurel sans contenu ?) then (oui)
      :Aucun appui attendu;
    else (non)
      :ACT-VALID Lire les appuis du Statement vérifié;
      :Conserver les appuis valides de cette origine;
    endif
  endif
endwhile (non)
:ACT-RESULT Restituer appuis valides + anomalies;
:Qualifier VERSION SOURCE, sans créer d'appui retenu;
:ACT-EXPORT Export : préserver les deux listes,\ndiagnostic d'incomplétude visible, strict non réputé acquis;
stop
note right
PROPOSITION DE CORRECTION C0A-REV-01.
Le patch actuel interrompt la boucle à la première anomalie;
l'export remplace alors tous les appuis par une liste vide.
end note
'''
SEQ15 = r'''
actor Lecteur as U
participant "export_concordance._ligne" as E
participant "concordance.appuis_dorigine\ncible : correction proposée" as S
database "Correspondance / extrémités\nLibraryNode / AppuiDepotJuillet" as DB
participant "LectureAppuis\nDTO en mémoire proposé" as R
U -> E : SEQ-01 lire concordance du couple source / cible
E -> S : SEQ-02 cible + document_source + document_cible
S -> S : valider couple / ambiguïté globale
alt couple invalide
  S --> E : SEQ-GLOBAL erreur explicite, pas de lecture étrangère
else couple valide
  S -> DB : SEQ-03 filtrer les groupes du couple
  loop chaque extrémité SOURCE
    S -> DB : occurrence + Document + type + objet
    alt archive / absence / mauvais Document / type invalide
      S -> R : SEQ-DIAG ajouter anomalie (corr, extrémité, motif)
    else Statement vérifié
      S -> DB : SEQ-VALID appuis_depot de ce Statement
      S -> R : ajouter appuis qualifiés VERSION SOURCE
    else groupe structurel vide
      note over S,R : Aucun appui à chercher, sans inventer un Statement
    end
  end
  S --> E : SEQ-RESULT appuis valides + anomalies
  E --> U : SEQ-EXPORT appuis préservés; diagnostic lisible\naucune confirmation probatoire créée
end
note over E,R : Lecture sans écriture. Ni nature de L1-A, ni type d'archive deviné.\nCible attendue distincte du patch actuel : C0A-REV-01.
'''

for uc, activity, sequence, names in [
    ('13', ACT13, SEQ13, ['Document','ContentType','ReferentHistorique','LibraryNode','Statement','VersionTexte','Correspondance','ExtremiteCorrespondance','ConfirmationAppui']),
    ('14', ACT14, SEQ14, ['Document','ContentType','ReferentHistorique','LibraryNode','Statement','VersionTexte','Correspondance','ExtremiteCorrespondance','NoeudArchive','ConfirmationAppui','AncrageCitation','AppuiDepotJuillet']),
    ('15', ACT15, SEQ15, ['Document','ContentType','LibraryNode','Statement','Correspondance','ExtremiteCorrespondance','NoeudArchive','AppuiDepotJuillet','BordereauDepotJuillet']),
]:
    folder=BASE/'use_cases'/f'UC-C-{uc}'
    write(folder,'activity.puml',f'UC-C-{uc} — activité cible C0A-UML-R1',activity)
    write(folder,'sequence.puml',f'UC-C-{uc} — interactions et erreurs C0A-UML-R1',sequence)
    extra = common_erd_note if 'VersionTexte' in names else '''note bottom of AppuiDepotJuillet
ERD-ORIG : identité par Statement vérifié, jamais object_id seul.
ERD-PAIR : couple de Documents de Correspondance.
Archive non typée : diagnostic, jamais reconstitution d'un appui.
end note'''
    if uc=='14': extra += '''
note bottom of NoeudArchive
ERD-ARCH : archive avant suppression.
Extrémité active vers noeud, puis vers archive.
CASCADE évité par refus du service / signaux locaux;
les protections globales relèvent de L1-A / C0-B / L5.
end note'''
    write(folder,'erd.puml',f'UC-C-{uc} — ERD cible local, schéma existant',erd(names,extra))
    if uc=='13':
        local_classes=CLASSES.replace('  ajax_delete_node(request, node_pk)\n','').replace('  supprimer_occurrence(noeud, motif)\n','').replace('  appuis_dorigine(noeud, document_source, document_cible)\n','').replace('édition / suppression','édition seulement').replace('  verifier_suppression_noeud(noeud)\n','').replace('  archiver_noeud(noeud, motif)\n','').replace('  get_descendants()\n','').replace('repointage / suppression','repointage seulement')
    elif uc=='14':
        local_classes='''
class "produced_views" as V <<module, MODIF_PATCH>> {
  ajax_delete_node(request, node_pk)
}
class "concordance" as S <<module, MODIF_PATCH>> {
  supprimer_occurrence(noeud, motif)
}
class "protection" as P <<module, MODIF_PATCH>> {
  verifier_suppression_noeud(noeud)
  archiver_noeud(noeud, motif)
  statement_protege(pk)
  captures_utilisees(pk)
  gardes pre_delete
}
class LibraryNode <<modèle existant>> {
  get_descendants()
  suppression ORM des occurrences
}
class NoeudArchive <<modèle existant>> {
  anciens IDs; texte; motif
  save(statement_supprime)
}
class ExtremiteCorrespondance <<modèle existant>> {
  noeud_id; archive_id
  save(archive, noeud)
}
class Statement <<modèle existant>> {
  delete()
}
V --> S : CLS-VUE : service atomique
S --> P : CLS-GARDE : bloc entier avant écriture
P --> NoeudArchive : CLS-ARCH : capturer avant retrait
S --> ExtremiteCorrespondance : CLS-REL : passer vers archive
S --> LibraryNode : supprimer du bas vers le haut
S --> Statement : CLS-PURGE : seulement si sans usage utile
S --> NoeudArchive : marquer suppression du Statement
note bottom of P
Les décisions et ancrages non archivables entraînent un refus.
Le service atomique annule ses écritures avant le catch HTTP.
Les gardes SQL/bulk et le journal complet restent hors C0-A.
end note
'''
    else:
        local_classes = '''
class "concordance" as S <<module, CORRECTION_PROPOSEE>> {
  correspondances_de(noeud, role)
  appuis_dorigine(noeud, document_source, document_cible)
}
class Correspondance <<modèle existant>> {
  document_source_id; document_cible_id
}
class ExtremiteCorrespondance <<modèle existant>> {
  role; noeud_id; archive_id
}
class LibraryNode <<modèle existant>> {
  document_id; content_type_id; object_id
  content_object
}
class AppuiDepotJuillet <<modèle existant>> {
  statement_id; entree_id; cote_citee
}
S --> Correspondance : CLS-PAIR : restreindre le couple
S --> ExtremiteCorrespondance : itérer sans abandon global
S --> LibraryNode : CLS-TYPE : vérifier Document et contenu
S --> AppuiDepotJuillet : lire seulement Statement vérifié
'''+reader_classes
    write(folder,'class.puml',f'UC-C-{uc} — responsabilités de la cible C0A-UML-R1',local_classes)

print('14 sources PlantUML et style local générés; aucun code applicatif importé.')
