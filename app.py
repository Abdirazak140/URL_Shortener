from flask import Flask, render_template, request
import sqlite3
import random

conn = sqlite3.connect('nano_path.db')
c = conn.cursor()

app = Flask(__name__)

c.execute('''
    CREATE TABLE Nano_Path(
        short_url TEXT PRIMARY KEY,
        original_url TEXT
    )
''')


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        pass
    else:
        return render_template('home.html')


@app.route('/short_url_generated')
def generated_url():
    return render_template('short_url.html')


def create_short_url(original_url):
    characters = "ABCEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    url_id = "".join(random.choice(characters) for _ in range(6))

    c.execute("INSERT INTO Nano_Path (short_url, original_url) VALUES (?, ?)", (url_id, original_url))
    c.commit()

    return url_id


def redirects(short_url):
    c.execute("")


if __name__ == '__main__':
    app.run(debug=True)
