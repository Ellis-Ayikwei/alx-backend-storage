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
        ris.incr(key)
        cache_key = f"cache:{url}"
        content = method(url, *args, **kwargs)
        ris.setex(cache_key, 10, content)
        return method(url, *args, **kwargs)
    return wrapper

@method_call_count
def get_page(url: str) -> str:
    """Fetch the page content, cache it, and track URL access count."""
    response = requests.get(url)
    content = response.text
   
    return content
   

get_page("http://slowwly.robertomurray.co.uk")