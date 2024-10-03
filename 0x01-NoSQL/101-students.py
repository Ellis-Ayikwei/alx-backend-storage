#!/usr/bin/env python3
"""
  A module defines a function that retruns the all students sorted by average
"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    return mongo_collection.find({"averageScore": {"$gt": 70}})
