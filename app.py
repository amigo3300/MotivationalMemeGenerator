"""Flask web app for generating memes."""


import random
import os
import requests
from flask import Flask, render_template, request

from MemeEngine.MemeEngine import MemeEngine
from QuoteEngine.Ingestor import Ingestor
from PIL import UnidentifiedImageError


app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(file))

    images_path = "./_data/photos/dog/"

    extensions = ('.jpg', '.jpeg', '.png', '.gif')
    imgs = []
    for root, dirs, files in os.walk(images_path):
        for name in files:
            if name.lower().endswith(extensions):
                imgs.append(os.path.join(root, name))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)

    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form.get('image_url')

    try:
        image = requests.get(image_url, timeout=10)
        image.raise_for_status()  # raises an error on 404, 500, etc.
    except requests.exceptions.RequestException:
        return 'Could not download that image', 400

    tmp_path = f'./tmp/{random.randint(0, 1000000000)}.jpg'

    with open(tmp_path, 'wb') as f:
        f.write(image.content)

    body = request.form.get('body', 'a quote is missing')
    author = request.form.get('author', 'unknown')

    try:
        path = meme.make_meme(tmp_path, body, author)
    except UnidentifiedImageError:
        return 'That URL doesn\'t point at a valid image.', 400
    finally:
        os.remove(tmp_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
