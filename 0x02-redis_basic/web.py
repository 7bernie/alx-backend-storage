#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps

# Establish a connection to Redis
store = redis.Redis()

def count_url_access(method):
    """ Decorator tracks how many times a URL is accessed in the key """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)
        
        # Error handling for Redis operations
        try:
            store.incr(count_key)
            store.set(cached_key, html)
            store.expire(cached_key, 10)
        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")
        
        return html
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """ Obtain and return HTML content of a url """
    try:
        res = requests.get(url)
        return res.text
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "Error: Failed to fetch URL content"

# Test the corrected code with different URLs
if __name__ == "__main__":
    url = "https://example.com"
    html_content = get_page(url)
    print(html_content)
