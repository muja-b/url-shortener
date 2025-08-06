import redis
import json
from typing import Optional
import logging

class RedisService:
    """Service for Redis cache operations."""
    
    def __init__(self, host='localhost', port=6379, db=0, ttl=86400):
        """
        Initialize Redis service.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            ttl: Time to live in seconds (default: 24 hours)
        """
        self.host = host
        self.port = port
        self.db = db
        self.ttl = ttl
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Redis."""
        try:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logging.info(f"Connected to Redis at {self.host}:{self.port}")
        except Exception as e:
            logging.warning(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def _get_key(self, short_code: str) -> str:
        """Generate Redis key for short code."""
        return f"url:short:{short_code}"
    
    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        if not self.redis_client:
            return False
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    def get_original_url(self, short_code: str) -> Optional[str]:
        """
        Get original URL from cache by short code.
        
        Args:
            short_code: The short code to look up
            
        Returns:
            Original URL if found in cache, None otherwise
        """
        if not self.is_connected():
            return None
        
        try:
            key = self._get_key(short_code)
            original_url = self.redis_client.get(key)
            if original_url:
                logging.info(f"Cache HIT for short code: {short_code}")
                return original_url
            else:
                logging.info(f"Cache MISS for short code: {short_code}")
                return None
        except Exception as e:
            logging.error(f"Redis get error: {e}")
            return None
    
    def set_url_mapping(self, short_code: str, original_url: str) -> bool:
        """
        Cache URL mapping (short code -> original URL).
        
        Args:
            short_code: The short code
            original_url: The original URL
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            key = self._get_key(short_code)
            self.redis_client.setex(key, self.ttl, original_url)
            logging.info(f"Cached URL mapping: {short_code} -> {original_url[:50]}...")
            return True
        except Exception as e:
            logging.error(f"Redis set error: {e}")
            return False
    
    def delete_url_mapping(self, short_code: str) -> bool:
        """
        Remove URL mapping from cache.
        
        Args:
            short_code: The short code to remove
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            key = self._get_key(short_code)
            self.redis_client.delete(key)
            logging.info(f"Deleted URL mapping from cache: {short_code}")
            return True
        except Exception as e:
            logging.error(f"Redis delete error: {e}")
            return False
    
    def clear_cache(self) -> bool:
        """
        Clear all URL cache entries.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            # Delete all keys with our prefix
            pattern = "url:short:*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                logging.info(f"Cleared {len(keys)} cache entries")
            return True
        except Exception as e:
            logging.error(f"Redis clear error: {e}")
            return False
    
    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        if not self.is_connected():
            return {"connected": False}
        
        try:
            info = self.redis_client.info()
            keys = self.redis_client.keys("url:short:*")
            return {
                "connected": True,
                "total_keys": len(keys),
                "memory_usage": info.get("used_memory_human", "N/A"),
                "uptime": info.get("uptime_in_seconds", 0)
            }
        except Exception as e:
            logging.error(f"Redis stats error: {e}")
            return {"connected": False, "error": str(e)} 