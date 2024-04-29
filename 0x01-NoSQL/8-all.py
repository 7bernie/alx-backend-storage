#!/usr/bin/env python3
"""
8-List all documents in Python
"""
import pymongo


def list_all(mongo_collection):
    """
    list all doc collections
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
