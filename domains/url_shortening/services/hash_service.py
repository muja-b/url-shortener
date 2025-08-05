import hashlib
from abc import ABC, abstractmethod
from typing import Protocol

class HashService(Protocol):
    """Protocol for hash services."""
    
    def generate_code(self, url: str, length: int = 8) -> str:
        """Generate a short code for the given URL."""
        ...

class RollingHashService:
    """Service for generating short codes using rolling hash."""
    
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    def generate_code(self, url: str, length: int = 8) -> str:
        """Generate a short code using rolling hash."""
        hash_value = self._rolling_hash(url)
        return self._encode_to_custom_base64(hash_value, length)
    
    def _rolling_hash(self, s: str) -> int:
        """Compute a simple rolling hash for the input string."""
        hash_value = 0
        p = 53  # a small prime number
        m = 2**32  # modulus to avoid overflow
        for c in s:
            hash_value = (hash_value * p + ord(c)) % m
        return hash_value
    
    def _encode_to_custom_base64(self, num: int, length: int) -> str:
        """Encode a number to a string using the custom BASE64_CHARS."""
        chars = []
        for _ in range(length):
            chars.append(self.BASE64_CHARS[num % 64])
            num //= 64
        return ''.join(reversed(chars))

class SHA256HashService:
    """Service for generating short codes using SHA-256."""
    
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    def generate_code(self, url: str, length: int = 8) -> str:
        """Generate a short code using SHA-256."""
        sha256_hash = hashlib.sha256(url.encode('utf-8')).digest()
        # Convert the first length * 6 bits to an integer
        num_bits = length * 6
        hash_int = int.from_bytes(sha256_hash, 'big') >> (256 - num_bits)
        return self._encode_to_custom_base64(hash_int, length)
    
    def _encode_to_custom_base64(self, num: int, length: int) -> str:
        """Encode a number to a string using the custom BASE64_CHARS."""
        chars = []
        for _ in range(length):
            chars.append(self.BASE64_CHARS[num % 64])
            num //= 64
        return ''.join(reversed(chars)) 