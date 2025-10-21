from .thread import (
    EmailThreadListView,
    EmailThreadDetailView,
    EmailSearchView,
    EmailThreadDeleteView,
    EmailThreadSaveView
)
from .email import (
    EmailDetailView,
    DownloadEmlView,
    EmailPrintableView,
    EmlUploadView,
    create_email_quote, # NEW
    ajax_update_email_quote # NEW
)
from .quote import (
    QuoteDetailView,
    AddQuoteView,
    QuoteListView,
    QuoteDeleteView,
    QuoteUpdateView
)

__all__ = [
    # Thread views
    'EmailThreadListView',
    'EmailThreadDetailView',
    'EmailSearchView',
    'EmailThreadDeleteView',
    'EmailThreadSaveView',

    # Email views
    'EmailDetailView',
    'DownloadEmlView',
    'EmailPrintableView',
    'EmlUploadView',
    'create_email_quote', # NEW
    'ajax_update_email_quote', # NEW

    # Quote views
    'QuoteDetailView',
    'AddQuoteView',
    'QuoteListView',
    'QuoteDeleteView',
    'QuoteUpdateView',
]
