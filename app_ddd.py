from infrastructure.web.flask_app import create_app
from infrastructure.web.routes import register_routes

def main():
    """Main application entry point."""
    app = create_app()
    register_routes(app)
    return app

if __name__ == '__main__':
    app = main()
    app.run(debug=True, host='0.0.0.0', port=5000) 