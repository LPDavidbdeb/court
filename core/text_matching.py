"""
Locating a quotation inside the document it was taken from.

A quote is stored as its own row, so nothing links it back to the spot in the
source it came from except its text. Finding that spot again is what orders
quotes as a reader meets them rather than in the order someone happened to
extract them (see Quote.position_in_source).

A literal search finds the spot only when the stored text is character-for-
character what the source says, and in this corpus it often is not. The sources
are emails and scanned pleadings: the same apostrophe arrives as U+2019 in one
message and as a bare space in the next, accents survive in the body but not in
the extracted text, a comma loses the space after it, and a typo in the original
gets silently corrected on its way into the quote. None of that changes which
passage is meant, so none of it should decide whether the passage can be found.
"""

import difflib
import re
import unicodedata

# Below this, a fuzzy hit is more likely to be a coincidence than the passage.
_MIN_FUZZY_CHARS = 30
_MIN_FUZZY_COVERAGE = 0.4

# difflib is quadratic in the worst case; on a long source the earlier, cheaper
# strategies are the ones that will succeed anyway.
_MAX_FUZZY_HAYSTACK = 20000

_MIN_ANCHOR_WORDS = 4


def fold_for_matching(text):
    """
    Reduce text to what two renderings of the same passage have in common.

    Strips accents, lowercases, and turns every run of non-alphanumeric
    characters into a single space. That collapses the differences this corpus
    actually exhibits — apostrophe glyphs, accents, stray punctuation, the
    "[...]" elision marker, inconsistent spacing — while keeping word identity,
    which is what distinguishes one passage from another.
    """
    decomposed = unicodedata.normalize('NFD', text or "")
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return " ".join(re.sub(r'[^0-9a-z]+', ' ', stripped.lower()).split())


def locate(haystack, needle):
    """
    Offset of `needle` within `haystack`, or -1. Both must already be folded.

    Three strategies, cheapest first, each catching what the one before it
    cannot:

    1. Literal search, which settles the large majority.
    2. The longest word-aligned prefix of the quote that does occur. A quote
       whose source contains a typo diverges at that typo and matches up to it;
       the prefix still pins the offset, which is all a sort key needs.
    3. The longest block the two have in common, for a quote that diverges too
       early for a prefix to survive. Guarded by a coverage floor so a passage
       that genuinely is not here is reported missing rather than placed
       somewhere arbitrary.

    The offset is in folded coordinates, so it is comparable only between
    quotes matched against the same folded source — which is the only way it
    is used.
    """
    if not haystack or not needle:
        return -1

    index = haystack.find(needle)
    if index >= 0:
        return index

    words = needle.split()
    for count in range(len(words), _MIN_ANCHOR_WORDS - 1, -1):
        index = haystack.find(" ".join(words[:count]))
        if index >= 0:
            return index

    if len(haystack) > _MAX_FUZZY_HAYSTACK:
        return -1

    match = difflib.SequenceMatcher(None, haystack, needle, autojunk=False)\
                   .find_longest_match(0, len(haystack), 0, len(needle))
    if match.size >= _MIN_FUZZY_CHARS and match.size >= _MIN_FUZZY_COVERAGE * len(needle):
        return match.a

    return -1


def order_by_position(quotes):
    """
    Quotes of one source, in the order that source reads.

    Sorting is skipped outright for a source holding a single quote. That is not
    a micro-optimisation: locating a quote means searching the whole transcribed
    document, and `sorted` evaluates the key even for a one-element list, so the
    search ran on every such source only to order it against nothing. Most
    sources are of that kind — 24 of 35 documents and 121 of 158 emails carry
    exactly one quote.

    It also settles what "unlocatable" costs. A quote whose text is a reading of
    a table rather than a passage lifted from it can never be found verbatim,
    but where it is the only quote of its document there is no order for that to
    spoil. Only a source with siblings needs the position at all.

    Returns a list, ordered where ordering means something and untouched where
    it does not.
    """
    quotes = list(quotes)
    if len(quotes) > 1:
        quotes.sort(key=lambda quote: quote.position_in_source)
    return quotes
