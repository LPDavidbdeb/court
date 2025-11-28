import google.generativeai as genai
from django.conf import settings
import fitz  # PyMuPDF
import PIL.Image

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
    }
}

def analyze_document_content(document_object, persona_key='forensic_clerk'):
    """
    Submits the document to the AI using the selected persona.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest') # Or 'gemini-1.5-flash'

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
