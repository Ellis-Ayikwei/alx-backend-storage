#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable

# Create Redis instance
ris = redis.Redis()
ris.flushdb()

def method_call_count(method: Callable) -> Callable:
    """Decorator to count how many times a URL is accessed."""
    @wraps(method)
    def wrapper(url: str, *args, **kwargs) -> str:
        """Increment the count for that URL each time the method is called."""
        key = f"count:{url}"
        ris.incr(key)  # Increments the key, creating it if it doesn't exist
        return method(url, *args, **kwargs)
    return wrapper

@method_call_count
def get_page(url: str) -> str:
    """Fetch the page content, cache it, and track URL access count."""
    cache_key = f"cache:{url}"
    
    # Check if the content is already cached
    cached_content = ris.get(cache_key)
    if cached_content:
        return cached_content.decode('utf-8')
    
    # If not cached, fetch the content and cache it for 10 seconds
    response = requests.get(url)
    content = response.text
    ris.setex(cache_key, 10, content)
   

get_page("http://slowwly.robertomurray.co.uk")