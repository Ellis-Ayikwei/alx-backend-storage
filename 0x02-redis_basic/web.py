#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable, Any 

# Create Redis instance (ris)
ris = redis.Redis()
ris.flushdb()

def method_call_count(method: Callable) -> Callable:
    """Decorator to count how many times a URL is accessed."""
    @wraps(method)
    def wrapper(url:str) -> str:
        """Increment the count for that key every time the method is called"""
        key = f"count:{url}"
        ris.incr(key)
        return method(url)
    return wrapper

@method_call_count
def get_page(url: str) -> str:
    """Fetch the page content, cache it, and track URL access count"""
    # Check if the URL content is cached
    cached_page = ris.get(url)
    if cached_page:
        return cached_page.decode('utf-8')

    # Fetch the page content if not cached
    response = requests.get(url)
    content = response.text

    # Cache the result with an expiration time of 10 seconds
    ris.setex(url, 10, content)

    return content
