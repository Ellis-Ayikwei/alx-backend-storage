#!/usr/bin/env python3
""" This Module defines a funtion that changes all topics of the 
school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """Updates all topics of a school document based on the name."""
    filter = {"name": name}
    update = {"$set": {"topics": topics}}
    return mongo_collection.update_many(filter, update)
