from domains.url_shortening.services.url_shortening_service import UrlShorteningService
from domains.url_shortening.services.hash_service import RollingHashService, SHA256HashService
from infrastructure.database.postgres_repository import PostgresUrlRepository
from application.use_cases.shorten_url_use_case import ShortenUrlUseCase
from application.use_cases.get_url_use_case import GetUrlUseCase
from application.use_cases.delete_url_use_case import DeleteUrlUseCase

class Container:
    """Simple dependency injection container."""
    
    def __init__(self, db_connection, db_cursor):
        self.db_conn = db_connection
        self.db_cur = db_cursor
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all services and use cases."""
        # Create repository
        self.repository = PostgresUrlRepository(self.db_conn, self.db_cur)
        
        # Create hash services
        self.primary_hash_service = RollingHashService()
        self.fallback_hash_service = SHA256HashService()
        
        # Create domain service
        self.shortening_service = UrlShorteningService(
            repository=self.repository,
            primary_hash_service=self.primary_hash_service,
            fallback_hash_service=self.fallback_hash_service
        )
        
        # Create use cases
        self.shorten_url_use_case = ShortenUrlUseCase(self.shortening_service)
        self.get_url_use_case = GetUrlUseCase(self.shortening_service)
        self.delete_url_use_case = DeleteUrlUseCase(self.shortening_service) 