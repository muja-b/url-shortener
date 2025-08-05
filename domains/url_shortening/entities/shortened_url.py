from datetime import datetime
from typing import Optional
from ..value_objects.original_url import OriginalUrl
from ..value_objects.short_code import ShortCode

class ShortenedUrl:
    """Entity representing a shortened URL with business rules."""
    
    def __init__(self, original_url: OriginalUrl, short_code: ShortCode, 
                 created_at: Optional[datetime] = None, id: Optional[int] = None):
        self.original_url = original_url
        self.short_code = short_code
        self.created_at = created_at or datetime.utcnow()
        self.id = id
    
    @classmethod
    def create(cls, original_url: str, short_code: str, id: Optional[int] = None) -> 'ShortenedUrl':
        """Factory method to create a new ShortenedUrl with validation."""
        original_url_vo = OriginalUrl(original_url)
        short_code_vo = ShortCode(short_code)
        return cls(original_url_vo, short_code_vo, id=id)
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary for API responses."""
        return {
            'id': self.id,
            'original_url': str(self.original_url),
            'short_code': str(self.short_code),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ShortenedUrl):
            return False
        return (self.original_url == other.original_url and 
                self.short_code == other.short_code)
    
    def __hash__(self) -> int:
        return hash((self.original_url, self.short_code))
    
    def __str__(self) -> str:
        return f"ShortenedUrl(original_url={self.original_url}, short_code={self.short_code})" 