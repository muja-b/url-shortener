import random
import string

def generate_short_url(length=6):
    """
    Generate a simple random short URL.
    Returns a random alphanumeric string of base64 characters in specified length.
    """
    # Use the custom character set (excludes some ASCII letters that cause problems with urls)
    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    return ''.join(random.choice(BASE64_CHARS) for _ in range(length))

def generate_url_hash(input_url, length=6):
    """
    Generate a short hash for URL shortening.
    Simple random approach - doesn't use the input URL.
    Returns a random alphanumeric string.
    """
    return generate_short_url(length)


    
