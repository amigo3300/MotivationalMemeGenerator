"""Define the Quote class that holds a quote and its author."""

class Quote():
    """A quote and who said it."""

    def __init__(self, body, author):
        """Create a quote.

        Args:
            body: the text of the quote
            author: the name of the person quoted
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Return a readable representation of the quote."""
        return f'<{self.body} - {self.author}>'
