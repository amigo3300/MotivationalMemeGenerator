"""Ingest quotes from PDF files."""                      # CSVIngestor.py


from typing import List
import subprocess
import os
import random

from .Quote import Quote
from .IngestorInterface import IngestorInterface


class PDFIngestor(IngestorInterface):
    """Ingest quotes from PDF files with 'body - author on each line."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a PDF file and return all the quotes it contains.

        Args:
            path: Path to a PDF file.

        Returns:
            A list of Quote objects.

        Raises:
            Exception: If the file is unsupported, pdftotext isn't installed,
            the PDF can't be converted, the converted text can't be decoded,
            a line isn't in the 'body - author' format.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest this filetype')

        tmp = f'./tmp/{random.randint(0,1000000000)}.txt'
        quotes = []

        try:
            subprocess.run(['pdftotext', path, tmp],
                           check=True, capture_output=True, text=True)
        except FileNotFoundError as e:
            raise Exception(f'pdftotext is not installed or not on PATH') \
                from e
        except subprocess.CalledProcessError as e:
            raise Exception(f'couldn\'t convert PDF {path}: '
                            f'{e.stderr.strip()}') from e

        try:
            with open(tmp, 'r', encoding='utf-8') as file_ref:
                for line in file_ref:
                    line = line.strip()
                    if len(line) > 0:
                        try:
                            parse = line.split(' - ')
                            new_quote = Quote(parse[0], parse[1])
                        except IndexError as e:
                            raise Exception(f'line not in "body - author" '
                                            f'format: {line}') from e
                        quotes.append(new_quote)
        except UnicodeDecodeError as e:
            raise Exception(f'converted text is not valid UTF-8: {path}') \
                from e
        finally:
            if os.path.exists(path):
                os.remove(tmp)

        return quotes


if __name__ == "__main__":
    result = PDFIngestor.parse('./_data/DogQuotes/DogQuotesPDF.pdf')
    print(result)
