import hashlib
import psycopg2
from typing import Optional, Tuple
from .hash_service import HashService
from .url_repository import UrlRepository

class UrlService:
    """Service for URL shortening business logic - orchestrates hash and repository services."""
    
    def __init__(self, db_conn, db_cursor):
        self.hash_service = HashService()
        self.repository = UrlRepository(db_conn, db_cursor)
    
    def shorten_url(self, original_url: str) -> Tuple[str, int]:
        """
        Shorten a URL with collision handling.
        Returns (short_code, status_code) where status_code is 201 for new, 200 for existing.
        """
        # Try each hash function until one works
        for hash_func in self.hash_service.get_hash_functions():
            short_code = hash_func(original_url)
            result = self.repository.save_url(original_url, short_code)
            
            if result[0] and result[1] in (200, 201):
                return result
        
        # All hash functions failed
        raise ValueError("Hash collision could not be resolved")
    
    def get_original_url(self, short_code: str) -> Optional[str]:
        """Retrieve a shortened URL by its short code."""
        shortened_url = self.repository.find_by_short_code(short_code)
        return str(shortened_url.original_url) if shortened_url else None
    
    def delete_url(self, short_code: str) -> bool:
        """Delete a URL by its short code. Returns True if deleted."""
        return self.repository.delete_by_short_code(short_code) 