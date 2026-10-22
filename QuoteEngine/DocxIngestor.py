"""Ingest quotes from Docx files."""


from typing import List
import docx
from docx.opc.exceptions import PackageNotFoundError

from .Quote import Quote
from .IngestorInterface import IngestorInterface


class DocxIngestor(IngestorInterface):
    """Ingest quotes from Docx files with 'body - author' on each line."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a Docx file and return all the quotes it contains.

        Args:
            path: Path to a Doc file.

        Returns:
            A list of Quote objects.

        Raises:
            Exception: if file is unsupported or is missing or not a valid
            Docx file, or a line is not in the 'body - author' format.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest this filetype')

        quotes = []

        try:
            doc = docx.Document(path)
        except PackageNotFoundError as e:
            raise Exception(f'file is missing or not a valid docx: {path}') \
                from e

        for para in doc.paragraphs:
            if para.text != "":
                try:
                    parse = para.text.split(' - ')
                    new_quote = Quote(parse[0], parse[1])
                except IndexError as e:
                    raise Exception(f'line not in "body - author" format:'
                                    f'{para.text}') from e
                quotes.append(new_quote)

        return quotes


if __name__ == "__main__":
    result = DocxIngestor.parse('./_data/DogQuotes/DogQuotesDOCX.docx')
    print(result)
