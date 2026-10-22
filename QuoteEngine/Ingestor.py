"""Select an ingestor to parse quotes of a file."""                      # CSVIngestor.py


from typing import List

from .Quote import Quote
from .IngestorInterface import IngestorInterface
from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .TXTIngestor import TXTIngestor


class Ingestor(IngestorInterface):
    """Select the right ingestor for a file and parse it."""

    ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TXTIngestor]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a file using the first Ingestor that supports its type.

        Args:
            path: Path to the file to parse.
        Returns:
            A list of quote objects.
        Raises:
            Exception: If no ingestor supports the file type, or if
            the chosen ingestor fails to parse the file.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)

        raise Exception(f'no ingestor available for file: {path}')


if __name__ == "__main__":
    result = Ingestor.parse('./_data/DogQuotes/DogQuotesDOCX.docx')
    print(result)
