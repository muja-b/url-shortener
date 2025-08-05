import psycopg2
from typing import List, Optional
from domains.url_shortening.repositories.url_repository import UrlRepository
from domains.url_shortening.entities.shortened_url import ShortenedUrl
from domains.url_shortening.value_objects.short_code import ShortCode
from domains.url_shortening.value_objects.original_url import OriginalUrl

class PostgresUrlRepository(UrlRepository):
    """PostgreSQL implementation of the URL repository."""
    
    def __init__(self, db_connection, db_cursor):
        self.db_conn = db_connection
        self.db_cur = db_cursor
    
    def save(self, shortened_url: ShortenedUrl) -> ShortenedUrl:
        """
        Save a shortened URL.
        Returns the saved entity with ID if it's a new record.
        Returns the existing entity if it already exists.
        """
        try:
            # Try to insert new record
            self.db_cur.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)",
                (str(shortened_url.original_url), str(shortened_url.short_code))
            )
            self.db_conn.commit()
            
            # Get the inserted record with ID
            self.db_cur.execute(
                "SELECT id, original_url, short_code, created_at FROM urls WHERE short_code = %s",
                (str(shortened_url.short_code),)
            )
            result = self.db_cur.fetchone()
            
            if result:
                return ShortenedUrl.create(
                    original_url=result[1],
                    short_code=result[2],
                    id=result[0]
                )
            return shortened_url
            
        except psycopg2.IntegrityError:
            self.db_conn.rollback()
            # Check if it's the same URL
            existing = self.find_by_short_code(shortened_url.short_code)
            if existing and existing.original_url == shortened_url.original_url:
                return existing
            # Check if URL already exists with different code
            existing_by_url = self.find_by_original_url(shortened_url.original_url)
            if existing_by_url:
                return existing_by_url
            raise ValueError("Hash collision occurred")
    
    def find_by_short_code(self, short_code: ShortCode) -> Optional[ShortenedUrl]:
        """Find a shortened URL by its short code."""
        self.db_cur.execute(
            "SELECT id, original_url, short_code, created_at FROM urls WHERE short_code = %s",
            (str(short_code),)
        )
        result = self.db_cur.fetchone()
        
        if result:
            return ShortenedUrl.create(
                original_url=result[1],
                short_code=result[2],
                id=result[0]
            )
        return None
    
    def find_by_original_url(self, original_url: OriginalUrl) -> Optional[ShortenedUrl]:
        """Find a shortened URL by its original URL."""
        self.db_cur.execute(
            "SELECT id, original_url, short_code, created_at FROM urls WHERE original_url = %s",
            (str(original_url),)
        )
        result = self.db_cur.fetchone()
        
        if result:
            return ShortenedUrl.create(
                original_url=result[1],
                short_code=result[2],
                id=result[0]
            )
        return None
    
    def delete_by_short_code(self, short_code: ShortCode) -> bool:
        """Delete a shortened URL by its short code. Returns True if deleted."""
        self.db_cur.execute(
            "DELETE FROM urls WHERE short_code = %s",
            (str(short_code),)
        )
        self.db_conn.commit()
        return self.db_cur.rowcount > 0
    
    def find_all(self) -> List[ShortenedUrl]:
        """Find all shortened URLs."""
        self.db_cur.execute(
            "SELECT id, original_url, short_code, created_at FROM urls ORDER BY created_at DESC"
        )
        results = self.db_cur.fetchall()
        
        return [
            ShortenedUrl.create(
                original_url=result[1],
                short_code=result[2],
                id=result[0]
            )
            for result in results
        ]
    
    def exists_by_short_code(self, short_code: ShortCode) -> bool:
        """Check if a short code already exists."""
        self.db_cur.execute(
            "SELECT 1 FROM urls WHERE short_code = %s",
            (str(short_code),)
        )
        return self.db_cur.fetchone() is not None 