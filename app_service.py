from flask import Flask, request, jsonify, render_template, g
import os
import validators
from db import get_connection, put_connection
from services.url_service import UrlService

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.before_request
def before_request():
    """Set up database connection and service before each request."""
    g.db_conn = get_connection()
    g.db_cur = g.db_conn.cursor()
    g.url_service = UrlService(g.db_conn, g.db_cur)

@app.teardown_request
def teardown_request(exception):
    """Clean up database connections after each request."""
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
    """Create a shortened URL."""
    data = request.get_json()
    if not data or 'original_url' not in data or not validators.url(data['original_url']):
        return jsonify({"error": "original_url is required and must be a valid URL"}), 400
    
    try:
        short_code, status_code = g.url_service.shorten_url(data['original_url'])
        return jsonify({
            "original_url": data['original_url'],
            "short_url": short_code
        }), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/url/<string:short_code>', methods=['GET'])
def get_url(short_code):
    """Get the original URL for a short code."""
    original_url = g.url_service.get_original_url(short_code)
    if original_url:
        return jsonify({
            "original_url": original_url,
            "short_code": short_code
        }), 200
    return jsonify({"error": "URL not found"}), 404

@app.route('/api/url/<string:short_code>', methods=['DELETE'])
def delete_url(short_code):
    """Delete a shortened URL."""
    success = g.url_service.delete_url(short_code)
    if success:
        return jsonify({"message": "URL deleted successfully"}), 204
    return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 