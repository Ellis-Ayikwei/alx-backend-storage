#!/usr/bin/env python3
"""The function that inserts into a new document in a collecion"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection"""

    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
