import random
import hashlib

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

def generate_random_salt(length=6):
    """
    Generate a random alphanumeric string of base64 characters for use as a salt or code.
    """
    return ''.join(random.choice(BASE64_CHARS) for _ in range(length))

def rolling_hash(s):
    """
    Compute a simple rolling hash for the input string.
    Used to generate a deterministic hash value for a URL.
    """
    hash_value = 0
    p = 53  # a small prime number
    m = 2**32  # modulus to avoid overflow
    for c in s:
        hash_value = (hash_value * p + ord(c)) % m
    return hash_value

def encode_to_custom_base64(num, length):
    """
    Encode a number to a string using the custom BASE64_CHARS, padded/truncated to 'length'.
    """
    chars = []
    for _ in range(length):
        chars.append(BASE64_CHARS[num % 64])
        num //= 64
    return ''.join(reversed(chars))

def generate_short_code(input_url, hash_length=8):
    """
    Generate a deterministic short code for URL shortening.
    Hashes the input URL with a rolling hash, encodes the hash to base64, and returns the encoded hash.
    """
    hash_value = rolling_hash(input_url)
    hash_encoded = encode_to_custom_base64(hash_value, hash_length)
    return hash_encoded

def generate_sha256_code(input_url, hash_length=8):
    """
    Generate a deterministic short code using SHA-256 for collision fallback.
    Hashes the input URL with SHA-256, encodes the hash to base64, and returns the encoded hash.
    """
    sha256_hash = hashlib.sha256(input_url.encode('utf-8')).digest()
    # Convert the first hash_length * 6 bits to an integer (since each base64 char encodes 6 bits)
    num_bits = hash_length * 6
    hash_int = int.from_bytes(sha256_hash, 'big') >> (256 - num_bits)
    return encode_to_custom_base64(hash_int, hash_length)


    
