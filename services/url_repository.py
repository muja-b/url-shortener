import psycopg2
from typing import List, Optional, Tuple
from .redis_service import RedisService
from config import Config

class UrlRepository:
    """Repository for URL database operations with Redis caching."""
    
    def __init__(self, db_conn, db_cursor):
        self.db_conn = db_conn
        self.db_cur = db_cursor
        self.redis_service = RedisService(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            ttl=Config.REDIS_TTL
        )
    
    def save_url(self, original_url: str, short_code: str) -> Tuple[str, int]:
        """
        Save a URL mapping to the database and cache.
        Returns (short_code, status_code) where status_code is 201 for new, 200 for existing.
        """
        # Check cache first for quick response
        cached_url = self.redis_service.get_original_url(short_code)
        if cached_url == original_url:
            return short_code, 200  # Already exists
        elif cached_url:
            return None, None  # Collision detected
        
        try:
            # Try to insert new record
            self.db_cur.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)",
                (original_url, short_code)
            )
            self.db_conn.commit()
            self.redis_service.set_url_mapping(short_code, original_url)
            return short_code, 201
            
        except psycopg2.IntegrityError:
            self.db_conn.rollback()
            
            # Check if same URL exists with different code
            existing = self._find_by_original_url_db(original_url)
            if existing:
                self.redis_service.set_url_mapping(existing, original_url)
                return existing, 200
            
            return None, None  # Collision occurred
    
    def find_by_short_code(self, short_code: str) -> Optional['ShortenedUrl']:
        """Find a shortened URL by its short code (cache-first)."""
        # Try cache first
        cached_url = self.redis_service.get_original_url(short_code)
        if cached_url:
            return self._create_entity(short_code, cached_url)
        
        # Cache miss - query database
        result = self._find_by_short_code_db(short_code)
        if result:
            self.redis_service.set_url_mapping(short_code, result[1])
            return self._create_entity(result[2], result[1], result[0])
        
        return None
    
    def delete_by_short_code(self, short_code: str) -> bool:
        """Delete a URL by its short code and remove from cache."""
        self.db_cur.execute("DELETE FROM urls WHERE short_code = %s", (short_code,))
        self.db_conn.commit()
        
        if self.db_cur.rowcount > 0:
            self.redis_service.delete_url_mapping(short_code)
            return True
        return False
    
    def exists_by_short_code(self, short_code: str) -> bool:
        """Check if a short code already exists (cache-first)."""
        return self.redis_service.get_original_url(short_code) is not None or self._exists_in_db(short_code)
    
    # Private helper methods
    def _find_by_short_code_db(self, short_code: str) -> Optional[tuple]:
        """Database query for finding by short code."""
        self.db_cur.execute(
            "SELECT id, original_url, short_code FROM urls WHERE short_code = %s",
            (short_code,)
        )
        return self.db_cur.fetchone()
    
    def _find_by_original_url_db(self, original_url: str) -> Optional[str]:
        """Database query for finding short code by original URL."""
        self.db_cur.execute(
            "SELECT short_code FROM urls WHERE original_url = %s",
            (original_url,)
        )
        result = self.db_cur.fetchone()
        return result[0] if result else None
    
    def _exists_in_db(self, short_code: str) -> bool:
        """Check if short code exists in database."""
        self.db_cur.execute("SELECT 1 FROM urls WHERE short_code = %s", (short_code,))
        return self.db_cur.fetchone() is not None
    
    def _create_entity(self, short_code: str, original_url: str, id: int = None) -> 'ShortenedUrl':
        """Create ShortenedUrl entity."""
        from domains.url_shortening.entities.shortened_url import ShortenedUrl
        return ShortenedUrl.create(original_url=original_url, short_code=short_code, id=id)