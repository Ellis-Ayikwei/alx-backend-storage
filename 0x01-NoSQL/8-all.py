#!/usr/bin/env python3
""" the funtion to list all from a document """


def list_all(mongo_collection):
    """Return all documents in a collection"""
    return [doc for doc in mongo_collection.find()]
