#!/usr/bin/env python3
"""Module that defines the Cache class"""
import redis
import uuid


class Cache:
    """Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """Generate a random key and store data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
