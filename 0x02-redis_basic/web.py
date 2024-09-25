#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable, Any 

# Create Redis instance (ris)
ris = redis.Redis()

def count_calls(method: Callable) -> Callable:
    """Count how many times methods of the Cache class are called."""
    @wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        url = args[0]  # Get the URL from the method args
        key = f"count:{url}"  # Key to store URL count
        """Increment the count for that key every time the method is called."""
        ris.incr(key)  # Increment access count in Redis
        return method(*args, **kwargs)
    
    return wrapper

@count_calls
def get_page(url: str) -> str:
    """Fetch the content of a URL and cache it in Redis with a 10-second expiration."""
    key = f"cache:{url}"
    cached_page = ris.get(key)
    
    if cached_page:
        return cached_page.decode("utf-8")
    
    # Fetch the content if not in cache
    response = requests.get(url)
    ris.setex(key, 10, response.text)
    return response.text
