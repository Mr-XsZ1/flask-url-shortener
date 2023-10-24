import random
from flask import Flask, request, jsonify, redirect, g
from datetime import datetime
import sqlite3

"""
Apa Yg Baru?
Add db sqlite3 
Fix error redirect 

Script By https://github.com/jepluk/flask-url-shortener
Mod script By Mr-XsZ
Telegram : https://t.me/Termuxzts

"""

app = Flask(__name__)

# Setiing SQLite database
conn = sqlite3.connect('url.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT,
        short_url TEXT
    )
''')
conn.commit()



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('url.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def store(url):
    db = get_db()
    cursor = db.cursor()
    
    # Hasilkan URL pendek yang unik
    while True:
        patch = ''.join(random.sample("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 6))
        cursor.execute('SELECT COUNT(*) FROM urls WHERE short_url = ?', (patch,))
        count = cursor.fetchone()[0]
        if count == 0:
            # URL pendek itu unik, masukkan ke dalam database
            cursor.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (url, patch))
            db.commit()
            return patch


def filter(url):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT short_url FROM urls WHERE long_url = ?', (url,))
    result = cursor.fetchone()
    cursor.close()  # Tutup db setelah mengambil hasilnya
    if result:
        return result[0]
    else:
        return store(url)



# api
# usage? host/create?url=https://youtube.com
@app.route('/create', methods=['GET'])
def create_patch(status=False):
    url = request.args.get('url')
    if url.startswith('https://') or url.startswith('http://'):
        return jsonify({'author': 'Mr-XsZ', 'status': False, 'data': {'long_url': url, 'short_url': None}})
    patch = filter(url)
    return jsonify({'author': 'Mr-XsZ', 'status': True, 'data': {'long_url': url, 'short_url': f'{request.url_root}{patch}'}})


# redirect ke url panjang
@app.route('/<patch>')
def gass(patch):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_url = ?', (patch,))
    result = cursor.fetchone()
    if result:
        long_url = result['long_url']
        #print(long_url)
        return redirect(f"https://{long_url}")
    else:
        return "Short URL not found", 404




# patch : /create?url=https://urlnya.com
# http://127.0.0.1:5000/create?url=https://google.com


# Tutup koneksi SQLite ketika aplikasi / script dihentikan
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()




if __name__ == '__main__':
    app.run(debug=True)
