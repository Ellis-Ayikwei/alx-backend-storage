#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable, Optional

# Create Redis instance
ris = redis.Redis()
ris.flushdb()  # Clear existing data


def method_call_count(method: Callable) -> Callable:
    """Decorator to count URL access and cache content."""

    @wraps(method)
    def wrapper(url: str, timeout: int = 10, *args, **kwargs) -> Optional[str]:
        """Increment URL access count, check cache, fetch and cache content."""
        key = f"count:{url}"
        ris.incr(key)
        cache_key = f"cache:{url}"

        # Check cache first
        cached_content = ris.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")  # Decode bytes to string


        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise exception for non-2xx status codes
            content = response.text
            ris.setex(cache_key, 10, content)
            return content
        except (requests.exceptions.RequestException, redis.exceptions.RedisError) as e:
            print(f"Error fetching or caching content for {url}: {e}")
            return None  # Indicate error

    return wrapper


@method_call_count
def get_page(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch the page content, handle errors, and return content or None."""
    return get_page.wrapper(url, timeout)


# Example usage with timeout
content = get_page("http://slowwly.robertomurray.co.uk", timeout=5)
if content:
    print(content)
else:
    print("Error retrieving content.")
