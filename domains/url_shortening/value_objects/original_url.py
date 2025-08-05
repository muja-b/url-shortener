import validators
from typing import Optional

class OriginalUrl:
    """Value object representing a valid original URL."""
    
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError(f"Invalid URL: {value}")
        self.value = value
    
    @staticmethod
    def _is_valid(url: str) -> bool:
        """Validate if the URL is properly formatted."""
        return bool(url and validators.url(url))
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, OriginalUrl):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value) 