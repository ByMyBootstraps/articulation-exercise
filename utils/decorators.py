# quick and dirty 0 dependency caching
# I should really rewrite this to use a proper cache someday
import functools

import os
from os import path
import hashlib
import json

DATA_ROOT = os.environ.get('DATA_ROOT', "./")
CACHE_ROOT = path.join(DATA_ROOT, "cache/")

from utils.os_tools import nextVersion, lastVersion

def getHashKey( inp ) :
    hash_object = hashlib.sha256(str(inp).encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def cache( inp, out, source ):
    """
    Stores a mapping from str(inp) to out that will be recovered by read_cache
    If a mapping already exists, the new mapping overrides but does not delete the old one
    """
    target_dir = path.join(CACHE_ROOT, source)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    hex_dig = getHashKey(inp)

    fn = nextVersion(target_dir, f"{hex_dig}_{{n}}.json")
    target_file = path.join(target_dir, fn)

    with open( target_file, "w" ) as f:
        f.write(json.dumps(out, indent=2))

def read_cache( inp, source ):
    """
    If a mapping for str(inp) has been saved using cache, returns the corresponding out
    Otherwise, returns None

    source: a (hopefully) friendly name for the process that triggered this caching. This is how we distinguish between identical inputs passed to different functions.
    """
    target_dir = path.join(CACHE_ROOT, source)
    if not os.path.exists(target_dir):
        return None

    hex_dig = getHashKey(inp)
    
    fn, n = lastVersion(target_dir, f"{hex_dig}_{{n}}.json")
    if n == -1:
        return None

    try:
        target_file = path.join(target_dir, fn)
        with open( target_file, "r" ) as f:
            return json.loads(f.read())
    except Exception as e:
        raise e
        # return None
    
def cacheTryLoad( fnc, cache_key, cache_source, force_regen, *args, **kwargs):
    """
    If a mapping for str(cache_key) has been saved using cache, returns the corresponding out
    Otherwise, calls fnc(*args, **kwargs), saves the result using cache, and returns it

    fnc: function to call if no cached value is found (with *args, **kwargs)
    cache_source: a (hopefully) friendly name for the process that triggered this caching. This is how we distinguish between identical inputs passed to different functions.
    force_regen: if True, always calls fnc(*args, **kwargs) and saves the result using cache
    """
    if not force_regen:
        cached_resp = read_cache(cache_key, cache_source)
        if cached_resp:
            return cached_resp
    
    resp = fnc(*args, **kwargs)

    # cache resp for future use
    cache( cache_key, resp, cache_source)

    return resp

def usecache(valueSourceFn, cacheKeyFn=lambda *args, **kwargs: str(args), useCacheFn=lambda *args, **kwargs: True):
    """
    Decorator for functions that return a value that can be cached
    valueSourceFn: returns a key encoding which function was called - in practice this is not clearly distinct from the inputs key because i tend to do implicit currying
    cacheKeyFn: function that calculates the key for the cache - this needs to output a unique key for every input that behaves differently
    useCacheFn: function that determines whether to override the cache and recalculate the value
    """
    def decorator(fnc):
        @functools.wraps(fnc)
        def wrapper(*args, **kwargs):
            return cacheTryLoad(fnc, cacheKeyFn(*args, **kwargs), valueSourceFn(*args, **kwargs), not useCacheFn(*args, **kwargs), *args, **kwargs)
        return wrapper
    return decorator
