import re
from typing import Optional

class ShortCode:
    """Value object representing a valid short code."""
    
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError(f"Invalid short code: {value}")
        self.value = value
    
    @staticmethod
    def _is_valid(code: str) -> bool:
        """Validate if the short code meets requirements."""
        if not code or not isinstance(code, str):
            return False
        
        # Check length (6-12 characters)
        if len(code) < 6 or len(code) > 12:
            return False
        
        # Check if it only contains valid characters (base64-like)
        valid_chars = re.compile(r'^[A-Za-z0-9\-_]+$')
        return bool(valid_chars.match(code))
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, ShortCode):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    @property
    def length(self) -> int:
        return len(self.value) 