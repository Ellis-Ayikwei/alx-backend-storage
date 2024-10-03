#!/usr/bin/env python3
"""The Module """


def schools_by_topic(mongo_collection, topic):
    """Returns a list of a dosc with the topic named {topic}"""
    topics_filter = {"topics": {"$in": [topic]}}
    return [doc for doc in mongo_collection.find(topics_filter)]
