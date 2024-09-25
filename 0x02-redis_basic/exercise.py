#!/usr/bin/env python3
"""Module that defines the Cache class"""
import redis
import uuid
from typing import Union, Any, Callable
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Count how many times methods of the Cache class are called
    
    Args:
        method: The method to decorate
    
    Returns:
        A decorated method that increments a Redis key for each call
    """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        """Increment the count for that key every time the method is called"""
        if hasattr(self, '_redis'):
            
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a method
    
    Args:
        method: The method to decorate
    
    Returns:
        A decorated method that stores the history of inputs and outputs
    """
    method_qualname = method.__qualname__
    @wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        """Store the history of inputs and outputs"""
        output = method(self, *args, **kwargs)
        if hasattr(self, '_redis'):
            self._redis.rpush(f"{method_qualname}:inputs", str(args))
            self._redis.rpush(f"{method_qualname}:outputs", output)
        return output
    return wrapper

class Cache():
    """Cache class"""

    def __init__(self):
        """Initialize the Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
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
    
def replay(method: Callable) -> None:
    """Replay the history of inputs and outputs for a method

    Args:
        method: The method to replay the history for
    """
    method_name = method.__qualname__
    
    # Check if the method is bound to an instance
    if not hasattr(method, '__self__'):
        print(f"Error: {method_name} is not bound to an instance.")
        return

    # Access the instance of the class
    instance = method.__self__

    # Check if Redis has stored any data for this method
    num_calls = instance.get_int(method_name)
    if num_calls is None or num_calls == 0:
        print(f"No calls were made to {method_name}.")
        return

    print(f"{method_name} was called {num_calls} times.")

    # Fetch inputs and outputs
    inputs = instance._redis.lrange(f"{method_name}:inputs", 0, num_calls - 1)
    outputs = instance._redis.lrange(f"{method_name}:outputs", 0, num_calls - 1)

    # Print each input-output pair
    for inp, out in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")
