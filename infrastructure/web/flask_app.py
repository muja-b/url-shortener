from flask import Flask, g
import os
from db import get_connection, put_connection
from domains.url_shortening.services.url_shortening_service import UrlShorteningService
from domains.url_shortening.services.hash_service import RollingHashService, SHA256HashService
from infrastructure.database.postgres_repository import PostgresUrlRepository
from application.use_cases.shorten_url_use_case import ShortenUrlUseCase
from application.use_cases.get_url_use_case import GetUrlUseCase
from application.use_cases.delete_url_use_case import DeleteUrlUseCase

def create_app():
    """Create and configure the Flask application with dependency injection."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    @app.before_request
    def before_request():
        """Set up database connection and dependencies before each request."""
        g.db_conn = get_connection()
        g.db_cur = g.db_conn.cursor()
        
        # Create repository
        g.repository = PostgresUrlRepository(g.db_conn, g.db_cur)
        
        # Create hash services
        g.primary_hash_service = RollingHashService()
        g.fallback_hash_service = SHA256HashService()
        
        # Create domain service
        g.shortening_service = UrlShorteningService(
            repository=g.repository,
            primary_hash_service=g.primary_hash_service,
            fallback_hash_service=g.fallback_hash_service
        )
        
        # Create use cases
        g.shorten_url_use_case = ShortenUrlUseCase(g.shortening_service)
        g.get_url_use_case = GetUrlUseCase(g.shortening_service)
        g.delete_url_use_case = DeleteUrlUseCase(g.shortening_service)
    
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
    
    return app 