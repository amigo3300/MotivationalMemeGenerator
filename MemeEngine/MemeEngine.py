"""Generate memes by overlaying quotes on an image."""

import os
import random
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MemeEngine:
    """Generate memes by drawing a quote and its author on an image."""

    def __init__(self, output_dir):
        """Create an engine that saves memes to that given directory.

        Args:
            output_dir: Directory where generated memes are saved.
        """
        self.output_dir = output_dir

    @staticmethod
    def get_random_position(img_width, img_height, text_width, text_height):
        """Return a random (x, y) position that keeps the text in the image.

        If the text is larger than the image in a dimension, that coordinate
        is 0.

        Args:
            :param img_width: Width of the image in pixels.
            :param img_height: Height of the image in pixels.
            :param text_width: Width of the text block in pixels.
            :param text_height: Height of the text block in pixels.

        Returns:
            A tuple (x, y) of integer pixel coordinates.
        """
        max_x = max(0, img_width - text_width)
        max_y = max(0, img_height - text_height)
        return random.randint(0, int(max_x)), random.randint(0, int(max_y))

    @staticmethod
    def measure_text(draw, text, font):
        """Return the (width, height) of the text drawn with the font.

        Args:
            :param draw: The ImageDraw object used to measure the text.
            :param text: The string to measure.
            :param font: The ImageFont used to render the text.

        Return:
            A tuple (width, height) in pixels.
        """
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        return right - left, bottom - top

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Create a meme and return the path to the saved image.

        The image is resized to the given width (keeping its aspect ratio) and
        the the quote is drawn at a random position, with the author on the
        line below.

        Args:
            :param img_path: Path to the source image.
            :param text: The quote body to draw.
            :param author: The quote author to draw.
            :param width: Width in pixels to resize the image to default 500.

        Returns:
            The file path of the generated meme.

        Raises:
            :exception If the image file is missing or is not a valid image.
        """
        try:
            img = Image.open(img_path)
            img = img.convert('RGB')
        except FileNotFoundError as e:
            raise Exception(f'image not found: {img_path}') from e
        except UnidentifiedImageError as e:
            raise Exception(f'not a valid image file: {img_path}') from e

        # resize, keeping aspect ratio
        ratio = width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((width, new_height))

        draw = ImageDraw.Draw(img)

        # add a quote
        quote_font = ImageFont.truetype(
            os.path.join(BASE_DIR, 'fonts', 'Roboto_Condensed-Bold.ttf'),
            size=24
        )
        author_font = ImageFont.truetype(
            os.path.join(BASE_DIR, 'fonts', 'Caveat-Regular.ttf'),
            size=18
        )

        quote_line = f'{text}'
        author_line = f'- {author}'

        tab_indent = 20
        line_spacing = 10

        quote_width, quote_height = self.measure_text(draw, quote_line,
                                                      quote_font)
        author_width, author_height = self.measure_text(draw, author_line,
                                                        author_font)

        max_text_width = max(quote_width, tab_indent + author_width)
        total_text_height = quote_height + line_spacing + author_height

        x, y = MemeEngine.get_random_position(img.width, img.height,
                                              max_text_width,
                                              total_text_height)

        draw.text((x, y), quote_line, font=quote_font, fill="white")
        draw.text((x + tab_indent, y + quote_height + line_spacing),
                  author_line, font=author_font, fill="white")

        out_path = os.path.join(self.output_dir,
                                f'{random.randint(0, 10000000)}.jpg')
        img.save(out_path)

        return out_path
