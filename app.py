from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

conn = sqlite3.connect('nano_path.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS Path(
        url_id TEXT PRIMARY KEY,
        original_url TEXT
    )
''')

conn.commit()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        original_url = request.form['original_url']
        url_id = create_short_url(original_url)
        current_url = request.url
        short_url = current_url + url_id

        return redirect(url_for('generated_url', short_url=short_url))

    else:
        return render_template('home.html')


@app.route('/generated_url')
def generated_url():
    short_url = request.args.get('short_url')
    return render_template('short_url.html', short_url=short_url)


@app.route('/<url_id>')
def redirect_user(url_id):
    return redirects(url_id)


def create_short_url(original_url):
    conn = sqlite3.connect('nano_path.db')
    c = conn.cursor()

    characters = "ABCEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    url_id = "".join(random.choice(characters) for _ in range(6))
    c.execute("INSERT INTO Path (url_id, original_url) VALUES (?, ?)", (url_id, original_url))
    conn.commit()

    return url_id


def redirects(url_id):
    conn = sqlite3.connect('nano_path.db')
    c = conn.cursor()

    c.execute("SELECT original_url from Path where url_id = (?)", (url_id,))
    result = c.fetchone()
    if result is not None:
        return redirect(result[0])
    else:
        return "Url Not Found", 404


if __name__ == '__main__':
    app.run(debug=True)
