import google.generativeai as genai
from django.conf import settings
import fitz  # PyMuPDF
import PIL.Image

def analyze_document_content(document_object):
    """
    Submits the document (PDF or Photo) to the AI for a factual analysis.
    The result is saved in the 'ai_analysis' field.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = """
    RÔLE : Greffier forensique.
    TÂCHE : Décris ce document de manière exhaustive pour qu'un tiers puisse comprendre son contenu sans le voir.
    
    INSTRUCTIONS :
    1. S'il y a du texte, résume les points clés, les dates et les signataires.
    2. S'il y a des images, décris la scène, les personnes et l'ambiance.
    3. Ne donne PAS d'opinion juridique. Rapporte les faits bruts.
    4. Si c'est un courriel ou une lettre, note l'expéditeur, le destinataire et la date.
    
    FORMAT DE SORTIE : Texte brut structuré.
    """
    
    content_parts = [prompt]

    try:
        # Case 1: PhotoDocument
        if hasattr(document_object, 'photos'): 
            for photo in document_object.photos.all()[:5]: # Max 5 photos
                if photo.file:
                    img = PIL.Image.open(photo.file.path)
                    content_parts.append(img)
                    content_parts.append("Image suivante du dossier...")

        # Case 2: PDFDocument
        elif hasattr(document_object, 'file') and document_object.file.name.lower().endswith('.pdf'):
            pdf_path = document_object.file.path
            doc = fitz.open(pdf_path)
            for page_num in range(min(len(doc), 5)): # Max 5 pages
                pix = doc.load_page(page_num).get_pixmap()
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
