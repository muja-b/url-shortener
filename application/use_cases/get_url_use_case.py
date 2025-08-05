from typing import Dict, Any, Optional, Tuple
from domains.url_shortening.services.url_shortening_service import UrlShorteningService

class GetUrlUseCase:
    """Use case for retrieving a URL by its short code."""
    
    def __init__(self, shortening_service: UrlShorteningService):
        self.shortening_service = shortening_service
    
    def execute(self, short_code: str) -> Tuple[Optional[Dict[str, Any]], int]:
        """
        Execute the get URL use case.
        
        Args:
            short_code: The short code to look up
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            shortened_url = self.shortening_service.get_by_short_code(short_code)
            if shortened_url:
                return {
                    'original_url': str(shortened_url.original_url),
                    'short_code': str(shortened_url.short_code)
                }, 200
            else:
                return {'error': 'URL not found'}, 404
        except Exception as e:
            return {'error': 'Internal server error'}, 500 