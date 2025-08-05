from typing import Dict, Any, Tuple
from domains.url_shortening.services.url_shortening_service import UrlShorteningService

class DeleteUrlUseCase:
    """Use case for deleting a URL by its short code."""
    
    def __init__(self, shortening_service: UrlShorteningService):
        self.shortening_service = shortening_service
    
    def execute(self, short_code: str) -> Tuple[Dict[str, Any], int]:
        """
        Execute the delete URL use case.
        
        Args:
            short_code: The short code to delete
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            success = self.shortening_service.delete_by_short_code(short_code)
            if success:
                return {'message': 'URL deleted successfully'}, 204
            else:
                return {'error': 'URL not found'}, 404
        except Exception as e:
            return {'error': 'Internal server error'}, 500 