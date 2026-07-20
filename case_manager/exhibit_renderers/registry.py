# case_manager/exhibit_renderers/registry.py

from .email import EmailRenderer
from .email_thread import EmailThreadRenderer
from .event import EventRenderer
from .manual import ManualRenderer
from .pdf_document import PdfDocumentRenderer
from .photo import PhotoRenderer
from .photo_document import PhotoDocumentRenderer


RENDERERS = {
    "pdf": PdfDocumentRenderer(),
    "photo": PhotoRenderer(),
    "photodoc": PhotoDocumentRenderer(),
    "event": EventRenderer(),
    "email": EmailRenderer(),
    "thread": EmailThreadRenderer(),

    # Temporairement :
    "document": ManualRenderer(),
    "chatsequence": ManualRenderer(),
}
