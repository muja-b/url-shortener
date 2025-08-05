from flask import request, jsonify, render_template, g

def register_routes(app):
    """Register all routes with the Flask application."""
    
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
        if not data or 'original_url' not in data:
            return jsonify({"error": "original_url is required"}), 400
        
        response_data, status_code = g.shorten_url_use_case.execute(data['original_url'])
        return jsonify(response_data), status_code
    
    @app.route('/api/url/<string:short_code>', methods=['GET'])
    def get_url(short_code):
        """Get the original URL for a short code."""
        response_data, status_code = g.get_url_use_case.execute(short_code)
        return jsonify(response_data), status_code
    
    @app.route('/api/url/<string:short_code>', methods=['DELETE'])
    def delete_url(short_code):
        """Delete a shortened URL."""
        response_data, status_code = g.delete_url_use_case.execute(short_code)
        return jsonify(response_data), status_code 