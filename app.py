from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Sample data - you can replace this with a database
urls = [
    {"id": 1, "original_url": "www.google.com", "short_url": "mb1"},
    {"id": 2, "original_url": "www.amazon.com", "short_url": "mb2"},
    {"id": 3, "original_url": "www.cc.com", "short_url": "mb3"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/url', methods=['GET'])
def get_urls():
    return jsonify(urls)

@app.route('/api/url', methods=['POST'])
def post_url():
    data = request.get_json()
    if not data or 'original_url' not in data:
        return jsonify({"error": "original_url is required"}), 400
    
    new_url = {
        "id": len(urls) + 1,
        "original_url": data['original_url'],
        "short_url": "mb" + str(len(urls) + 1)
    }
    urls.append(new_url)
    return jsonify(new_url), 201

@app.route('/api/url/<string:short_url>', methods=['GET'])
def get_url(short_url):
    for url in urls:
        if url['short_url'] == short_url:
            return jsonify(url), 200
    return jsonify({"error": "URL not found"}), 404

@app.route('/api/url/<string:short_url>', methods=['DELETE'])
def delete_url(short_url):
    for i, url in enumerate(urls):
        if url['short_url'] == short_url:
            deleted_url = urls.pop(i)
            return jsonify(deleted_url), 204
    return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 