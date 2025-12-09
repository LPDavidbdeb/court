from django.shortcuts import render, get_object_or_404
from argument_manager.models import TrameNarrative

def index(request):
    return render(request, 'core/index.html')

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
    
    return render(request, 'core/story_cinematic.html', {
        'trame': trame,
        'timeline': timeline
    })
