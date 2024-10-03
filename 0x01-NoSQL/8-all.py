#!/usr/bin/env python
""" the funtion to list all from a document """

def list_all(mongo_collection):
    """the funtion to list all in a collection"""
    result = mongo_collection.find()
    if not result :
        return []
    return result
