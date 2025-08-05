from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.shortened_url import ShortenedUrl
from ..value_objects.short_code import ShortCode
from ..value_objects.original_url import OriginalUrl

class UrlRepository(ABC):
    """Abstract repository interface for URL data access."""
    
    @abstractmethod
    def save(self, shortened_url: ShortenedUrl) -> ShortenedUrl:
        """
        Save a shortened URL.
        Returns the saved entity with ID if it's a new record.
        Returns the existing entity if it already exists.
        """
        pass
    
    @abstractmethod
    def find_by_short_code(self, short_code: ShortCode) -> Optional[ShortenedUrl]:
        """Find a shortened URL by its short code."""
        pass
    
    @abstractmethod
    def find_by_original_url(self, original_url: OriginalUrl) -> Optional[ShortenedUrl]:
        """Find a shortened URL by its original URL."""
        pass
    
    @abstractmethod
    def delete_by_short_code(self, short_code: ShortCode) -> bool:
        """Delete a shortened URL by its short code. Returns True if deleted."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[ShortenedUrl]:
        """Find all shortened URLs."""
        pass
    
    @abstractmethod
    def exists_by_short_code(self, short_code: ShortCode) -> bool:
        """Check if a short code already exists."""
        pass 