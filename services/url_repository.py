import psycopg2
from typing import Optional, Tuple

class UrlRepository:
    """Repository for URL database operations."""
    
    def __init__(self, db_conn, db_cursor):
        self.db_conn = db_conn
        self.db_cur = db_cursor
    
    def save_url(self, original_url: str, short_code: str) -> Tuple[str, int]:
        """
        Save a URL mapping to the database.
        Returns (short_code, status_code) where status_code is 201 for new, 200 for existing.
        """
        try:
            self.db_cur.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)",
                (original_url, short_code)
            )
            self.db_conn.commit()
            return short_code, 201
            
        except psycopg2.IntegrityError:
            self.db_conn.rollback()
            
            self.db_cur.execute(
                "SELECT original_url FROM urls WHERE short_code = %s",
                (short_code,)
            )
            existing = self.db_cur.fetchone()
            
            if existing and existing[0] == original_url:
                return short_code, 200
            
            return None, None
    
    def get_original_url(self, short_code: str) -> Optional[str]:
        """Get the original URL for a short code."""
        self.db_cur.execute(
            "SELECT original_url FROM urls WHERE short_code = %s",
            (short_code,)
        )
        result = self.db_cur.fetchone()
        return result[0] if result else None
    
    def delete_url(self, short_code: str) -> bool:
        """Delete a URL by its short code. Returns True if deleted."""
        self.db_cur.execute(
            "DELETE FROM urls WHERE short_code = %s",
            (short_code,)
        )
        self.db_conn.commit()
        return self.db_cur.rowcount > 0
    
    def url_exists(self, short_code: str) -> bool:
        """Check if a short code already exists."""
        self.db_cur.execute(
            "SELECT 1 FROM urls WHERE short_code = %s",
            (short_code,)
        )
        return self.db_cur.fetchone() is not None 