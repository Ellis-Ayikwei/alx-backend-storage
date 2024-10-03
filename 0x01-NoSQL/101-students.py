#!/usr/bin/env python3
"""
  A module defines a function that retruns the all students sorted by average
"""


def top_students(mongo_collection):
    """Return all students sorted by average score"""
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ])
