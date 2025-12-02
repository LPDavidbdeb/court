import google.generativeai as genai
from django.conf import settings
import fitz  # PyMuPDF
import PIL.Image
import json
from .utils import EvidenceFormatter

# 1. Define the Personas
AI_PERSONAS = {
    'forensic_clerk': {
        'name': 'Greffier Forensique (Description Visuelle)',
        'prompt': """
        RÔLE : Greffier forensique.
        TÂCHE : Décris ce document de manière exhaustive pour qu'un tiers puisse comprendre son contenu sans le voir.
        INSTRUCTIONS :
        1. Décris la scène, les personnes et l'ambiance.
        2. Rapporte les faits visuels bruts sans opinion.
        3. Si texte visible, résume les points clés.
        FORMAT : Texte structuré.
        """
    },
    'official_scribe': {
        'name': 'Scribe Officiel (Transcription PDF)',
        'prompt': """
        RÔLE : Scribe officiel / Transcripteur juridique.
        TÂCHE : Transcris le contenu textuel de ce document avec une précision absolue (mot pour mot).
        INSTRUCTIONS CRITIQUES :
        1. AUCUNE INTERPRÉTATION ou résumé.
        2. Conserve le formatage structurel (Titres, paragraphes, listes à puces) pour que le texte soit lisible.
        3. Si le texte est illisible, marque [Illisible].
        4. Le but est de substituer ce texte au document original dans un rapport légal.
        FORMAT DE SORTIE : Markdown propre.
        """
    },
    'summary_clerk': {
        'name': 'Secrétaire de Synthèse (Résumé)',
        'prompt': """
        RÔLE : Secrétaire juridique senior.
        TÂCHE : Fais un résumé exécutif de ce document.
        INSTRUCTIONS :
        1. Identifie les dates clés.
        2. Identifie les acteurs principaux.
        3. Résume l'enjeu ou le contenu en 3-4 points.
        """
    },
    'police_investigator': {
        'name': 'Enquêteur Criminel (Plainte Art. 131)',
        'model_model': 'gemini-1.5-pro',
        'temperature': 0.1,
        'prompt': """
        RÔLE : Assistant expert en rédaction juridique formé à la procédure pénale canadienne.
        MISSION : Rédiger les données structurées pour une PLAINTE POLICIÈRE FORMELLE.
        
        CONSIGNES DE TON ET DE CONTENU :
        1.  Produire un compte rendu clair, objectif et factuel.
        2.  Langage neutre et professionnel : aucune spéculation, opinion ou phrase émotionnelle.
        3.  NE PAS ajouter ou inférer de faits non explicitement fournis.
        4.  Ignorer le contexte de garde d'enfants (civil). Se concentrer sur le mensonge (criminel).

        STRUCTURE DE SORTIE OBLIGATOIRE (JSON) :
        {
            "titre_document": "RAPPORT D'OCCURRENCE / PLAINTE POLICIÈRE",
            "sections": [
                {
                    "titre": "A. RENSEIGNEMENTS SUR LE PLAIGNANT",
                    "contenu": "Indiquer [Information non fournie] si absent."
                },
                {
                    "titre": "B. APERÇU DE L'INCIDENT",
                    "contenu": "Type d'incident (Faux affidavit - Art 131 C.cr.), Date approximative."
                },
                {
                    "titre": "C. RÉCIT DÉTAILLÉ (FACTUEL)",
                    "contenu": "Résumé chronologique sec des événements pertinents pour l'infraction."
                },
                {
                    "titre": "D. LISTE DES MENSONGES (ACTUS REUS)",
                    "contenu": [
                        "Mensonge 1 : Citation exacte...",
                        "Mensonge 2 : Citation exacte..."
                    ]
                },
                {
                    "titre": "E. PREUVES MATÉRIELLES (DATE & PIÈCE)",
                    "contenu": [
                        "Contre le mensonge 1 : La photo P-12 du [DATE] montre...",
                        "Contre le mensonge 2 : Le courriel P-14 du [DATE] prouve..."
                    ]
                },
                {
                    "titre": "F. PREUVE DE CONNAISSANCE (MENS REA)",
                    "contenu": "Preuve que le sujet SAVAIIT que c'était faux (ex: Elle est l'auteure du courriel P-X)."
                },
                {
                    "titre": "G. DEMANDE",
                    "contenu": "Je demande que cette affaire soit examinée et documentée pour enquête criminelle."
                }
            ]
        }
        """
    },
}

def analyze_document_content(document_object, persona_key='forensic_clerk'):
    """
    Submits the document to the AI using the selected persona.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro-latest')

    # 2. Select the Prompt
    persona = AI_PERSONAS.get(persona_key, AI_PERSONAS['forensic_clerk'])
    content_parts = [persona['prompt']]

    try:
        # Case 1: PhotoDocument
        if hasattr(document_object, 'photos'): 
            for photo in document_object.photos.all()[:10]: # Increased limit to 10
                if photo.file:
                    img = PIL.Image.open(photo.file.path)
                    content_parts.append(img)

        # Case 2: PDFDocument
        elif hasattr(document_object, 'file') and document_object.file.name.lower().endswith('.pdf'):
            pdf_path = document_object.file.path
            doc = fitz.open(pdf_path)
            # Increased limit to 10 pages for transcriptions
            for page_num in range(min(len(doc), 10)): 
                pix = doc.load_page(page_num).get_pixmap(dpi=150)
                img = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                content_parts.append(img)

        # API Call
        response = model.generate_content(content_parts)
        
        # Save
        document_object.ai_analysis = response.text
        document_object.save()
        return True

    except Exception as e:
        print(f"Erreur d'analyse : {e}")
        return False

def analyze_for_json_output(prompt_parts):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # Configuration pour forcer le JSON
    generation_config = {
        "response_mime_type": "application/json",
    }
    
    model = genai.GenerativeModel(
        'gemini-pro-latest', # Utilisation d'un modèle stable et compatible
        generation_config=generation_config
    )
    
    response = model.generate_content(prompt_parts)
    return response.text

def run_narrative_audit_service(narrative):
    """
    Exécute l'agent 'Auditeur' sur une trame narrative.
    Retourne un dict JSON structuré.
    """
    # 1. Préparation des données
    xml_context = EvidenceFormatter.format_narrative_context_xml(narrative)

    # 2. Le Prompt Système (L'Auditeur Impartial)
    system_instruction = """
    RÔLE : Auditeur Forensique Impartial.
    CONTEXTE : Tu analyses une section d'un dossier judiciaire civil.
    
    INPUT : 
    1. <theses_adverses> : Ce que la partie adverse prétend (Allégations).
    2. <elements_preuve> : Les faits bruts disponibles (Emails, Photos, etc.).

    MISSION :
    Pour chaque allégation, détermine si les preuves la contredisent, la supportent ou sont neutres.
    Sois factuel. Cite les IDs des preuves (ex: P-EMAIL-12).
    Ne fais PAS de déduction psychologique (pas de "il voulait dire que...").
    
    FORMAT DE SORTIE (JSON STRICT) :
    {
      "constats_objectifs": [
        {
           "fait_identifie": "Titre court du fait observé",
           "description_factuelle": "Description précise (ex: Le père était à l'hôpital le 12 mars selon P-EMAIL-5).",
           "contradiction_directe": "Explique brièvement quelle allégation est touchée."
        }
      ]
    }
    """

    prompt_parts = [system_instruction, xml_context]

    # 3. Appel à votre fonction existante
    raw_json = analyze_for_json_output(prompt_parts)

    # 4. Parsing
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response", "raw": raw_json}

def run_police_investigator_service(narratives_queryset):
    """
    Prépare le 'Big Context' et lance l'agent Police.
    """
    # Construction du contexte global (Chronologie + Allégations)
    full_chronology = EvidenceFormatter.format_full_chronology(narratives_queryset)
    
    allegations_text = ""
    for narrative in narratives_queryset:
        for stmt in narrative.targeted_statements.all():
            allegations_text += f"- DÉCLARATION : « {stmt.text} » (Doc: {stmt.document.title})\n"

    # Injection dans le prompt
    persona = AI_PERSONAS['police_investigator']
    prompt_sequence = [
        persona['prompt'],
        "VOICI LES DÉCLARATIONS SUSPECTES :",
        allegations_text,
        "VOICI LA CHRONOLOGIE DES FAITS PROUVÉS :",
        full_chronology
    ]
    
    # Appel à l'IA (Force le JSON via votre fonction existante)
    return analyze_for_json_output(prompt_sequence)
