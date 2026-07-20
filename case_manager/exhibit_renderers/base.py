# case_manager/exhibit_renderers/base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExhibitRenderer(ABC):

    @abstractmethod
    def render(
        self,
        *,
        row,
        sources: list[Any],
        destination: Path,
    ) -> Path:
        """
        Transforme une cote procédurale complète en un seul PDF.
        """
        raise NotImplementedError
