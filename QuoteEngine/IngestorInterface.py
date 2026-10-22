"""Abstract class for all quote file ingestors."""

from abc import ABC, abstractmethod

from typing import List
from .Quote import Quote


class IngestorInterface(ABC):
    """Abstract base class for all quote file ingestors."""

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True if file extension is supported by the ingestor."""
        ext = path.split(".")[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a file and return the quotes it contains.

        Args:
            path: Path to the file to parse.
        Returns:
            A list of quote objects.
        """
        pass
