#!/usr/bin/env python
""" the funtion to list all from a document """


def list_all(mongo_collection):
    """the function to list all documents in a collection"""
    result = list(mongo_collection.find())
    return result if result else []
