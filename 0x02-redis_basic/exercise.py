#!/usr/bin/env python3
"""Module that defines the Cache class"""
import redis
import uuid
from typing import Union, Any, Callable
from functools import wraps

def count_calls(method: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
    """Count how many times methods of the Cache class are called
    
    Args:
        method: The method to decorate
    
    Returns:
        A decorated method that increments a Redis key for each call
    """
    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Increment the count for that key every time the method is called"""
        if hasattr(self, '_redis'):
            key = f"{method.__qualname__}"
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """Cache class"""

    def __init__(self):
        """Initialize the Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, float, int]) -> str:
        """Generate a random key and store data in Redis
        
        Args:
            data (Union[str, bytes, float, int]): The data to store in Redis
        
        Returns:
            str: The random key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: callable = None) -> Any:
        """
        Get an item by key from Redis, and convert it using fn if provided
        
        Args:
            key: The key to retrieve the value for
            fn: An optional callable to convert the value
        
        Returns:
            The retrieved value, or None if key is not found
        """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value
    
    def get_str(self, key: str) -> str:
        """Get a string item by key from Redis
        
        Args:
            key: The key to retrieve the value for
        
        Returns:
            The retrieved value as a string, or None if key is not found
        """
        return self.get(key, lambda x: x.decode('utf-8'))
    
    def get_int(self, key: str) -> int:
        """Get an integer item by key from Redis
        
        Args:
            key (str): The key to retrieve the value for
        
        Returns:
            int: The retrieved value as an integer, or None if key is not found
        """
        return self.get(key, int)
        
        
