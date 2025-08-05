from typing import Dict, Any, Tuple
from domains.url_shortening.services.url_shortening_service import UrlShorteningService

class ShortenUrlUseCase:
    """Use case for shortening a URL."""
    
    def __init__(self, shortening_service: UrlShorteningService):
        self.shortening_service = shortening_service
    
    def execute(self, original_url: str) -> Tuple[Dict[str, Any], int]:
        """
        Execute the URL shortening use case.
        
        Args:
            original_url: The URL to shorten
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            shortened_url, status_code = self.shortening_service.shorten_url(original_url)
            return {
                'original_url': str(shortened_url.original_url),
                'short_code': str(shortened_url.short_code),
                'short_url': str(shortened_url.short_code)  # For API compatibility
            }, status_code
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500 