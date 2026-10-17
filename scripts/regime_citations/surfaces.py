"""
L'inventaire des surfaces mesurées. Fixé avant la première mesure : la liste
est hachée dans chaque sortie (`liste_des_surfaces`), deux mesures ne se
comparent que si ce hachage concorde.

Exclues : les vues qui appellent un service d'IA (analyse, suggestion, audit,
recherche sémantique), qui écrivent des fichiers (production, archive zip) ou
qui ne répondent qu'en POST. Le réseau est de toute façon bloqué pendant la
mesure.
"""


def _pks(modele):
    return list(modele._base_manager.order_by("pk").values_list("pk", flat=True))


def surfaces():
    from argument_manager.models import TrameNarrative
    from case_manager.models import LegalCase, PerjuryContestation
    from document_manager.models import Document
    from email_manager.models import Email, EmailThread
    from email_manager.models import Quote as EmailQuote
    from events.models import Event
    from googlechat_manager.models import ChatSequence
    from pdf_manager.models import PDFDocument
    from pdf_manager.models import Quote as PDFQuote
    from photos.models import PhotoDocument
    from protagonist_manager.models import Protagonist

    s = [
        "/", "/emails/threads/", "/emails/quotes/", "/pdfs/", "/arguments/", "/arguments/grouped/",
        "/arguments/axes/", "/cases/", "/cases/cotes/", "/documents/list/", "/documents/produced/",
        "/documents/perjury-elements/", "/chat/sequences/", "/events/", "/protagonists/", "/causes/",
        "/photos/documents/",
        "/arguments/ajax/get-email-quotes-list/", "/arguments/ajax/get-pdf-quotes-list/",
        "/arguments/ajax/pdf-quotes-for-tinymce/", "/arguments/ajax/all-quotes-for-tinymce/",
        "/arguments/ajax/get-email-threads/", "/arguments/ajax/get-source-pdfs/",
        "/arguments/ajax/get-events-list/", "/arguments/ajax/get-statements-list/",
    ]
    s += [f"/emails/quotes/?page={n}" for n in range(1, 13)]
    # Requêtes de la recherche de preuves : des mots courants, sans rapport avec le dossier.
    for q in ["le", "de", "la", "et", "pour", "avec", "les", "une", "pas", "est"]:
        s.append(f"/documents/ajax/search-evidence/?query={q}")
    for pk in _pks(EmailThread):
        s += [f"/emails/thread/{pk}/", f"/arguments/ajax/get-thread-emails/{pk}/",
              f"/arguments/ajax/all-quotes-for-tinymce/?app=email_manager&modele=emailthread&pk={pk}"]
    avec_citations = set(EmailQuote._base_manager.values_list("email_id", flat=True))
    for pk in _pks(Email):
        s += [f"/emails/email/{pk}/", f"/emails/email/{pk}/print/", f"/email/{pk}/"]
        if pk in avec_citations:
            s += [f"/emails/quote/add/{pk}/",
                  f"/arguments/ajax/all-quotes-for-tinymce/?app=email_manager&modele=email&pk={pk}"]
    for pk in _pks(EmailQuote):
        s += [f"/emails/quote/{pk}/", f"/emails/quote/{pk}/update/", f"/emails/quote/{pk}/delete/"]
    for pk in _pks(PDFDocument):
        s += [f"/pdfs/pdf/{pk}/", f"/pdfs/pdf/{pk}/create_quote/", f"/pdf/{pk}/",
              f"/arguments/ajax/get-pdf-viewer/{pk}/",
              f"/arguments/ajax/all-quotes-for-tinymce/?app=pdf_manager&modele=pdfdocument&pk={pk}"]
    for pk in _pks(PDFQuote):
        s += [f"/pdfs/quote/{pk}/", f"/pdfs/quote/{pk}/delete/"]
    for pk in _pks(TrameNarrative):
        s += [f"/arguments/{pk}/", f"/arguments/{pk}/update/", f"/arguments/{pk}/affidavit/",
              f"/arguments/narrative/{pk}/manage-perjury/", f"/arguments/{pk}/ajax_get_photo_documents/",
              f"/arguments/{pk}/ajax_get_chat_sequences/", f"/story/{pk}/", f"/histoire/cinematique/{pk}/",
              f"/admin/argument_manager/tramenarrative/{pk}/change/"]
    for pk in _pks(LegalCase):
        s += [f"/cases/{pk}/", f"/cases/{pk}/protagonists/", f"/cases/{pk}/export/",
              f"/cases/{pk}/export-llm/", f"/cases/{pk}/export-police/"]
    for pk in _pks(PerjuryContestation):
        s += [f"/cases/contestations/{pk}/", f"/cases/contestations/{pk}/manage-narratives/",
              f"/cases/contestations/{pk}/manage-statements/", f"/cases/contestations/{pk}/preview/",
              f"/cases/contestations/{pk}/preview-police/"]
    for pk in _pks(Document):
        for vue in ["detail", "update", "interactive", "clean", "cinematic", "schema", "backbone", "contestation"]:
            s.append(f"/documents/{vue}/{pk}/")
        s += [f"/documents/produced/editor/{pk}/", f"/document/{pk}/"]
    for pk in _pks(Protagonist):
        s.append(f"/protagonists/{pk}/")
    for pk in _pks(Event):
        s.append(f"/events/{pk}/")
    for pk in _pks(ChatSequence):
        s.append(f"/chat/sequences/{pk}/")
    for pk in _pks(PhotoDocument):
        s.append(f"/photos/document/{pk}/")
    return s
