from typing import List, Optional, Tuple
from ..entities.shortened_url import ShortenedUrl
from ..value_objects.original_url import OriginalUrl
from ..value_objects.short_code import ShortCode
from .hash_service import HashService, RollingHashService, SHA256HashService
from ..repositories.url_repository import UrlRepository

class UrlShorteningService:
    """Domain service for URL shortening business logic."""
    
    def __init__(self, repository: UrlRepository, 
                 primary_hash_service: HashService = None,
                 fallback_hash_service: HashService = None):
        self.repository = repository
        self.primary_hash_service = primary_hash_service or RollingHashService()
        self.fallback_hash_service = fallback_hash_service or SHA256HashService()
    
    def shorten_url(self, original_url: str) -> Tuple[ShortenedUrl, int]:
        """
        Shorten a URL with collision handling.
        Returns (ShortenedUrl, status_code) where status_code is 201 for new, 200 for existing.
        """
        original_url_vo = OriginalUrl(original_url)
        
        # Try primary hash service
        short_code, status = self._try_with_hash_service(original_url_vo, self.primary_hash_service)
        if short_code and status in (200, 201):
            return short_code, status
        
        # Try fallback hash service
        short_code, status = self._try_with_hash_service(original_url_vo, self.fallback_hash_service)
        if short_code and status in (200, 201):
            return short_code, status
        
        # Both hash services failed
        raise ValueError("Hash collision could not be resolved")
    
    def _try_with_hash_service(self, original_url: OriginalUrl, hash_service: HashService) -> Tuple[Optional[ShortenedUrl], Optional[int]]:
        """Try to create a shortened URL using the given hash service."""
        try:
            code_value = hash_service.generate_code(str(original_url))
            short_code_vo = ShortCode(code_value)
            
            # Try to save to repository
            shortened_url = ShortenedUrl(original_url, short_code_vo)
            saved_url = self.repository.save(shortened_url)
            
            if saved_url.id:  # New record
                return saved_url, 201
            else:  # Existing record
                return saved_url, 200
                
        except ValueError as e:
            # Collision occurred
            return None, None
    
    def get_by_short_code(self, short_code: str) -> Optional[ShortenedUrl]:
        """Retrieve a shortened URL by its short code."""
        try:
            short_code_vo = ShortCode(short_code)
            return self.repository.find_by_short_code(short_code_vo)
        except ValueError:
            return None
    
    def delete_by_short_code(self, short_code: str) -> bool:
        """Delete a shortened URL by its short code."""
        try:
            short_code_vo = ShortCode(short_code)
            return self.repository.delete_by_short_code(short_code_vo)
        except ValueError:
            return False
    
    def get_all_urls(self) -> List[ShortenedUrl]:
        """Get all shortened URLs."""
        return self.repository.find_all() 