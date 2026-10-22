"""Ingest quotes from TXT files."""                      # CSVIngestor.py


from multiprocessing.pool import ExceptionWithTraceback
from typing import List

from .Quote import Quote
from .IngestorInterface import IngestorInterface


class TXTIngestor(IngestorInterface):
    """Ingest TXT files with 'body - author' on each line."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a TXT file and return all the quotes it contains.

        Args:
            path: Path to the TXT file.

        Returns:
            A list of Quote objects.

        Raises:
            Exception: If the file type is unsupported, the file
            cannot be opened or decoded, or a line is not in the
            'body - author' format.

        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest this filetype')

        quotes = []

        try:
            with open(path, 'r', encoding='utf-8') as file_ref:
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
        except FileNotFoundError as e:
            raise Exception(f'file not found: {path}') from e
        except UnicodeDecodeError as e:
            raise Exception(f'file is not valid UTF-8 text: {path}') from e
        except OSError as e:
            raise Exception(f'could not read file: {path}') from e

        return quotes


if __name__ == "__main__":
    result = TXTIngestor.parse('./_data/DogQuotes/DogQuotesTXT.txt')
    print(result)
