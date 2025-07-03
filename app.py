from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from db import get_connection
from url_hash import generate_url_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database connection
conn = get_connection()
cur = conn.cursor()

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
    
    cur.execute("INSERT INTO urls (original_url, short_code) VALUES (%s, %s)", (data['original_url'], short_url))
    conn.commit()
    return jsonify({"original_url": data['original_url'], "short_url": short_url}), 201

@app.route('/api/url/<string:short_url>', methods=['GET'])
def get_url(short_url):
    cur.execute("SELECT * FROM urls WHERE short_code = %s", (short_url,))
    url = cur.fetchone()
    if url:
        colnames = [desc[0] for desc in cur.description]
        url_dict = dict(zip(colnames, url))
        return jsonify(url_dict), 200
    return jsonify({"error": "URL not found"}), 404

@app.route('/api/url/<string:short_url>', methods=['DELETE'])
def delete_url(short_url):
    cur.execute("DELETE FROM urls WHERE short_code = %s", (short_url,))
    conn.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "URL not found"}), 404
    return jsonify({"message": "URL deleted successfully"}), 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)