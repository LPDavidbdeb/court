from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.apps import apps
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from argument_manager.models import TrameNarrative
from pdf_manager.models import PDFDocument
from email_manager.models import Email
from document_manager.models import Document
from case_manager.models import LegalCase
from case_manager.services import rebuild_global_exhibits
from .services import global_semantic_search

def index(request):
    return render(request, 'core/index.html')

def semantic_search_view(request):
    """
    View to display and process global semantic search.
    """
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        results = global_semantic_search(query)
        
    return render(request, 'core/semantic_search.html', {
        'query': query,
        'results': results,
    })

def story_scrollytelling_view(request, pk):
    """
    Affiche une trame narrative sous forme d'histoire chronologique interactive.
    pk: L'ID de la Trame Narrative "L'Érosion des Motifs"
    """
    trame = get_object_or_404(TrameNarrative, pk=pk)
    timeline = trame.get_chronological_evidence()
    
    return render(request, 'core/story_scrollytelling.html', {
        'trame': trame,
        'timeline': timeline
    })

def story_cinematic_view(request, pk):
    """
    Processus parallèle : Vue "Expérience Cinématographique".
    Utilise les mêmes données que la vue standard, mais les injecte 
    dans le template d'animation GSAP.
    """
    trame = get_object_or_404(TrameNarrative, pk=pk)
    
    # On réutilise la logique de tri existante du modèle (Data Source of Truth)
    timeline = trame.get_chronological_evidence()
    source_documents = trame.get_source_documents()
    
    return render(request, 'core/story_cinematic.html', {
        'trame': trame,
        'timeline': timeline,
        'source_documents': source_documents
    })

def pdf_document_public_view(request, pk):
    pdf_document = get_object_or_404(PDFDocument, pk=pk)
    return redirect(pdf_document.file.url)

def email_public_view(request, pk):
    email = get_object_or_404(Email, pk=pk)
    
    raw_body = email.body_plain_text or ""
    body_lines = raw_body.splitlines()
    cleaned_lines = [line for line in body_lines if not line.strip().startswith('>')]
    cleaned_body = "\n".join(cleaned_lines)
    
    # Order quotes by creation date (ascending)
    quotes = email.quotes.all().order_by('created_at')
    
    return render(request, 'core/public_email.html', {
        'email': email,
        'cleaned_body': cleaned_body,
        'quotes': quotes
    })

def document_public_view(request, pk):
    document = get_object_or_404(Document, pk=pk)
    nodes = document.nodes.filter(depth__gt=1).prefetch_related('content_object').order_by('path')
    
    formatted_list = []
    counters = {2: 0, 3: 0, 4: 0}
    for node in nodes:
        depth = node.depth
        if depth == 2:
            counters[2] += 1
            counters[3] = 0
            counters[4] = 0
            node.numbering = f"{counters[2]}."
        elif depth == 3:
            counters[3] += 1
            counters[4] = 0
            node.numbering = f"{chr(96 + counters[3])}."
        elif depth == 4:
            counters[4] += 1
            roman_map = {1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v'}
            node.numbering = f"{roman_map.get(counters[4], counters[4])}."
        else:
            node.numbering = ""
        node.indent_pixels = (depth - 2) * 40  # Adjust indent since we start from depth 2
        formatted_list.append(node)
        
    return render(request, 'core/public_document.html', {
        'document': document,
        'formatted_nodes': formatted_list
    })

class GenerateGlobalTimelineView(View):
    def get(self, request, *args, **kwargs):
        # 1. Find or Create the Master Case
        master_case, created = LegalCase.objects.get_or_create(
            title="MASTER ARCHIVE - ALL EVIDENCE"
        )
        
        # 2. Run the rebuild service
        try:
            count = rebuild_global_exhibits(master_case.pk)
            messages.success(request, f"Global Timeline updated! {count} items indexed.")
        except Exception as e:
            messages.error(request, f"Error generating timeline: {e}")

        # 3. Redirect to the STANDARD Case Detail view
        # This leverages your existing template, Word export, and Zip download!
        return redirect('case_manager:case_detail', pk=master_case.pk)

# ---------------------------------------------------------------------------
# Champs de texte éditables en place
# ---------------------------------------------------------------------------

@require_POST
def ajax_maj_champ(request, app_label, modele, pk, champ):
    """
    Enregistre un champ de texte, quel que soit le modèle qui le porte.

    Un seul point d'entrée plutôt qu'un par champ et par application : le
    comportement d'édition doit être le même sur la page d'un fil, d'un
    courriel, d'un document ou d'une trame, et pour l'analyse comme pour la
    note, le résumé ou la description. Les quatre vues qui faisaient chacune ce
    travail pour un champ ont été supprimées ; l'une d'elles avait dérivé et
    perdait le texte saisi.

    Ce qui est exposé, c'est le modèle qui le dit — voir `ChampsEditables`. La
    liste ne peut pas vivre ici : une liste par nom de champ ouvrirait tous les
    homonymes du projet.

    Rien d'autre n'est touché — en particulier pas `analyse_source`, qui dit
    d'où un texte vient et non ce qu'il est devenu : une fois l'analyse
    modifiée ici, la base et le fichier divergent, et c'est précisément ce que
    ce champ permet de constater.
    """
    try:
        modele_classe = apps.get_model(app_label, modele)
    except (LookupError, ValueError):
        return JsonResponse({'success': False, 'error': "modèle inconnu"}, status=404)

    declares = getattr(modele_classe, 'champs_editables', {})
    if champ not in declares:
        return JsonResponse({'success': False, 'error': "champ non éditable"}, status=400)

    # L'horodatage est facultatif. `analyse` et `note` en portent un parce
    # qu'on veut savoir quand le texte a divergé du fichier importé ; `resume`
    # et `description` n'en ont jamais eu, et leur en imposer un aurait voulu
    # dire une migration par modèle pour une date que rien n'affiche.
    horodatage = declares[champ]
    champs = {f.name for f in modele_classe._meta.get_fields()}
    requis = {champ} | ({horodatage} if horodatage else set())
    if not requis <= champs:
        return JsonResponse(
            {'success': False, 'error': f"ce modèle ne porte pas « {champ} »"}, status=400)

    objet = get_object_or_404(modele_classe, pk=pk)
    try:
        donnees = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': "JSON invalide"}, status=400)

    setattr(objet, champ, donnees.get('contenu', ''))
    ecrits = [champ]
    if horodatage:
        setattr(objet, horodatage, timezone.now())
        ecrits.append(horodatage)
    objet.save(update_fields=ecrits)

    reponse = {'success': True}
    if horodatage:
        reponse['maj'] = getattr(objet, horodatage).strftime('%d %B %Y, %H:%M')
    return JsonResponse(reponse)
