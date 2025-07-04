from flask import Flask, render_template, request, jsonify, g
import os

import psycopg2
from db import get_connection, put_connection
from url_hash import generate_url_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.before_request
def before_request():
    g.db_conn = get_connection()
    g.db_cur = g.db_conn.cursor()

@app.teardown_request
def teardown_request(exception):
    db_conn = getattr(g, 'db_conn', None)
    db_cur = getattr(g, 'db_cur', None)
    if db_cur is not None:
        db_cur.close()
    if db_conn is not None:
        if exception:
            db_conn.rollback()
        else:
            db_conn.commit()
        put_connection(db_conn)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/url', methods=['POST'])
def post_url():
    data = request.get_json()
    if not data or 'original_url' not in data:
        return jsonify({"error": "original_url is required"}), 400
    
    short_url = generate_url_hash(data['original_url'])
    try:
        g.db_cur.execute("INSERT INTO urls (original_url, short_code) VALUES (%s, %s)", (data['original_url'], short_url))
        g.db_conn.commit()
        return jsonify({"original_url": data['original_url'], "short_url": short_url}), 201        
    except psycopg2.IntegrityError:
        return jsonify({"error": "URL already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/url/<string:short_url>', methods=['GET'])
def get_url(short_url):
    g.db_cur.execute("SELECT original_url, short_code FROM urls WHERE short_code = %s", (short_url,))
    url = g.db_cur.fetchone()
    if url:
        url_dict = dict(zip(("original_url", "short_code"), url))
        return jsonify(url_dict), 200
    return jsonify({"error": "URL not found"}), 404

@app.route('/api/url/<string:short_url>', methods=['DELETE'])
def delete_url(short_url):
    g.db_cur.execute("DELETE FROM urls WHERE short_code = %s", (short_url,))
    g.db_conn.commit()
    if g.db_cur.rowcount == 0:
        return jsonify({"error": "URL not found"}), 404
    return jsonify({"message": "URL deleted successfully"}), 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)