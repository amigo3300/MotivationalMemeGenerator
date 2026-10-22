"""Ingest quotes from CSV files."""


from typing import List
import pandas

from .Quote import Quote
from .IngestorInterface import IngestorInterface


class CSVIngestor(IngestorInterface):
    """Ingest quotes from CSV files with 'body' and 'author' columns."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Parse a CSV file and return all the quotes it contains.

        Args:
            path: Path to the CSV file.

        Returns:
            A list of Quote objects.

        Raises:
            Exception: If the file type is unsupported, the file is missing,
            or the expected columns are absent.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest this filetype')

        quotes = []

        try:
            df = pandas.read_csv(path, header=0)
            for index, row in df.iterrows():
                new_quote = Quote(row['body'], row['author'])
                quotes.append(new_quote)
        except FileNotFoundError as e:
            raise Exception(f'file not found: {path}') from e
        except KeyError as e:
            raise Exception(f'missing an expected column: {e}') from e

        return quotes


if __name__ == "__main__":
    result = CSVIngestor.parse('./_data/DogQuotes/DogQuotesCSV.csv')
    print(result)
