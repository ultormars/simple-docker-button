import os
import psycopg2
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "proje_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "sifre123")

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(1)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tiklamalar (
            id SERIAL PRIMARY KEY,
            zaman TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def ana_sayfa():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tiklamalar;")
    toplam_tiklama = cur.fetchone()[0]
    cur.close()
    conn.close()
    return render_template('index.html', toplam_tiklama=toplam_tiklama)

@app.route('/tikla', methods=['POST'])
def tikla():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tiklamalar DEFAULT VALUES;")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM tiklamalar;")
    yeni_sayi = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    return jsonify({"yeni_sayi": yeni_sayi})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)