import hashlib
from typing import Callable

class HashService:
    """Service for hash generation logic."""
    
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    def __init__(self):
        pass
    
    def generate_rolling_hash(self, url: str, length: int = 8) -> str:
        """Generate short code using rolling hash."""
        hash_value = 0
        p = 53  # a small prime number
        m = 2**32  # modulus to avoid overflow
        for c in url:
            hash_value = (hash_value * p + ord(c)) % m
        return self._encode_base64(hash_value, length)
    
    def generate_sha256_hash(self, url: str, length: int = 8) -> str:
        """Generate short code using SHA-256."""
        sha256_hash = hashlib.sha256(url.encode('utf-8')).digest()
        # Convert the first length * 6 bits to an integer (since each base64 char encodes 6 bits)
        num_bits = length * 6
        hash_int = int.from_bytes(sha256_hash, 'big') >> (256 - num_bits)
        return self._encode_base64(hash_int, length)
    
    def _encode_base64(self, num: int, length: int) -> str:
        """Encode a number to a string using the custom BASE64_CHARS."""
        chars = []
        for _ in range(length):
            chars.append(self.BASE64_CHARS[num % 64])
            num //= 64
        return ''.join(reversed(chars))
    
    def get_hash_functions(self) -> list[Callable[[str], str]]:
        """Get list of hash functions to try in order."""
        return [
            self.generate_rolling_hash,
            self.generate_sha256_hash
        ] 